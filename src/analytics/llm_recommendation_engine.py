# src/analytics/llm_recommendation_engine.py
"""AI Recommendation Narrator Layer for Phase 5.
Interprets structured analytics outputs and generates human-readable
market intelligence narratives using LLM APIs or template fallback.

The LLM is NOT responsible for generating signals or probabilities.
It ONLY interprets, summarizes, explains, and narrates existing analytics.
"""

import json
import os
import logging
from abc import ABC, abstractmethod
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


# ── LLM System Prompt ─────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a professional market intelligence analyst for the Indian stock market.
You interpret pre-computed analytics data and generate concise, institutional-grade
market intelligence summaries.

STRICT RULES:
1. ONLY interpret the data provided in the context. NEVER invent numbers, probabilities, or price targets.
2. NEVER guarantee future price movements. Use language like "suggests", "indicates", "may".
3. Always mention at least one risk factor or warning.
4. Keep the key_insight to 2-3 sentences maximum.
5. Be professional, concise, and actionable.
6. Reference specific data points from the context (e.g., "68% confidence", "Long Buildup").
7. The best_use_case should be a specific trading strategy.
8. The warning should be specific and actionable.

OUTPUT FORMAT (respond with ONLY valid JSON, no markdown):
{
    "key_insight": "2-3 sentence summary of the current situation",
    "best_use_case": "specific trading strategy recommendation",
    "warning": "specific risk factor to watch"
}"""


# ── Abstract LLM Provider ─────────────────────────────────────────────────

class LLMProvider(ABC):
    """Abstract base class for LLM API providers."""

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response from the LLM.

        Parameters
        ----------
        system_prompt : str
            System-level instructions for the LLM.
        user_prompt : str
            The user-facing prompt with analytics context.

        Returns
        -------
        str
            Raw text response from the LLM.
        """
        ...


class GeminiProvider(LLMProvider):
    """Google Gemini API provider."""

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=f"{system_prompt}\n\n{user_prompt}",
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise


class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=500,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise


class ClaudeProvider(LLMProvider):
    """Anthropic Claude API provider."""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-latest"):
        self.api_key = api_key
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.model,
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise


# ── Template Fallback (No LLM Required) ───────────────────────────────────

def _derive_momentum_label(context: dict) -> str:
    """Derive momentum label from context."""
    conf = context.get("confidence", 0.5)
    if conf >= 0.70:
        return "Strong"
    if conf >= 0.55:
        return "Moderate"
    if conf >= 0.40:
        return "Weak"
    return "Very Weak"


def _derive_warnings(context: dict) -> List[str]:
    """Generate contextual warnings from analytics data."""
    warnings = []

    # Anomaly warning
    if context.get("anomaly_status") == "Anomaly Detected":
        warnings.append("Anomalous price action detected — exercise caution with position sizing.")

    # Volatility warning
    vol = context.get("volatility_regime", "")
    if "High" in vol or "Expansion" in vol:
        warnings.append("Elevated volatility — consider wider stop losses and smaller positions.")

    # Regime transition warning
    if context.get("regime_transition", False):
        warnings.append(f"Regime transition detected — directional conviction may be lower during transitions.")

    # IV warning
    iv = context.get("iv_regime", "")
    if "High" in iv:
        warnings.append("High implied volatility — options premiums are elevated, caution on buying options.")

    # Low confidence warning
    if context.get("confidence", 0.5) < 0.45:
        warnings.append("Low signal confidence — consider waiting for stronger confirmation.")

    # Bearish derivatives vs bullish signal
    sig_class = context.get("signal_class", "neutral")
    deriv = context.get("derivatives_sentiment", "")
    if sig_class == "bullish" and "Bearish" in deriv:
        warnings.append("Derivatives sentiment diverges from bullish signal — watch for reversal.")
    elif sig_class == "bearish" and "Bullish" in deriv:
        warnings.append("Derivatives sentiment diverges from bearish signal — short covering possible.")

    # Fallback warning
    if not warnings:
        warnings.append("Monitor for regime change and volume confirmation.")

    return warnings


