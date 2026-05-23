# 📈 Indian Market & Derivatives Intelligence Terminal

An institutional-grade, interactive **Streamlit** terminal that brings together technical analysis, market-wide opportunity scanning, ML ensemble signal engines, AI-powered recommendation narration, option pricing models, derivatives sentiment analysis, backtesting, and portfolio risk management for the Indian stock market (NSE).

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?logo=scikit-learn&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-0.2.40+-3776AB)

---

## ✨ Features

| Category | Feature | Description |
|---|---|---|
| **Market Scanner** | **Multi-Factor ML Scanner** | Scan the NIFTY 50 universe with ML-powered signal classification, automatic opportunity scoring (0–10), and conviction ranking. |
| | **Intelligence Feed** | Dynamic, institutional-style narrative alerts summarizing market participation and sector rotation. |
| | **Sector Intelligence** | Sector-wide strength aggregation and relative strength vs. NIFTY 50. |
| **Stock Analysis** | **Executive Summary V2** | Glassmorphism-styled AI decision support layout with signal badge, confidence bars, narrative insights, and secondary metric pills. |
| | **ML Signal Engine** | RandomForest + GradientBoosting ensemble classifier producing 7-class signal taxonomy (Strong Bullish → Strong Bearish + Uncertain) with explainable contributing factors. |
| | **AI Recommendation Narrator** | Human-readable market intelligence narratives with LLM support (Gemini/OpenAI/Claude) and high-quality template fallback (no API key required). |
| | **Autocomplete Search** | Search stocks instantly by typing ticker symbols or company names (e.g. `rel` -> `RELIANCE.NS`). |
| **Smart Engines (AI/ML)**| **25-Feature ML Pipeline** | Extracts momentum, trend, volume, volatility, price action, and persistence features for ML classification. |
| | **Regime Detection** | Classify market phases (Trending, Consolidation, Volatility Expansion) and detect transitions. |
| | **Anomaly Detection** | Isolation Forest ML engine flags statistically rare volume/volatility/momentum patterns. |
| | **Probability Engine** | Estimate success probability and confidence bands of technical setups. |
| | **Expected Move Range** | ATR-based 5-day move projection. |
| **Derivatives & Options**| **Options Analytics** | Black-Scholes pricing, implied volatility estimation, IV percentile, and Greeks (Call/Put). |
| | **Derivatives Sentiment** | Put/Call Ratio (PCR) proxy, Open Interest buildup (Long/Short buildup, Short covering, Long unwinding), and Max Pain. |
| **Quant Tools** | **Strategy Backtester** | Setup-based strategy backtests with custom targets, stop losses, and metrics (Sharpe, Sortino, Drawdown, Expectancy). |
| | **Portfolio Intelligence** | Position tracking, sector exposure, Value-at-Risk (VaR), and risk alerts. |

---

## 🏗️ Project Structure

```
Indian Market & Derivatives Intelligence Terminal/
├── app.py                          # Main Streamlit application (Phase 5 integrated)
├── requirements.txt                # Python dependencies
├── EXPLANATION.md                  # Comprehensive Dual-Layer Documentation
│
├── data/                           # Data Layer
│   ├── nse_data.py                 # YFinance data fetching & autocomplete
│   └── symbols.json                # Ticker-to-name mapping database
│
├── analytics/                      # Technical Analysis Layer
│   └── indicators.py               # Technical indicator computations
│
├── signals/                        # Signals Layer
│   └── rule_based.py               # Rule-based signal generator (ML fallback)
│
├── visualizations/                 # Visualization Layer
│   ├── candlestick.py              # Candlestick plotting with overlays
│   └── trend_cards.py              # 7-class visual signal cards
│
├── pricing/                        # Legacy option pricing (Original)
│   ├── black_scholes.py            # Black-Scholes model
│   └── greeks.py                   # Greeks calculator
│
├── src/                            # Extended Intelligence Modules (Phases 2-5)
│   ├── data/
│   │   ├── universe.py             # Stock universe & sector catalog
│   │   ├── market_context.py       # Relative strength calculations
│   │   └── position_sizing.py      # Position sizing calculators
│   │
│   ├── analytics/
│   │   ├── ml_features.py          # [Phase 5] 25-feature ML pipeline
│   │   ├── ml_signal_engine.py     # [Phase 5] RF+GB ensemble signal classifier
│   │   ├── llm_recommendation_engine.py # [Phase 5] AI Narrator (LLM + template)
│   │   ├── scanner.py              # Scanner engine & ML opportunity scoring
│   │   ├── trade_quality.py        # 4-factor trade quality scoring
│   │   ├── advanced_breadth.py     # Market participation & rotation
│   │   ├── ml_models.py            # Isolation Forest anomaly detection
│   │   ├── regime_detection.py     # Market regime & transition detection
│   │   ├── signal_reliability.py   # Historical setup backtesting & reliability
│   │   ├── probability_engine.py   # Setup success probability estimator
│   │   ├── options_intelligence.py # Options pricing, IV, & Greeks integration
│   │   ├── derivatives_sentiment.py# PCR, OI buildup classification, Max Pain
│   │   ├── backtesting.py          # Quant backtester with Sharpe & Sortino
│   │   └── portfolio_intelligence.py # Portfolio risk, exposure, & VaR engine
│   │
│   └── visualizations/
│       └── executive_summary_v2.py # [Phase 5] Glassmorphism executive summary
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip

### Installation & Launch

```bash
# 1. Navigate to the project directory
cd "Indian Market & Derivatives Intelligence Terminal"

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate           # Windows
source venv/bin/activate        # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the terminal
streamlit run app.py
```

The dashboard will open at **http://localhost:8501**.

### Optional: AI Narrator with LLM

The AI Recommendation Narrator works out of the box with high-quality templates (no API key needed). To enable LLM-powered narratives:

1. **Via sidebar:** Select a provider (Gemini/OpenAI/Claude) and enter your API key.
2. **Via `.env` file:** Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ```

---

## 🧭 Daily Workflow Example

1. **Scan the Market:** Launch **Market Scanner** mode to run the ML-powered batch scan.
2. **Review Context:** Check the **Market Intelligence Feed** and overall market **breadth metrics**.
3. **Select Setups:** Identify top opportunities under the **Top Opportunities** cards (look for 🤖 ML badge for ML-scored signals).
4. **Deep-Dive:** Switch to **Single Stock Analysis** and start typing the ticker/company name.
5. **Read the AI Summary:** The redesigned **Executive Summary** shows signal badge, confidence bar, AI narrative, and risk level in one glance.
6. **Check Contributing Factors:** Expand the **Signal Contributing Factors** panel to see exactly WHY the ML engine generated that signal.
7. **Verify with Derivatives:** Check derivatives sentiment and implied volatility (IV) levels.
8. **Backtest:** Run the historical backtest for that setup to verify win rate, Sharpe ratio, and expectancy.
9. **Trade:** Execute with automated position sizing and risk management guidelines.

---

## 📄 Documentation

For deep explanations of all technical terms, algorithms, mathematics, and user workflows, see the dual-layer documentation:
👉 **[EXPLANATION.md](EXPLANATION.md)**

---

<p align="center">
  Built with ❤️ using Python, Streamlit & Scikit-Learn
</p>
