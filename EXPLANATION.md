# 📈 Indian Market & Derivatives Intelligence Terminal

## Institutional AI-Assisted Market Intelligence & Probabilistic Decision Support System

> **This document has two layers.**
> Scroll down to find the one that fits you:
>
> | Layer | For whom | Starts at |
> |-------|----------|-----------|
> | 🟢 **Beginner Guide** | First-time users, non-technical traders | Right below |
> | 🔵 **Advanced Technical Docs** | Quant developers, advanced traders | [Section A — Platform Overview](#a-platform-overview) |

---
---

# 🟢 PART 1 — BEGINNER GUIDE

*Everything you need to start using the app in under 5 minutes.*

---

## 1. Quick Start — For First-Time Users

### What Is This App?

This app helps **traders and investors** quickly understand the Indian stock market using:

- 📊 **Charts & indicators** — see price trends at a glance
- ⚡ **Buy / sell signals** — the app tells you whether a stock looks bullish or bearish
- 🎯 **Probabilities** — know the historical success rate of a setup before you trade
- 🤖 **AI anomaly alerts** — the app flags unusual market behavior automatically
- 📌 **Options intelligence** — understand volatility and derivatives positioning
- 🧪 **Backtesting** — test whether a strategy actually worked in the past
- 🔍 **Market scanner** — scan 50 stocks in one click to find the best opportunities

### Who Is It For?

- ✅ Beginners learning to trade Indian stocks
- ✅ Active traders looking for faster analysis
- ✅ Swing traders who need daily opportunity scans
- ✅ Anyone who wants data-driven confidence before entering a trade

### How to Launch

1. Open a terminal / command prompt
2. Navigate to the project folder
3. Run:
   ```
   streamlit run app.py
   ```
4. The app opens in your browser automatically

### Two Modes

Once the app loads you will see a sidebar on the left with two modes:

| Mode | What it does |
|------|-------------|
| **Single Stock Analysis** | Deep-dive into one stock — signals, probabilities, options, backtest |
| **Market Scanner** | Scan all 50 NIFTY stocks at once — find the best opportunities |

Pick a mode and you're ready to go.

---

## 2. Complete Beginner Walkthrough

### Using Single Stock Analysis

**Step 1 — Search for a stock (with Autocomplete)**
In the sidebar, start typing either the ticker symbol (e.g., `TCS`) or the company name (e.g., `Tata`). The app will dynamically search the Indian stock universe and show matching suggestions in a dropdown list. Selecting a suggestion automatically populates the input field.

* **How Autocomplete Works:** The search engine queries a built-in mapping of the NIFTY 50 and NIFTY 100 stock universes. It checks both tickers and company names case-insensitively, sorting results so exact ticker matches appear first.
* **Easy Searching:** You don't need to memorize tickers like `HDFCBANK.NS`. Simply type `hdfc` or `bank`, and select the suggestion that matches your stock.
* **Examples:**
  * Typing `rel` -> Suggests `RELIANCE.NS - Reliance Industries Limited`
  * Typing `tcs` -> Suggests `TCS.NS - Tata Consultancy Services Limited`
  * Typing `hdfc` -> Suggests `HDFCBANK.NS - HDFC Bank Limited`
  * Typing `infosys` -> Suggests `INFY.NS - Infosys Limited`

**Step 2 — Choose a time period**
Pick how much history you want to analyze: 1 month, 3 months, 6 months, 1 year, or 2 years.
For most swing trading, **6 months to 1 year** works best.

**Step 3 — Read the Executive Summary**
This is the first thing you see — a row of cards showing:
- Current price
- Buy/sell signal
- Market regime (trending, sideways, etc.)
- Setup type (breakout, pullback, etc.)
- Win rate, probability, IV regime, anomaly status

*Think of it as a one-glance health check for the stock.*

**Step 4 — Look at the chart**
The candlestick chart shows price action with overlays like moving averages and Bollinger Bands. Green candles = price went up, red = price went down.

**Step 5 — Check the Signal & Recommendation**
The Signal Engine tells you:
- **Bullish** = the indicators suggest the stock may go up
- **Bearish** = the indicators suggest the stock may go down
- **Neutral** = no strong direction detected

Below that you get a plain-English recommendation.

**Step 6 — Review AI Intelligence**
This section shows three cards:
- **Anomaly Detection** — is anything unusual happening?
- **Regime Detection** — what market phase are we in?
- **Signal Reliability** — how often has this type of signal worked before?

**Step 7 — Check Options & Derivatives**
You'll see IV (implied volatility), option prices, Greeks, and derivatives sentiment. Don't worry if these terms are new — there's a glossary at the bottom of this document.

**Step 8 — Run a Backtest**
Open the "Strategy Backtest" section. Adjust stop loss and target, then see how this setup performed historically — win rate, Sharpe ratio, and max drawdown.

### Using Market Scanner

**Step 1 — Switch to Market Scanner**
In the sidebar, select "Market Scanner."

**Step 2 — Pick a scan period**
Choose how much history each stock should be analyzed over (e.g., 6 months).

**Step 3 — Wait for the scan**
The app scans all 50 NIFTY stocks. This takes 30–90 seconds.

**Step 4 — Read the Intelligence Feed**
At the top you'll see 2–4 short messages like:
> 📈 Sector leadership concentrated in Financials.
> ⚠ Narrow market participation (28% quality setups).

These tell you the overall market mood before you look at individual stocks.

**Step 5 — Check Top Opportunities**
Three cards show the highest-scored stocks with their conviction level.

**Step 6 — Filter and explore**
Use the dropdowns to filter by Sector, Setup Type, or Regime.
Switch between tabs: All Opportunities, Bullish, Bearish, and Anomalies.

**Step 7 — Click into a stock**
Found something interesting? Switch back to Single Stock Analysis mode and type that ticker to do a deep-dive.

---

## 3. Real End-to-End Examples

### Example 1: RELIANCE.NS

Suppose you type `RELIANCE.NS` in the sidebar. Here's what you might see:

| Card | Value | What it means |
|------|-------|---------------|
| Signal | **Bullish** | Indicators suggest upward momentum |
| Regime | **Trending Bullish** | The stock has been in an uptrend |
| Setup | **Trend Continuation** | The existing uptrend looks likely to continue |
| Probability | **67%** | Historically, this setup succeeds about 67% of the time |
| Anomaly | **Normal** | Nothing unusual — price action is within historical norms |
| IV Regime | **Moderate IV** | Options are neither cheap nor expensive |
| Derivatives | **Long Buildup** | Rising price with rising volume — fresh buying |

**What a trader might do:**
"Signal is bullish, trend is intact, probability is 67%, derivatives confirm long buildup. This looks like a reasonable buy setup. I'll check the backtest to see if the win rate holds and set a stop loss at 3%."

### Example 2: TCS.NS

| Card | Value | What it means |
|------|-------|---------------|
| Signal | **Neutral** | No strong directional signal |
| Regime | **Consolidation** | Stock is moving sideways |
| Setup | **Consolidation** | Tight range, waiting for breakout |
| Anomaly | **Anomaly Detected** | Volume is unusually high for a consolidation phase |

**What a trader might do:**
"The stock is consolidating but the anomaly engine flagged unusual volume. This could mean a breakout is coming. I'll add it to my watchlist and wait for a directional signal before entering."

### Example 3: HDFCBANK.NS

| Card | Value | What it means |
|------|-------|---------------|
| Signal | **Bearish** | Indicators point downward |
| Regime | **Trending Bearish** | Stock has been falling |
| Derivatives | **Short Buildup** | Falling price + rising volume = fresh shorting |
| Probability | **38%** | This setup has a low historical success rate for longs |

**What a trader might do:**
"Everything is bearish — signal, regime, derivatives. Probability of a bounce is only 38%. I'll avoid buying and look for opportunities elsewhere."

---

## 4. Daily Workflow — How a Trader Uses the App

Here's a practical morning routine:

| Step | Action | Time |
|------|--------|------|
| 1 | Open the app → Switch to **Market Scanner** | 10 sec |
| 2 | Read the **Intelligence Feed** — understand the market mood | 15 sec |
| 3 | Check **breadth metrics** — are most stocks bullish or bearish? | 10 sec |
| 4 | Look at **Top 3 Opportunities** — which stocks have highest scores? | 15 sec |
| 5 | Filter by your favorite sector if needed | 5 sec |
| 6 | Switch to **Single Stock Analysis** for the top pick | 10 sec |
| 7 | Read the **Executive Summary** — 12 metrics at a glance | 15 sec |
| 8 | Check **probability** and **signal reliability** | 10 sec |
| 9 | Check **derivatives sentiment** — does OI confirm the setup? | 10 sec |
| 10 | Run a **backtest** — has this strategy worked before? | 15 sec |
| 11 | Make your trading decision with confidence | — |

**Total time: ~2 minutes** from opening the app to making an informed decision.

---

## 5. Understanding Colors, Signals & Icons

### Signal Colors

| Color / Icon | Meaning |
|-------------|---------|
| 🟢 **Bullish** | Indicators point upward — potential buy opportunity |
| 🔴 **Bearish** | Indicators point downward — potential sell or avoid |
| 🟡 **Neutral** | No strong direction — wait for clarity |

### Conviction Levels

| Level | Score | What it means |
|-------|-------|---------------|
| ⭐⭐⭐⭐ **Elite Setup** | 8.0+ | Extremely strong opportunity across all factors |
| ⭐⭐⭐ **High Conviction** | 6.5–7.9 | Strong opportunity worth acting on |
| ⭐⭐ **Moderate** | 5.0–6.4 | Decent setup but not the strongest |
| ⭐ **Weak** | Below 5.0 | Poor alignment — better opportunities exist |

### Probability Scores

| Range | Label | What it means |
|-------|-------|---------------|
| 70%+ | ✅ High Probability | History strongly supports this setup |
| 50–69% | ⚠ Moderate Probability | Reasonable but not certain |
| Below 50% | ❌ Low Probability | History suggests this setup often fails |

### Anomaly Alerts

| Status | What it means |
|--------|---------------|
| **Normal** | Price action is within historical norms — nothing unusual |
| **Anomaly Detected** | Something statistically rare is happening — investigate further |

*Anomalies are NOT buy/sell signals. They are "pay attention" alerts.*

### Risk & Reliability

| Label | What it means |
|-------|---------------|
| ✅ **High Reliability** | This setup type has won 65%+ of the time historically |
| ⚠ **Moderate Reliability** | 50–65% historical win rate — use with additional confirmation |
| ❌ **Low Reliability** | Below 50% — this setup frequently fails |

---

## 6. AI & ML — Explained Simply

The app uses four "smart engines" behind the scenes. Here's what each one does in plain English:

### 🔬 Anomaly Detection
**What it does:** Looks at volume, volatility, and momentum and asks: *"Is today's behavior normal or unusual compared to the last few months?"*
**How it helps:** If a stock suddenly has 3× normal volume while moving sideways, something may be about to happen. The anomaly engine flags it so you can investigate.

### 🌡️ Regime Detection
**What it does:** Classifies the market into phases — *trending up, trending down, consolidating, or volatile*.
**How it helps:** Strategies that work in a trending market fail in a sideways market. Knowing the regime helps you pick the right approach.

### 📊 Signal Reliability
**What it does:** Looks back through history and counts how many times the same type of setup (breakout, pullback, etc.) led to a profit.
**How it helps:** Instead of guessing, you get a concrete win rate like "this setup has worked 68% of the time."

### 🎯 Probability Engine
**What it does:** Combines historical win rate with current conditions (volume, momentum, trend alignment) to estimate the probability of success *right now*.
**How it helps:** Two breakouts can look the same on a chart, but one has strong volume and trend alignment (72% probability) while the other doesn't (45%). The engine tells you which is which.

---

## 7. What Should I Look At First?

If you're overwhelmed by all the information, here's a simple priority guide:

### For Single Stock Analysis

| Priority | Section | Why |
|----------|---------|-----|
| 1st | **Executive Summary** | Get the full picture in 5 seconds |
| 2nd | **Signal & Recommendation** | Know the direction and action |
| 3rd | **Probability & Reliability** | Know if the setup is trustworthy |
| 4th | **Derivatives Sentiment** | Does smart money confirm the setup? |
| 5th | **Backtest** | Has this actually worked before? |
| Optional | Chart, indicators, raw data | Only if you want to dig deeper |

### For Market Scanner

| Priority | Section | Why |
|----------|---------|-----|
| 1st | **Intelligence Feed** | Understand the market mood |
| 2nd | **Top 3 Opportunities** | See the best setups instantly |
| 3rd | **Breadth Metrics** | Is the market broadly strong or weak? |
| 4th | **Anomalies Tab** | See if any stock has unusual behavior |
| Optional | Filters, full table | Explore specific sectors or setups |

### The 30-Second Rule

If you only have 30 seconds:
1. Look at the **signal** (Bullish / Bearish / Neutral)
2. Look at the **probability** (above or below 50%?)
3. Look at the **conviction** (Elite / High / Moderate / Weak)

These three numbers tell you 80% of what you need to know.

---

## 8. Frequently Asked Questions

**Q: Do I need to know coding to use this app?**
A: No. Just run `streamlit run app.py` once, and everything works in your browser. No coding needed to analyze stocks.

**Q: Is this app giving me guaranteed trading advice?**
A: No. This app provides *data-driven analysis and historical probabilities*. All trading involves risk. The probabilities are estimates based on past data — they are not guarantees.

**Q: What does "Anomaly Detected" mean? Should I buy?**
A: An anomaly means something *statistically unusual* is happening. It could be bullish or bearish. It's a prompt to investigate further, not a direct buy/sell signal.

**Q: Why does the scanner take time?**
A: The scanner fetches live data for 50 stocks from Yahoo Finance, computes indicators, runs ML models, and scores each stock. This takes 30–90 seconds depending on your internet speed.

**Q: What stock exchange does this app cover?**
A: It covers stocks listed on the **NSE (National Stock Exchange)** of India. Tickers end with `.NS` (e.g., `RELIANCE.NS`).

**Q: Can I add my own stocks to the scanner?**
A: The scanner currently scans the NIFTY 50 universe. The stock list is defined in `src/data/universe.py` and can be customized.

**Q: What does IV Percentile mean in simple terms?**
A: It tells you whether options are *cheap or expensive* right now compared to the past year. High IV Percentile (80%+) = expensive options. Low IV Percentile (20% or less) = cheap options.

**Q: What's the difference between Signal and Probability?**
A: The **signal** tells you the *direction* (bullish or bearish). The **probability** tells you *how likely* that direction is to play out based on historical data. A bullish signal with 45% probability is much weaker than one with 75%.

---
---

# 🔵 PART 2 — ADVANCED TECHNICAL DOCUMENTATION

*Institutional-grade architecture, module internals, and quant concepts.*
*If you're a developer, quant researcher, or advanced trader, this section is for you.*

---

## A. Platform Overview

### Evolution

This platform evolved through four distinct phases:

| Phase | Focus | Outcome |
|-------|-------|---------|
| **Phase 1** | Single-stock trader intelligence | OHLCV analytics, indicators, signals, trade quality, position sizing, executive summaries |
| **Phase 2** | Market-wide opportunity discovery | Scanner engine, NIFTY universe, sector intelligence, breadth analysis, conviction hierarchy |
| **Phase 3** | Probabilistic intelligence & explainable ML | Anomaly detection, regime detection, signal reliability, probability engine, advanced breadth |
| **Phase 4** | Derivatives intelligence & quant research | Options pricing, IV analytics, derivatives sentiment, backtesting, portfolio intelligence |

### Philosophy

This is **NOT** a technical indicators dashboard or an academic options calculator.

This **IS** an institutional-grade market intelligence terminal designed to:

- Accelerate trader decision-making
- Provide probabilistic reasoning
- Deliver explainable intelligence
- Prioritize opportunities by conviction
- Integrate market structure with derivatives positioning
- Reduce manual analysis workload

Every feature serves a single purpose: **help the trader make better decisions faster.**

---

## B. Complete Dashboard Workflow

### Mode 1: Single Stock Analysis

When a trader enters a ticker, the platform executes this pipeline:

```
Ticker Input → Data Fetch (yfinance) → Compute Indicators → Generate Signals
    → Classify Setup → Detect Anomalies → Detect Regime → Evaluate Reliability
    → Estimate Probability → Compute Expected Move → Options Intelligence
    → Derivatives Sentiment → Executive Summary → Visualization
```

**Output sections:**

1. **Executive Summary** — 12-metric institutional overview (price, signal, regime, trade quality, setup, win rate, probability, IV regime, derivatives sentiment, OI buildup, anomaly, expected move)
2. **Price Action & Indicators** — Interactive candlestick chart with overlays
3. **Technical Indicators** — Latest values in compact table
4. **Signal & Recommendation** — Rule-based signal with actionable recommendation
5. **AI Intelligence Panel** — Anomaly detection, regime detection, signal reliability, probability assessment, expected move
6. **Options & Derivatives Intelligence** — IV analysis, option pricing, Greeks, derivatives sentiment, max pain, OI buildup
7. **Strategy Backtest** — Interactive backtesting with configurable SL/target
8. **Raw OHLCV Data** — Last 20 data points

### Mode 2: Market Scanner

The scanner executes across the NIFTY 50 universe:

```
NIFTY Universe → Batch Fetch → Per-Stock: Indicators + Signals + Trade Quality
    + Relative Strength + Anomaly Detection + Regime Detection
    → Sector Strength → Multi-Factor Scoring → Conviction Ranking
    → Advanced Breadth → Market Intelligence Feed → Visualization
```

**Output sections:**

1. **Market Intelligence Feed** — 2-4 institutional-style narrative alerts
2. **Breadth Metrics** — Advancing/Declining, Bullish %, Bearish %, Participation
3. **Top Opportunities** — Top 3 ranked setups with scores
4. **Filters** — Sector, Setup Type, Regime
5. **Tabbed Results** — All / Bullish / Bearish / Anomalies

---

## C. Module-by-Module Explanation

### Scanner Engine (`src/analytics/scanner.py`)

- **Purpose**: Scans the NIFTY 50 universe, computes indicators, generates signals, and ranks opportunities.
- **Inputs**: List of tickers, historical period
- **Outputs**: Ranked DataFrame with Signal, Confidence, Setup Type, Trade Quality, Relative Strength, Anomaly Score, Anomaly Class, Regime, Opportunity Score, Conviction, Explanation
- **Trader Relevance**: Replaces hours of manual stock-by-stock analysis with a single scan.

### Trade Quality Engine (`src/analytics/trade_quality.py`)

- **Purpose**: Scores each trade setup on four dimensions: trend strength, momentum, volume confirmation, volatility quality.
- **Inputs**: SMA difference, RSI, volume, average volume, ATR, price
- **Outputs**: Component scores (0-10) and weighted overall quality score
- **Trader Relevance**: Quantifies "how good is this setup?" objectively.

### Signal Engine (`signals/rule_based.py`)

- **Purpose**: Generates buy/sell/hold signals from technical indicator thresholds.
- **Inputs**: DataFrame with computed indicators
- **Outputs**: Signal (Bullish/Bearish/Neutral), confidence (0-1), explanation, recommendation
- **Trader Relevance**: Removes subjectivity from signal generation.

### Regime Detection (`src/analytics/regime_detection.py`)

- **Purpose**: Classifies the current market regime and detects transitions.
- **Regimes**: Trending Bullish, Trending Bearish, Consolidation, High Volatility Expansion, Sideways
- **Outputs**: Current regime, previous regime, transition flag, duration, alert
- **Trader Relevance**: Tells the trader "what kind of market is this?" — strategies that work in trends fail in consolidation.

### Breadth Intelligence (`src/analytics/advanced_breadth.py`)

- **Purpose**: Computes market-wide participation, sector leadership, divergence, and generates narrative feeds.
- **Inputs**: Scanner results DataFrame
- **Outputs**: Bullish/bearish percentages, participation rate, sector rotation, divergence flag, market narrative, alerts
- **Trader Relevance**: Answers "Is the market broadly strong or is strength concentrated?"

### Relative Strength (`src/data/market_context.py`)

- **Purpose**: Computes stock vs. NIFTY 50 relative performance.
- **Inputs**: Stock OHLCV DataFrame, NIFTY OHLCV DataFrame
- **Outputs**: RS ratio (>1 = outperformance)
- **Trader Relevance**: Identifies stocks outperforming the broader market.

### Probability Engine (`src/analytics/probability_engine.py`)

- **Purpose**: Estimates setup success probability using historical hit rate + factor adjustments (momentum, volume, trend alignment, volatility).
- **Inputs**: Indicator DataFrame, setup type
- **Outputs**: Probability (0.10-0.95), confidence band, factor breakdown, explanation
- **Trader Relevance**: Moves the platform from "this is a breakout" to "this breakout has a 72% probability of continuation."

### Anomaly Detection (`src/analytics/ml_models.py`)

- **Purpose**: Uses Isolation Forest on volume ratio, ATR ratio, and rate-of-change to detect statistically rare price action.
- **Inputs**: Indicator DataFrame (50+ rows)
- **Outputs**: Anomaly score (0-100), anomaly class (Normal/Anomaly Detected), explanation
- **Trader Relevance**: Anomalies are NOT signals — they are investigation prompts. "Something unusual is happening here — pay attention."

### Signal Reliability (`src/analytics/signal_reliability.py`)

- **Purpose**: Backtests setup types on historical data to compute win rate, expectancy, and reliability labels.
- **Inputs**: Indicator DataFrame, setup type
- **Outputs**: Win rate, total signals, average 5-day return, expectancy, reliability label
- **Trader Relevance**: Answers "How reliable has this type of setup been historically?"

### Options Intelligence (`src/analytics/options_intelligence.py`)

- **Purpose**: Integrates Black-Scholes pricing, Greeks, implied volatility estimation, IV percentile, and RV analysis.
- **Inputs**: Indicator DataFrame, optional strike, risk-free rate, time-to-expiry
- **Outputs**: IV estimate, RV, IV percentile, IV regime, call/put prices, Greeks, explanation
- **Trader Relevance**: Tells the trader whether options are cheap/expensive and whether volatility supports the setup.

### Derivatives Sentiment (`src/analytics/derivatives_sentiment.py`)

- **Purpose**: Estimates Put-Call Ratio, classifies OI buildup (Long Buildup, Short Buildup, Short Covering, Long Unwinding), estimates max pain.
- **Inputs**: OHLCV DataFrame
- **Outputs**: PCR proxy, buildup classification, max pain estimate, overall sentiment, explanation
- **Trader Relevance**: Confirms or contradicts the technical setup with derivatives positioning.

### Backtesting Engine (`src/analytics/backtesting.py`)

- **Purpose**: Runs institutional-grade backtests on setup types with configurable holding period, stop loss, and target.
- **Inputs**: Indicator DataFrame, setup type, holding period, SL%, target%
- **Outputs**: Total trades, win rate, avg return, CAGR, Sharpe, Sortino, max drawdown, expectancy, profit factor, trade log
- **Trader Relevance**: Validates strategies before committing capital.

### Portfolio Intelligence (`src/analytics/portfolio_intelligence.py`)

- **Purpose**: Tracks positions, computes exposure, sector concentration, VaR, and generates portfolio alerts.
- **Inputs**: List of position dicts (ticker, quantity, avg_price, current_price)
- **Outputs**: Total value, P&L, sector exposure, concentration warnings, VaR (95%), portfolio volatility
- **Trader Relevance**: Prevents over-concentration and quantifies portfolio risk.

---

## D. Market Intelligence Concepts

### Breadth Divergence
When the index rises while the majority of stocks are bearish, or vice versa. This signals that surface-level strength may be misleading and a reversal could be approaching.

### Sector Rotation
Leadership shifts from one sector to another (e.g., Financials → IT). Detected by comparing average Trade Quality and Relative Strength across sectors.

### Volatility Regimes
- **Low Volatility**: ATR/Close < 1.2% — consolidation, potential breakout ahead
- **Moderate**: Normal market conditions
- **High Volatility Expansion**: ATR/Close > 3% — rapid moves, wider stops needed

### Anomaly Detection
Uses Isolation Forest (unsupervised ML) to identify statistically rare combinations of volume, volatility, and momentum. Anomalies are attention flags, not trading signals.

### Probabilistic Setups
Each setup type receives an estimated probability of success based on: historical hit rate + momentum quality + volume confirmation + trend alignment + volatility conditions. All probabilities are bounded [10%-95%] and fully explainable.

### Regime Transitions
Detects shifts between regimes (e.g., Consolidation → Trending Bullish). Transitions are high-value signals because strategies must adapt to the new regime.

### Conviction Hierarchy
- **Elite Setup ⭐⭐⭐⭐**: Opportunity Score ≥ 8.0
- **High Conviction ⭐⭐⭐**: Score ≥ 6.5
- **Moderate ⭐⭐**: Score ≥ 5.0
- **Weak ⭐**: Score < 5.0

---

## E. Options & Derivatives Intelligence

### Black-Scholes Model
Prices European call and put options using: spot price, strike price, time to expiry, risk-free rate, and volatility. Used to generate theoretical ATM option prices.

### Greeks
| Greek | Measures | Trader Use |
|-------|----------|------------|
| **Delta** | Price sensitivity to underlying | Directional exposure |
| **Gamma** | Rate of Delta change | Hedging difficulty near expiry |
| **Vega** | Sensitivity to IV changes | Volatility exposure |
| **Theta** | Daily time decay | Cost of holding options |
| **Rho** | Interest rate sensitivity | Generally minor for short-dated |

### Implied Volatility (IV)
The market's expectation of future volatility implied by option prices. Higher IV = more expensive options. The platform estimates IV from realized volatility when live option chain data is unavailable.

### IV Percentile
Shows where current IV stands relative to its historical range. IV Percentile ≥ 80% means options are historically expensive — selling strategies may be attractive. IV Percentile ≤ 20% means options are cheap — buying strategies may be attractive.

### OI Buildup Classification
| Pattern | Price | Volume | Meaning |
|---------|-------|--------|---------|
| **Long Buildup** | Rising | Rising | Fresh buying — bullish |
| **Short Buildup** | Falling | Rising | Fresh shorting — bearish |
| **Short Covering** | Rising | Falling | Shorts exiting — moderately bullish |
| **Long Unwinding** | Falling | Falling | Longs exiting — moderately bearish |

### Max Pain
The strike price where option writers would lose the least money. Stocks tend to gravitate toward max pain near expiry.

---

## F. Executive Summary Engine

The executive summary combines 12 metrics across market structure, momentum, volatility, derivatives, and ML intelligence into a single institutional-grade overview panel:

1. Current Price, Signal, Regime, Trade Quality
2. Setup Type, Win Rate, Success Probability, IV Regime
3. Derivatives Sentiment, OI Buildup, Anomaly Status, Expected Move

This allows traders to assess a stock's full intelligence profile in under 5 seconds.

---

## G. Scanner & Prioritization Engine

### Multi-Factor Opportunity Score

The Opportunity Score (0-10) is computed as a weighted combination:

| Factor | Weight | Source |
|--------|--------|--------|
| Trade Quality | 30% | Trend, momentum, volume, volatility |
| Signal Confidence | 20% | Rule-based signal engine |
| Relative Strength | 20% | Stock vs NIFTY performance |
| Sector Strength | 30% | Average sector trade quality |

### Conviction Mapping
Score → Conviction label (Elite/High/Moderate/Weak)

### Explanation Engine
Each ranked stock receives an auto-generated explanation of why it ranked high or low.

---

## H. Backtesting & Reliability

### Strategy Evaluation
The backtest engine simulates historical trades for a given setup type with configurable stop loss and target. It tracks:
- Win rate and loss rate
- Average return per trade
- Sharpe ratio (risk-adjusted return)
- Sortino ratio (downside risk-adjusted)
- Maximum drawdown
- Expectancy (expected gain per trade)
- Profit factor (gross profits / gross losses)

### Historical Reliability
The signal reliability engine scans past data for identical setup types and computes their historical success rate. This allows traders to understand: "Has this kind of setup worked before?"

---

## I. System Architecture

```
Indian Market & Derivatives Intelligence Terminal/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── EXPLANATION.md                  # This documentation
│
├── data/                           # Data layer (Phase 1)
│   ├── nse_data.py                 # Yahoo Finance data fetching
│   └── symbols.json                # Symbol catalog
│
├── analytics/                      # Core analytics (Phase 1)
│   └── indicators.py               # Technical indicator computation
│
├── signals/                        # Signal generation (Phase 1)
│   └── rule_based.py               # Rule-based signal engine
│
├── visualizations/                 # Visualization layer (Phase 1)
│   ├── candlestick.py              # Plotly candlestick charts
│   └── trend_cards.py              # Signal card renderer
│
├── pricing/                        # Legacy option pricing (Original)
│   ├── black_scholes.py            # Black-Scholes model
│   └── greeks.py                   # Greeks calculator
│
├── src/                            # Extended intelligence modules
│   ├── data/
│   │   ├── universe.py             # NIFTY universe management (Phase 2)
│   │   ├── market_context.py       # Index regime & relative strength (Phase 1)
│   │   └── position_sizing.py      # Position sizing engine (Phase 1)
│   │
│   ├── analytics/
│   │   ├── scanner.py              # Market scanner engine (Phase 2)
│   │   ├── trade_quality.py        # Trade quality scoring (Phase 1)
│   │   ├── advanced_breadth.py     # Advanced breadth intelligence (Phase 3)
│   │   ├── ml_models.py            # Isolation Forest anomaly detection (Phase 3)
│   │   ├── regime_detection.py     # Regime transition detection (Phase 3)
│   │   ├── signal_reliability.py   # Historical signal reliability (Phase 3)
│   │   ├── probability_engine.py   # Probabilistic setup engine (Phase 3)
│   │   ├── options_intelligence.py # Options & IV analytics (Phase 4)
│   │   ├── derivatives_sentiment.py# Derivatives sentiment engine (Phase 4)
│   │   ├── backtesting.py          # Advanced backtesting engine (Phase 4)
│   │   └── portfolio_intelligence.py # Portfolio risk engine (Phase 4)
│   │
│   └── visualizations/
│       └── executive_summary.py    # Executive summary renderer (Phase 1)
```

### Data Flow

```
Yahoo Finance API → nse_data.py → indicators.py → rule_based.py → scanner.py
                                                                       ↓
                                          ml_models.py ← indicators_df → regime_detection.py
                                          signal_reliability.py ←──────→ probability_engine.py
                                          options_intelligence.py ←─────→ derivatives_sentiment.py
                                          backtesting.py ←──────────────→ advanced_breadth.py
                                                                       ↓
                                                                   app.py (Streamlit UI)
```

### Caching Strategy
- `@st.cache_data(ttl=600)` for Yahoo Finance fetches (10-minute TTL)
- Index data fetched once per scanner run
- Indicators computed once per stock and reused across engines

---

## J. Product Philosophy

### What This Platform IS

An **Institutional AI-Assisted Indian Market & Derivatives Intelligence Terminal** focused on:

- **Trader workflow acceleration** — reduce hours of analysis to minutes
- **Probabilistic reasoning** — move from "this looks bullish" to "72% probability"
- **Explainable intelligence** — every score, every ranking has a reason
- **Opportunity prioritization** — strongest setups surface first
- **Market structure awareness** — breadth, regime, sector rotation
- **Derivatives confirmation** — options positioning validates technical setups
- **Institutional-grade analytics** — Sharpe, Sortino, VaR, expectancy

### What This Platform Is NOT

- ❌ A technical indicators dashboard
- ❌ An academic quant project
- ❌ An options calculator
- ❌ A black-box prediction system
- ❌ A get-rich-quick tool

### Design Principles

1. **Explainability over complexity** — every output can be traced to its inputs
2. **Bounded probabilities** — no 100% predictions, all probabilities clamped [10%-95%]
3. **Graceful degradation** — if any module fails, the rest continue working
4. **Trader cognition** — information is prioritized, not dumped
5. **Signal-to-noise** — filters, tabs, and conviction hierarchy reduce noise

---

## K. Glossary

> One-liner definitions for every important term used across the platform.

### Price & Market Data

| Term | Definition |
|------|------------|
| **OHLCV** | Open, High, Low, Close, Volume — the five standard data points for each trading bar. |
| **Candlestick** | A chart element showing open, high, low, close prices for a time period as a body and wicks. |
| **Ticker** | A unique symbol representing a stock on an exchange (e.g., RELIANCE.NS). |
| **Spot Price** | The current market price of the underlying stock. |
| **Bar** | A single time-period unit of OHLCV data (e.g., one day). |
| **Time Series** | A sequence of data points ordered by time, such as daily closing prices. |
| **Intraday** | Data or activity occurring within a single trading day. |
| **Historical Data** | Past OHLCV records used for analysis and backtesting. |

### Technical Indicators

| Term | Definition |
|------|------------|
| **SMA (Simple Moving Average)** | The arithmetic mean of closing prices over a specified number of periods. |
| **EMA (Exponential Moving Average)** | A weighted moving average that gives more importance to recent prices. |
| **SMA20 / SMA50** | 20-period and 50-period simple moving averages used to gauge trend direction. |
| **RSI (Relative Strength Index)** | A momentum oscillator (0–100) measuring the speed and magnitude of price changes. |
| **MACD (Moving Average Convergence Divergence)** | A trend-following momentum indicator showing the relationship between two EMAs. |
| **MACD Signal Line** | A 9-period EMA of the MACD line used to generate crossover signals. |
| **Bollinger Bands** | Bands plotted two standard deviations above and below a moving average to measure volatility. |
| **BB Upper / BB Lower** | The upper and lower Bollinger Band boundaries. |
| **ATR (Average True Range)** | A volatility indicator measuring the average range of price movement over N periods. |
| **VWAP (Volume Weighted Average Price)** | The average price weighted by volume, used as a benchmark for institutional execution. |
| **ADX (Average Directional Index)** | Measures the strength of a trend regardless of its direction (0–100). |
| **True Range** | The greatest of: current high minus low, absolute high minus previous close, or absolute low minus previous close. |
| **Crossover** | When one indicator line crosses above or below another (e.g., MACD crossing its signal). |
| **Overbought** | A condition where RSI > 70, suggesting the asset may be due for a pullback. |
| **Oversold** | A condition where RSI < 30, suggesting the asset may be due for a bounce. |

### Signals & Setups

| Term | Definition |
|------|------------|
| **Signal** | A buy/sell/hold recommendation generated by the rule-based engine. |
| **Bullish Signal** | Indicates upward price momentum or favorable buying conditions. |
| **Bearish Signal** | Indicates downward price momentum or favorable selling/shorting conditions. |
| **Setup Type** | Classification of the current technical pattern (Breakout, Pullback, Reversal, Trend Continuation, Consolidation). |
| **Breakout** | A price move above a resistance level (e.g., above Bollinger Upper Band). |
| **Pullback** | A temporary price decline within an uptrend, offering a re-entry opportunity. |
| **Reversal** | A change in the direction of the prevailing trend (e.g., RSI crossing above 30 from oversold). |
| **Trend Continuation** | Confirmation that the existing trend is intact and likely to persist. |
| **Consolidation** | A period of low volatility where price moves sideways within a narrow range. |
| **Confidence** | A 0–1 score measuring how strongly the signal engine believes in the generated signal. |

### Trade Quality & Scoring

| Term | Definition |
|------|------------|
| **Trade Quality Score** | A composite 0–10 score evaluating a setup across trend, momentum, volume, and volatility. |
| **Trend Strength** | How strongly price is trending, derived from SMA difference. |
| **Volume Confirmation** | Whether volume supports the current price move (volume above average = confirmation). |
| **Volatility Quality** | Lower ATR relative to price indicates tighter, more predictable moves. |
| **Opportunity Score** | A weighted 0–10 score combining Trade Quality, Signal Confidence, Relative Strength, and Sector Strength. |
| **Conviction Hierarchy** | A four-tier ranking: Elite (≥8), High (≥6.5), Moderate (≥5), Weak (<5). |

### Market Intelligence

| Term | Definition |
|------|------------|
| **Relative Strength (RS)** | Ratio of stock returns to index returns; RS > 1 means the stock outperforms the index. |
| **Breadth** | The proportion of stocks advancing vs. declining in the market. |
| **Participation Rate** | Percentage of scanned stocks with Trade Quality above 5.0. |
| **Breadth Divergence** | When index direction conflicts with the majority of individual stock signals. |
| **Sector Rotation** | The shifting of market leadership from one sector to another over time. |
| **Leadership Sector** | The sector with the highest average Trade Quality and Relative Strength. |
| **Lagging Sector** | The sector with the lowest average Trade Quality and Relative Strength. |
| **Market Narrative** | A 1–2 sentence institutional-style summary of current market conditions. |
| **Intelligence Feed** | Short, prioritized market insight messages displayed at the top of the scanner. |

### Regime & Regime Detection

| Term | Definition |
|------|------------|
| **Market Regime** | The current phase of market behavior (Trending Bullish, Trending Bearish, Consolidation, High Volatility, Sideways). |
| **Regime Transition** | A shift from one market regime to another (e.g., Consolidation → Trending Bullish). |
| **Regime Duration** | The number of consecutive bars the market has remained in its current regime. |
| **Trend Exhaustion** | When a prolonged trend shows signs of weakening momentum, suggesting a potential reversal. |
| **Volatility Expansion** | A shift from low-volatility to high-volatility conditions (ATR/Close > 3%). |
| **Volatility Compression** | Declining ATR relative to price, often preceding a breakout. |

### ML & Anomaly Detection

| Term | Definition |
|------|------------|
| **Isolation Forest** | An unsupervised ML algorithm that identifies anomalies by isolating data points in random trees. |
| **Anomaly Score** | A 0–100 score where higher values indicate more statistically unusual behavior. |
| **Anomaly Class** | Classification as either "Normal" or "Anomaly Detected." |
| **Volume Ratio** | Current volume divided by the 20-day average volume; values > 2 are considered unusual. |
| **ATR Ratio** | ATR divided by closing price; measures volatility relative to price level. |
| **Rate of Change (ROC)** | Percentage change in price over a specified number of periods. |
| **Contamination** | The expected proportion of anomalies in the dataset (set to 5% in our Isolation Forest). |
| **Feature Engineering** | The process of creating meaningful input variables (volume ratio, ATR ratio, ROC) from raw data. |

### Signal Reliability & Probability

| Term | Definition |
|------|------------|
| **Win Rate** | The percentage of historical setup occurrences that resulted in a positive return. |
| **Expectancy** | The average expected return per trade: (avg win × win rate) + (avg loss × loss rate). |
| **Forward Return** | The percentage price change over the N bars following a setup trigger. |
| **Reliability Label** | Classification of signal quality: High (≥65%), Moderate (≥50%), Low (<50%). |
| **Setup Probability** | The estimated likelihood of a setup succeeding, combining historical hit rate with factor adjustments. |
| **Confidence Band** | A range (probability ± 10%) representing uncertainty around the probability estimate. |
| **Factor Adjustment** | A modifier applied to the base probability based on momentum, volume, trend, or volatility. |
| **Expected Move** | The ATR-based projected price range over N days (ATR × √days). |

### Options & Derivatives

| Term | Definition |
|------|------------|
| **Black-Scholes Model** | A mathematical model for pricing European-style call and put options. |
| **European Option** | An option that can only be exercised at expiration (as opposed to American options). |
| **Call Option** | A contract giving the right to buy the underlying at the strike price. |
| **Put Option** | A contract giving the right to sell the underlying at the strike price. |
| **Strike Price** | The predetermined price at which an option can be exercised. |
| **ATM (At-The-Money)** | An option whose strike price equals the current stock price. |
| **ITM (In-The-Money)** | A call with strike below spot, or a put with strike above spot. |
| **OTM (Out-of-The-Money)** | A call with strike above spot, or a put with strike below spot. |
| **Time to Expiry (T)** | The remaining time until the option expires, expressed in years. |
| **Risk-Free Rate (r)** | The theoretical return of a zero-risk investment, used in option pricing. |
| **Delta (Δ)** | How much the option price changes per ₹1 move in the underlying. |
| **Gamma (Γ)** | How fast Delta changes per ₹1 move in the underlying. |
| **Vega (ν)** | How much the option price changes per 1% change in implied volatility. |
| **Theta (Θ)** | The daily time decay — how much value the option loses per day. |
| **Rho (ρ)** | How much the option price changes per 1% change in the risk-free rate. |
| **Implied Volatility (IV)** | The market's expectation of future volatility as implied by current option prices. |
| **Realized Volatility (RV)** | The actual observed volatility of returns over a historical period. |
| **IV Percentile** | Where the current IV stands relative to its historical range (0–100%). |
| **IV Regime** | Classification of the current IV level: Very Low, Low, Moderate, High. |
| **IV Smile / Skew** | The pattern of IV varying across different strike prices. |

### Derivatives Sentiment

| Term | Definition |
|------|------------|
| **Open Interest (OI)** | The total number of outstanding (unsettled) option or futures contracts. |
| **Put-Call Ratio (PCR)** | The ratio of put volume/OI to call volume/OI; PCR > 1 suggests bearish sentiment. |
| **Long Buildup** | Rising price + rising volume/OI — fresh buying positions being created. |
| **Short Buildup** | Falling price + rising volume/OI — fresh short positions being created. |
| **Short Covering** | Rising price + falling volume/OI — shorts exiting by buying back. |
| **Long Unwinding** | Falling price + falling volume/OI — longs exiting by selling. |
| **Max Pain** | The strike price where the total loss for option holders is maximized (price gravitates here near expiry). |
| **Gamma Zone** | Strike regions with high gamma exposure, where market maker hedging can amplify moves. |
| **OI Heatmap** | A visualization showing OI concentration across strikes and expiries. |

### Backtesting & Strategy

| Term | Definition |
|------|------------|
| **Backtest** | Simulating a trading strategy on historical data to evaluate its performance. |
| **Holding Period** | The number of bars a position is held before exiting. |
| **Stop Loss (SL)** | A predefined price level where a losing trade is automatically closed. |
| **Target** | A predefined price level where a winning trade is automatically closed. |
| **CAGR (Compound Annual Growth Rate)** | The annualized rate of return for an investment over a specified period. |
| **Sharpe Ratio** | Risk-adjusted return: (mean return − risk-free rate) / standard deviation of returns. |
| **Sortino Ratio** | Like Sharpe but only penalizes downside volatility, ignoring upside variance. |
| **Maximum Drawdown** | The largest peak-to-trough decline in portfolio value during a backtest. |
| **Profit Factor** | Gross profits divided by gross losses; values > 1 indicate a profitable strategy. |
| **Equity Curve** | A chart showing the cumulative growth of a portfolio over time. |
| **Trade Log** | A record of each trade's entry, exit, and return percentage. |

### Portfolio & Risk

| Term | Definition |
|------|------------|
| **Portfolio** | A collection of financial positions held by a trader. |
| **Position** | A single holding in a specific stock with quantity and average price. |
| **Exposure** | The total monetary value at risk across all positions. |
| **Sector Concentration** | The percentage of portfolio value allocated to a single sector. |
| **VaR (Value at Risk)** | The estimated maximum loss at a given confidence level (e.g., 95%) over one day. |
| **Portfolio Beta** | The sensitivity of portfolio returns to market (index) returns. |
| **Correlation Risk** | The risk from multiple positions moving together in the same direction. |
| **Position Sizing** | Determining how many shares to buy based on risk tolerance and stop loss distance. |
| **Risk-per-Trade** | The maximum percentage of capital risked on a single trade (typically 1–2%). |
| **Drawdown Probability** | The estimated likelihood of experiencing a given percentage loss. |

### Architecture & Platform

| Term | Definition |
|------|------------|
| **Streamlit** | A Python framework for building interactive web dashboards. |
| **Yahoo Finance (yfinance)** | A Python library for downloading historical market data from Yahoo Finance. |
| **Caching (st.cache_data)** | Storing computed results temporarily to avoid redundant API calls and recalculations. |
| **TTL (Time-to-Live)** | The duration a cached result remains valid before being refreshed (set to 600 seconds). |
| **Graceful Degradation** | The ability of the system to continue working partially when individual modules fail. |
| **Debug Mode** | A sidebar toggle that reveals scanner logs, failed tickers, and raw diagnostics. |
| **Scanner Pipeline** | The sequential process of fetching, computing, scoring, and ranking stocks. |
| **Module** | A self-contained Python file implementing a specific analytical capability. |
| **NIFTY 50** | The benchmark index of the 50 largest Indian stocks listed on the National Stock Exchange. |
| **NSE (National Stock Exchange)** | India's largest stock exchange by trading volume. |
| **BSE (Bombay Stock Exchange)** | India's oldest stock exchange. |