def _build_factors_text(context: dict) -> str:
    """Build a human-readable string from contributing factors."""
    factors = context.get("contributing_factors", [])
    if not factors:
        return "Multiple technical factors support the current bias"

    positives = [f["factor"] for f in factors if f.get("impact") == "positive"][:3]
    negatives = [f["factor"] for f in factors if f.get("impact") == "negative"][:2]

    parts = []
    if positives:
        parts.append("supported by " + ", ".join(positives).lower())
    if negatives:
        parts.append("tempered by " + ", ".join(negatives).lower())

    return " ".join(parts) if parts else "Multiple technical factors support the current bias"


def _template_narrator(context: dict) -> dict:
    """Generate recommendation using templates. Professional quality, zero cost.

    Returns dict with key_insight, best_use_case, warning, full_narrative,
    risk_level, momentum_label.
    """
    ticker = context.get("ticker", "STOCK")
    price = context.get("price", 0)
    signal = context.get("signal", "Neutral")
    signal_class = context.get("signal_class", "neutral")
    confidence = context.get("confidence", 0.5)
    probability = context.get("probability", 0.5)
    regime = context.get("regime", "Unknown")
    oi_buildup = context.get("oi_buildup", "Neutral")
    deriv_sent = context.get("derivatives_sentiment", "Neutral")
    anomaly = context.get("anomaly_status", "Normal")
    iv_regime = context.get("iv_regime", "Moderate")
    expected_move = context.get("expected_move_pct", 0.0)
    win_rate = context.get("win_rate")

    momentum = _derive_momentum_label(context)
    factors_text = _build_factors_text(context)
    warnings = _derive_warnings(context)

    conf_pct = f"{confidence:.0%}"
    prob_pct = f"{probability*100:.0f}%" if probability else "N/A"
    wr_pct = f"{win_rate*100:.1f}%" if win_rate else "N/A"

    # ── Key Insight Templates ────────────────────────────────────────────
    if signal_class == "bullish":
        if confidence >= 0.65:
            key_insight = (
                f"{ticker} shows strong bullish momentum at ₹{price:,.2f} with {conf_pct} confidence. "
                f"The setup is {factors_text}. "
                f"Derivatives positioning ({oi_buildup}) and {regime.lower()} regime confirm the directional bias."
            )
        elif confidence >= 0.50:
            key_insight = (
                f"{ticker} displays a moderate bullish setup at ₹{price:,.2f} with {conf_pct} confidence. "
                f"The setup is {factors_text}. "
                f"The {regime.lower()} regime provides supportive context."
            )
        else:
            key_insight = (
                f"{ticker} has a weak bullish lean at ₹{price:,.2f} with limited confirmation ({conf_pct}). "
                f"The setup is {factors_text}. "
                f"Conviction is low — wait for stronger signals before committing."
            )
    elif signal_class == "bearish":
        if confidence >= 0.65:
            key_insight = (
                f"{ticker} shows strong bearish pressure at ₹{price:,.2f} with {conf_pct} confidence. "
                f"The setup is {factors_text}. "
                f"Derivatives positioning ({oi_buildup}) reinforces downside risk."
            )
        elif confidence >= 0.50:
            key_insight = (
                f"{ticker} displays moderate bearish signals at ₹{price:,.2f} with {conf_pct} confidence. "
                f"The setup is {factors_text}. "
                f"The {regime.lower()} regime suggests continued caution."
            )
        else:
            key_insight = (
                f"{ticker} shows weak bearish tendencies at ₹{price:,.2f} ({conf_pct} confidence). "
                f"The setup is {factors_text}. "
                f"Downside conviction is limited."
            )
    elif signal_class == "uncertain":
        key_insight = (
            f"{ticker} at ₹{price:,.2f} is in a high-volatility uncertain state. "
            f"The {regime.lower()} regime and {anomaly.lower() if anomaly != 'Normal' else 'elevated volatility'} "
            f"make directional calls unreliable. Reduce exposure and wait for clarity."
        )
    else:  # neutral
        key_insight = (
            f"{ticker} at ₹{price:,.2f} is in a consolidation phase with no clear directional bias ({conf_pct} confidence). "
            f"The {regime.lower()} regime suggests waiting for a breakout or breakdown confirmation "
            f"before taking a position."
        )

    # ── Best Use Case ────────────────────────────────────────────────────
    use_case_map = {
        ("bullish", "Strong"): "Momentum swing trading (3-5 day hold)",
        ("bullish", "Moderate"): "Pullback entry with tight stop loss",
        ("bullish", "Weak"): "Small exploratory position with wide stop",
        ("bullish", "Very Weak"): "Watchlist only — wait for confirmation",
        ("bearish", "Strong"): "Short-term protective hedging or put buying",
        ("bearish", "Moderate"): "Reduce long exposure, tighten stop losses",
        ("bearish", "Weak"): "Monitor for further weakness before acting",
        ("bearish", "Very Weak"): "Maintain positions with trailing stops",
        ("uncertain", "Strong"): "Reduce position size significantly",
        ("uncertain", "Moderate"): "Avoid new positions until volatility settles",
        ("uncertain", "Weak"): "Straddle or options-based strategies only",
        ("uncertain", "Very Weak"): "Stay on sidelines",
        ("neutral", "Strong"): "Range-bound strategies (sell at resistance, buy at support)",
        ("neutral", "Moderate"): "Wait for breakout with volume confirmation",
        ("neutral", "Weak"): "No action — insufficient edge",
        ("neutral", "Very Weak"): "No action — insufficient edge",
    }
    best_use_case = use_case_map.get(
        (signal_class, momentum),
        "Wait for clearer directional signal"
    )

    # ── Risk Level ───────────────────────────────────────────────────────
    risk_factors = 0
    if anomaly == "Anomaly Detected":
        risk_factors += 2
    if "High" in str(iv_regime):
        risk_factors += 1
    if context.get("regime_transition", False):
        risk_factors += 1
    if confidence < 0.45:
        risk_factors += 1
    if expected_move > 4.0:
        risk_factors += 1

    if risk_factors >= 3:
        risk_level = "High"
    elif risk_factors >= 1:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    # ── Full Narrative ───────────────────────────────────────────────────
    full_narrative = (
        f"{key_insight}\n\n"
        f"Setup probability stands at {prob_pct} with a historical win rate of {wr_pct}. "
        f"Expected 5-day move is ±{expected_move:.1f}%. "
        f"IV regime is {iv_regime.lower()}.\n\n"
        f"⚠ {warnings[0]}"
    )

    return {
        "key_insight": key_insight,
        "best_use_case": best_use_case,
        "warning": warnings[0],
        "full_narrative": full_narrative,
        "risk_level": risk_level,
        "momentum_label": momentum,
    }


# ── Intelligence Context Builder ──────────────────────────────────────────

def build_intelligence_context(
    ticker: str,
    price: float,
    signal_info: dict,
    regime_result: dict,
    prob_result: dict,
    options_intel: dict,
    deriv_sentiment: dict,
    anomaly_result: dict,
    reliability: dict,
    move_result: dict,
) -> dict:
    """Assemble all analytics into a structured context dict for LLM/template.

    SAFETY: Only passes pre-computed insights. Never passes raw OHLCV data.
    """
    # Derive momentum label from signal confidence
    confidence = signal_info.get("confidence", 0.5)
    if confidence >= 0.70:
        momentum = "Strong"
    elif confidence >= 0.55:
        momentum = "Moderate"
    elif confidence >= 0.40:
        momentum = "Weak"
    else:
        momentum = "Very Weak"

    # Derive volatility label
    regime = regime_result.get("current_regime", "Unknown")
    iv = options_intel.get("iv_regime", "Moderate IV")
    if "High Volatility" in regime or "High" in iv:
        volatility_regime = "High / Expanding"
    elif "Consolidation" in regime or "Low" in iv or "Compressed" in iv:
        volatility_regime = "Low / Compressed"
    else:
        volatility_regime = "Stable / Moderate"

    return {
        "ticker": ticker,
        "price": price,
        "signal": signal_info.get("signal", "Neutral"),
        "signal_class": signal_info.get("signal_class", "neutral"),
        "confidence": confidence,
        "probability": prob_result.get("probability", 0.5),
        "regime": regime,
        "regime_transition": regime_result.get("transition_detected", False),
        "momentum": momentum,
        "volatility_regime": volatility_regime,
        "derivatives_sentiment": deriv_sentiment.get("sentiment", "Neutral"),
        "oi_buildup": deriv_sentiment.get("buildup", "Neutral"),
        "anomaly_status": anomaly_result.get("anomaly_class", "Normal"),
        "iv_regime": iv,
        "risk_level": "Moderate",  # Will be overridden by template/LLM
        "win_rate": reliability.get("win_rate"),
        "expected_move_pct": move_result.get("expected_move_pct", 0.0),
        "contributing_factors": signal_info.get("contributing_factors", []),
        "setup_type": signal_info.get("setup_type", "Unknown"),
    }


# ── LLM Output Validation ─────────────────────────────────────────────────

def _validate_llm_output(llm_output: dict, context: dict) -> bool:
    """Validate LLM output doesn't contradict analytics.

    Returns True if output is valid, False if it should be rejected.
    """
    insight = llm_output.get("key_insight", "").lower()
    signal_class = context.get("signal_class", "neutral")

    # Check: LLM shouldn't contradict signal direction
    if signal_class == "bullish" and any(w in insight for w in ["strong bearish", "sell immediately", "crash"]):
        logger.warning("LLM output contradicts bullish signal — rejecting.")
        return False
    if signal_class == "bearish" and any(w in insight for w in ["strong bullish", "buy aggressively", "rally"]):
        logger.warning("LLM output contradicts bearish signal — rejecting.")
        return False

    # Check: No guaranteed language
    forbidden = ["guaranteed", "will definitely", "certain to", "100% chance", "risk-free"]
    if any(word in insight for word in forbidden):
        logger.warning("LLM output contains forbidden guarantee language — rejecting.")
        return False

    return True


def _clean_error_message(e: Exception) -> str:
    """Format API exceptions into friendly, actionable user messages."""
    err_str = str(e)
    # Check for quota / rate limits (429)
    if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str or "RateLimit" in err_str:
        return "Quota Exceeded / Rate Limit Reached (429). Please check your API billing or plan limits."
    # Check for authentication / key issues (401)
    if "401" in err_str or "UNAUTHENTICATED" in err_str or ("invalid" in err_str.lower() and "key" in err_str.lower()) or "auth" in err_str.lower():
        return "Authentication Failed (401). Please verify your API Key."
    # Check for model access / not found (404)
    if "404" in err_str or ("model" in err_str.lower() and "not found" in err_str.lower()):
        return "Model not found or unsupported model version (404)."
    
    # Nested message parsing from JSON client responses
    if "'message':" in err_str:
        try:
            parts = err_str.split("'message':")
            if len(parts) > 1:
                subpart = parts[1].split(",")[0].strip().strip("'\"{}")
                return f"API Error: {subpart}"
        except Exception:
            pass

    # Generic short error
    if len(err_str) > 100:
        return f"API Error: {err_str[:90]}..."
    return err_str


# ── Main Recommendation Function ──────────────────────────────────────────

def get_recommendation(
    context: dict,
    provider: str = "None (Template)",
    api_key: Optional[str] = None,
) -> dict:
    """Generate AI recommendation from analytics context.

    Parameters
    ----------
    context : dict
        Output from ``build_intelligence_context()``.
    provider : str
        One of: "None (Template)", "Gemini", "OpenAI", "Claude".
    api_key : str, optional
        API key for the selected provider.

    Returns
    -------
    dict
        {"key_insight", "best_use_case", "warning", "full_narrative",
         "risk_level", "momentum_label"}
    """
    # Try .env file for API key if not provided
    if api_key is None or api_key.strip() == "":
        try:
            from dotenv import load_dotenv
            load_dotenv()
            env_keys = {
                "Gemini": "GEMINI_API_KEY",
                "OpenAI": "OPENAI_API_KEY",
                "Claude": "ANTHROPIC_API_KEY",
            }
            env_var = env_keys.get(provider)
            if env_var:
                api_key = os.environ.get(env_var)
        except ImportError:
            pass

    # If no API key or template mode, use template fallback
    if provider == "None (Template)" or not api_key or api_key.strip() == "":
        res = _template_narrator(context)
        res["mode"] = "Template"
        return res

    # Build user prompt from context
    user_prompt = (
        f"Analyze the following market intelligence for {context['ticker']}:\n\n"
        f"Current Price: ₹{context['price']:,.2f}\n"
        f"Signal: {context['signal']} ({context['signal_class']})\n"
        f"Confidence: {context['confidence']:.0%}\n"
        f"Setup Probability: {context['probability']*100:.0f}%\n"
        f"Market Regime: {context['regime']}\n"
        f"Momentum: {context['momentum']}\n"
        f"Volatility Regime: {context['volatility_regime']}\n"
        f"Derivatives Sentiment: {context['derivatives_sentiment']}\n"
        f"OI Buildup: {context['oi_buildup']}\n"
        f"Anomaly Status: {context['anomaly_status']}\n"
        f"IV Regime: {context['iv_regime']}\n"
        f"Win Rate: {context['win_rate']*100:.1f}%" if context.get('win_rate') else "Win Rate: N/A" + "\n"
        f"Expected 5-Day Move: ±{context['expected_move_pct']:.1f}%\n"
        f"Setup Type: {context['setup_type']}\n"
    )

    # Add contributing factors if available
    factors = context.get("contributing_factors", [])
    if factors:
        user_prompt += "\nContributing Factors:\n"
        for f in factors[:5]:
            user_prompt += f"- {f['factor']}: {f.get('detail', f.get('impact', ''))}\n"

    # Select provider
    try:
        providers = {
            "Gemini": lambda: GeminiProvider(api_key),
            "OpenAI": lambda: OpenAIProvider(api_key),
            "Claude": lambda: ClaudeProvider(api_key),
        }
        llm = providers[provider]()
        raw_response = llm.generate(SYSTEM_PROMPT, user_prompt)

        # Parse JSON response
        # Strip markdown code fences if present
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

        llm_output = json.loads(cleaned)

        # Validate output
        if not _validate_llm_output(llm_output, context):
            logger.warning("LLM output failed validation — falling back to template.")
            res = _template_narrator(context)
            res["mode"] = "Template Fallback (Validation Failed)"
            return res

        # Merge LLM output with template-derived fields
        template_result = _template_narrator(context)
        result = {
            "key_insight": llm_output.get("key_insight", template_result["key_insight"]),
            "best_use_case": llm_output.get("best_use_case", template_result["best_use_case"]),
            "warning": llm_output.get("warning", template_result["warning"]),
            "full_narrative": (
                llm_output.get("key_insight", "") + "\n\n"
                + f"📌 Best Use Case: {llm_output.get('best_use_case', '')}\n"
                + f"⚠ {llm_output.get('warning', '')}"
            ),
            "risk_level": template_result["risk_level"],
            "momentum_label": template_result["momentum_label"],
            "mode": "LLM",
        }
        return result

    except Exception as e:
        logger.error(f"LLM recommendation failed: {e}. Falling back to template.")
        res = _template_narrator(context)
        clean_err = _clean_error_message(e)
        res["mode"] = f"Template Fallback (Error: {clean_err})"
        return res
