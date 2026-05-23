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

*Everything you need to start using the app in under 5 minutes — even if you've never traded a stock before.*

---

## 1. Quick Start — For First-Time Users

### What Is This App? (In One Sentence)

**This app is like a doctor's check-up for any Indian stock** — it examines the stock from every angle (price trends, AI analysis, derivatives data, historical testing) and gives you a clear health report so you can decide whether to buy, sell, or wait.

### What Does It Actually Do?

Think of it as a **personal stock research assistant** that does in 2 minutes what would normally take a professional analyst 2 hours:

| What YOU want to know | What THE APP tells you |
|---|---|
| "Is this stock going up or down?" | 🟢 **Bullish** / 🔴 **Bearish** / 🟡 **Neutral** signal |
| "Should I actually trust this signal?" | A **probability score** like 67% — meaning this type of setup has worked 67 out of 100 times in the past |
| "Is anything weird happening?" | An **anomaly alert** if volume or volatility is unusually high |
| "What phase is the market in?" | A **regime label** like "Trending Bullish" or "Consolidation" |
| "Are big traders buying or selling?" | **Derivatives sentiment** — Long Buildup (buying) or Short Buildup (selling) |
| "Which stock should I look at today?" | The **Market Scanner** ranks all 50 NIFTY stocks and shows you the top 3 |

### Who Is It For?

- ✅ **Complete beginners** who want to understand stocks using data instead of tips
- ✅ **Active traders** who want faster, more confident decisions
- ✅ **Swing traders** who need a daily scan of the best opportunities
- ✅ **Investors** who want to time their entries better
- ✅ **Anyone** who is tired of guessing and wants numbers behind their decisions

### How to Launch (Step by Step)

1. **Open a terminal / command prompt** on your computer
   - On Windows: Press `Win + R`, type `cmd`, press Enter
   - On Mac/Linux: Open the "Terminal" application
2. **Navigate to the project folder:**
   ```
   cd "Indian Market & Derivatives Intelligence Terminal"
   ```
3. **Start the app:**
   ```
   streamlit run app.py
   ```
4. Your web browser opens automatically at `http://localhost:8501`
5. You'll see the dashboard — **you're ready to go!**

> 💡 **Tip:** If this is your first time, make sure you've already installed the required packages by running `pip install -r requirements.txt` before Step 3.

### The Two Modes — Which One Should I Pick?

When the app loads, you'll see a **sidebar on the left** with a radio button to choose your mode:

| Mode | When to use it | Analogy |
|------|---------------|---------|
| **Single Stock Analysis** | When you already have a stock in mind and want a deep analysis | Like getting a full medical check-up for one patient |
| **Market Scanner** | When you want to find the best stocks to trade today | Like screening 50 patients and finding the healthiest ones |

**If you're new, start with Single Stock Analysis** — type `RELIANCE.NS` and explore.

---

## 2. Complete Beginner Walkthrough

### Part A — Using Single Stock Analysis (Screen by Screen)

Here is exactly what you'll see on your screen, section by section, from top to bottom.

---

#### 🔎 Step 1 — Search for a Stock (Sidebar)

**What you see:** A text input box at the top of the sidebar that says *"Search Ticker/Company (e.g. RELIANCE, TCS, HDFC)"*.

**What to do:** Start typing. You can type either:
- A **ticker symbol** like `TCS` or `SBIN`
- A **company name** like `Tata` or `State Bank`

**What happens:** A dropdown appears below the text box showing matching stocks. For example:

| You type | Dropdown shows |
|----------|---------------|
| `rel` | `RELIANCE.NS - Reliance Industries Limited` |
| `tcs` | `TCS.NS - Tata Consultancy Services Limited` |
| `hdfc` | `HDFCBANK.NS - HDFC Bank Limited`, `HDFCLIFE.NS - HDFC Life Insurance Company Limited` |
| `state` | `SBIN.NS - State Bank of India` |
| `infosys` | `INFY.NS - Infosys Limited` |
| `tata` | `TATAMOTORS.NS - Tata Motors Limited`, `TATASTEEL.NS - Tata Steel Limited` |
| `bajaj` | `BAJFINANCE.NS - Bajaj Finance Limited`, `BAJAJFINSV.NS - Bajaj Finserv Limited`, `BAJAJ-AUTO.NS - Bajaj Auto Limited` |
| `pharma` | `SUNPHARMA.NS - Sun Pharmaceutical Industries Limited` |

Click on the stock you want. The ticker gets selected automatically.

> 💡 **Tip:** You don't need to remember ticker codes! Typing any part of the company name works. Typing `bank` shows all banking stocks.

**Below the search box**, you'll see a dropdown for **Historical Period**:

| Period | Meaning | Best for |
|--------|---------|----------|
| `1mo` | Last 1 month of data | Very short-term trades |
| `3mo` | Last 3 months | Short-term swing trading |
| `6mo` | Last 6 months | Medium-term analysis |
| `1y` | Last 1 year *(default)* | Most common for swing trading |
| `2y` | Last 2 years | Long-term trend analysis |

**Recommendation for beginners:** Leave it at `1y` (1 year). This gives enough history for reliable analysis.

---

#### 📋 Step 2 — Read the AI Market Intelligence Summary (First Thing on Screen)

**What you see:** A redesigned glassmorphism-styled summary with three sections:

**Section 1 — Signal Badge + Key Metrics (side by side):**

On the **left**, you see a large colored badge showing the signal:

| Signal | Color | Meaning |
|--------|-------|---------|
| 🟢 **Strong Bullish** | Green | Very strong buy signal — ML models agree |
| 🔵 **Bullish Continuation** | Cyan | Uptrend likely to continue — trend is aligned |
| 🟡 **Weak Bullish** | Light green | Mild bullish lean but trend structure is weak |
| 🟡 **Neutral / Consolidation** | Yellow | No clear direction — wait for breakout |
| 🟠 **Weak Bearish** | Light red | Mild bearish lean, not strong enough to short |
| 🔴 **Bearish Breakdown** | Red | Downtrend with trend confirmation |
| 🔴 **Strong Bearish** | Dark red | Very strong sell signal — ML models agree |
| ⚠ **High Volatility / Uncertain** | Purple | Anomaly detected + high volatility — avoid trading |

Below the badge you'll see whether the signal was generated by the **ML Ensemble** (machine learning) or **Rule-Based** fallback engine.

On the **right**, a metrics panel shows:

| Metric | Example | What it tells you |
|--------|---------|-------------------|
| Bias | Strong Bullish | The overall directional bias |
| Confidence | 72% | How confident the ML models are (with animated progress bar) |
| Momentum | Strong | Whether momentum supports the signal |
| Volatility | Stable | Current volatility regime |
| Risk Level | Low / Moderate / High | Overall risk assessment |
| Regime | Trending Bullish | What phase the market is in |

**Section 2 — AI Key Insight (the blue card below):**

This is the most important part — a **plain-English paragraph** that explains:
- What the current situation is (e.g., "RELIANCE shows strong bullish momentum at ₹2,845.30 with 72% confidence")
- **Best Use Case** — exactly what to do (e.g., "Momentum swing trading, 3-5 day hold")
- **Warning** — what risk to watch (e.g., "Elevated volatility — consider wider stop losses")

**Section 3 — Secondary Metric Pills (5 small cards):**

| Pill | Example | What it tells you |
|------|---------|-------------------|
| Win Rate | 64.3% | How often this setup has worked historically |
| Probability | 67% | Estimated chance of success right now |
| IV Regime | Moderate IV | Whether options are cheap or expensive |
| Derivatives | Bullish | Derivatives sentiment direction |
| Exp. Move | ±2.8% | Expected 5-day price movement |

> 🧠 **How to read the new summary in 5 seconds:**
> 1. Look at the **signal badge color** — green = bullish, red = bearish, yellow = wait
> 2. Read the **AI Key Insight** paragraph — it tells you everything in plain English
> 3. Check the **confidence bar** — above 60% = worth acting on, below 45% = weak

---

#### 📊 Step 3 — Look at the Chart

**What you see:** A large interactive candlestick chart with colored lines overlaid.

**How to read it (for absolute beginners):**

| Element | What it looks like | What it means |
|---------|-------------------|---------------|
| **Green candle** | A green rectangle | Price went UP during that day — the stock closed higher than it opened |
| **Red candle** | A red rectangle | Price went DOWN during that day — the stock closed lower than it opened |
| **Thin lines (wicks)** | Lines sticking out above/below each candle | The highest and lowest prices reached during the day |
| **Blue line (SMA20)** | A smooth blue line | The average closing price over the last 20 days — shows short-term trend |
| **Orange line (SMA50)** | A smooth orange line | The average closing price over the last 50 days — shows medium-term trend |
| **Gray bands (Bollinger)** | Two gray lines forming a channel | A "normal range" — if price touches the upper band, it may be overbought; lower band, oversold |

> 💡 **Simple rule:** If the blue line (SMA20) is ABOVE the orange line (SMA50) and both are going up → the stock is in an **uptrend**. If below and going down → **downtrend**.

---

#### ⚡ Step 4 — Check the ML Signal & AI Recommendation

**What you see:** Two side-by-side panels.

**Left panel — ML Signal Engine:**
A rich signal card showing:
- The **7-class signal** (e.g., "Strong Bullish", "Bearish Breakdown", "Neutral / Consolidation")
- **Confidence bar** with percentage (animated fill)
- **Probability breakdown** showing bullish / neutral / bearish percentages (e.g., ▲ 68% ● 22% ▼ 10%)
- **Model Agreement** — how much the two ML models (RandomForest and GradientBoosting) agree
- Badge showing whether it's **ML Ensemble** or **Rule-Based** (fallback for stocks with limited data)

**Right panel — AI Recommendation:**
A narrative paragraph generated by the AI Narrator, like:
> *"RELIANCE shows strong bullish momentum at ₹2,845.30 with 72% confidence. The setup is supported by RSI momentum direction, trend structure, and volume expansion. Derivatives positioning (Long Buildup) confirms the directional bias."*
>
> *📌 Best Use Case: Momentum swing trading (3-5 day hold)*
>
> *⚠ Monitor for regime change and volume confirmation.*

You can also expand the **"Signal Contributing Factors"** section to see exactly which features drove the ML signal:

| Factor | Importance | Impact | Detail |
|--------|-----------|--------|--------|
| RSI Momentum Direction | 12.3% | 🟢 Positive | RSI rising over last 5 bars (+8.2) |
| Trend Structure | 10.8% | 🟢 Positive | SMA20 1.023× above SMA50 |
| Volume Expansion | 9.4% | 🟢 Positive | Volume 1.8× above 20-day average |
| Volatility Level | 7.1% | 🔴 Negative | ATR at 2.9% of price — high |
| 5-Day Momentum | 6.8% | 🟢 Positive | +4.2% over 5 days |

> 💡 **What's new in Phase 5:** The old signal engine was rule-based (simple if/else scoring). The new ML engine uses machine learning trained on your stock's own price history to learn patterns, making signals much more accurate and less biased toward "Neutral".

**Example — What a recommendation looks like for different signals:**

| Signal | Example recommendation |
|--------|----------------------|
| 🟢 Bullish | "Bullish trend continuation detected. Price above SMA20 and SMA50 with strong volume. Consider entering a long position with a 3% stop loss." |
| 🔴 Bearish | "Bearish momentum building. RSI declining below 45 with price below SMA20. Avoid fresh longs. Consider booking profits if already holding." |
| 🟡 Neutral | "Market is consolidating. No strong directional cues. Wait for a breakout above Bollinger Upper or breakdown below Bollinger Lower before acting." |

---

#### 🤖 Step 5 — Review the AI Intelligence Panel

**What you see:** Three cards in a row, followed by two more cards below.

**Card 1 — 🔬 Anomaly Detection**

| What it shows | Example | What it means in plain English |
|--------------|---------|-------------------------------|
| Anomaly Class | **Normal** | "Nothing unusual is happening. The stock is behaving as expected." |
| Anomaly Class | **Anomaly Detected** | "Something unusual is happening — maybe volume spiked 3x, or the price moved way more than normal. Investigate!" |
| Anomaly Score | 23 | A number from 0 to 100. Higher = more unusual. Below 50 is usually normal. |

> 🏥 **Analogy:** It's like a smoke detector. "Normal" = no smoke. "Anomaly Detected" = smoke detected — go check if there's a fire (it might just be toast).

**Card 2 — 🌡️ Regime Detection**

| Regime shown | What it means | What you should do |
|-------------|---------------|-------------------|
| **Trending Bullish** | Stock has been going up steadily | Good for buying dips (pullback entries) |
| **Trending Bearish** | Stock has been going down steadily | Avoid buying. Wait for reversal signals |
| **Consolidation** | Stock is moving sideways in a narrow range | Wait for a breakout before acting |
| **High Volatility Expansion** | Big swings in both directions | Use wider stop losses. Trade smaller sizes |
| **Sideways** | No clear trend, random movement | Best to skip this stock and find a trending one |

It also shows if a **transition** just happened (e.g., "Consolidation → Trending Bullish"). Transitions are valuable because they signal a new phase is beginning.

> 🏥 **Analogy:** Think of it like weather forecasting. "Trending Bullish" = sunny weather, great for outdoor plans. "High Volatility" = storm warning, stay cautious.

**Card 3 — 📊 Signal Reliability**

| What it shows | Example | What it means |
|--------------|---------|---------------|
| Win Rate | **64.3%** | "Out of all the times this type of setup appeared in the past, 64.3% of them made money" |
| Explanation | "Trend Continuation setups have historically delivered positive returns 64% of the time with an average gain of 1.8%." | Full context about how reliable this setup has been |

> 🏥 **Analogy:** It's like checking a restaurant's rating before eating there. Win Rate 65%+ = "this restaurant usually delivers good food." Below 50% = "mixed reviews — proceed with caution."

**Card 4 — 🎯 Setup Probability**

| What it shows | Example | What it means |
|--------------|---------|---------------|
| Success Probability | **67%** | "Based on history AND current conditions, there's about a 67% chance this trade works" |
| Confidence Band | 57% – 77% | "The true probability is likely somewhere in this range" |
| Explanation | "Base hit rate 60% + volume confirmation (+3%) + trend alignment (+4%) = 67%" | How the app calculated the number |

> 💡 **Key difference:** Win Rate looks at history alone. Probability adjusts for what's happening RIGHT NOW (volume, momentum, trend strength). Probability is more useful for your current decision.

**Card 5 — 📐 Expected Move**

| What it shows | Example | What it means |
|--------------|---------|---------------|
| Move Range | **±2.8%** | "Over the next 5 trading days, the stock is expected to move about 2.8% up or down" |

This helps you set realistic stop losses and targets.

---

#### 📌 Step 6 — Check Options & Derivatives Intelligence

**What you see:** Three cards in a row (IV Analysis, Option Pricing, Greeks), then two cards below (Derivatives Sentiment, Max Pain).

**Don't panic if these terms are new.** Here's what matters for a beginner:

**IV Analysis (Most Important for Beginners):**

| What it shows | Example | Plain English |
|--------------|---------|---------------|
| IV Estimate | 28.5% | "The market expects this stock to move about 28.5% per year" |
| IV Percentile | 72% | "Options are more expensive than usual (72% of the time in the past year, options were cheaper than today)" |
| IV Regime | Moderate IV | A label: Very Low / Low / Moderate / High |

> 💡 **Simple rule:** IV Percentile above 80% = options are expensive (good time to sell options). Below 20% = options are cheap (good time to buy options). In between = normal.

**Derivatives Sentiment (Very Useful):**

| What it shows | Example | Plain English |
|--------------|---------|---------------|
| Sentiment | Bullish | "Overall derivatives data supports a bullish view" |
| PCR Proxy | 0.85 | Put-Call Ratio — below 1 is bullish, above 1 is bearish |
| OI Buildup | Long Buildup | "Big traders are adding new buying positions" |
| Max Pain | ₹2,800 | "The price where option sellers lose the least — price often gravitates here near expiry" |

**The four types of OI Buildup explained with examples:**

| Buildup type | What's happening | Real-world analogy |
|-------------|-----------------|-------------------|
| **Long Buildup** | Price rising + new positions being created | "People are buying concert tickets because they expect the show to be great" |
| **Short Buildup** | Price falling + new positions being created | "People are betting against the concert — they think it'll be cancelled" |
| **Short Covering** | Price rising + positions being closed | "People who bet against the concert are now panicking and buying tickets" |
| **Long Unwinding** | Price falling + positions being closed | "People who bought tickets are selling them — they've lost confidence" |

---

#### 🧪 Step 7 — Run a Backtest

**What you see:** An expandable section titled "Run Backtest for Current Setup." Click to open it.

**What you'll configure:**

| Setting | What it means | Example | Recommendation |
|---------|--------------|---------|----------------|
| Holding Period | How many days to hold the trade | 5 bars | 5–10 for swing trading |
| Stop Loss % | Maximum loss before auto-exit | 3% | 2–4% for most stocks |
| Target % | Profit target before auto-exit | 5% | 4–8% for swing trades |

**What you'll see after running:**

| Metric | Example | What it means in plain English |
|--------|---------|-------------------------------|
| Total Trades | 23 | "The app found 23 instances of this setup in the past year" |
| Win Rate | 60.9% | "14 out of 23 trades were profitable" |
| Avg Return | 1.45% | "On average, each trade made 1.45% profit" |
| Sharpe Ratio | 1.32 | "The risk-adjusted return is good (above 1.0 is decent, above 2.0 is excellent)" |
| Max Drawdown | -8.2% | "The worst losing streak resulted in an 8.2% drop from peak" |
| Expectancy | 0.72% | "On average, you can expect to make 0.72% per trade over many trades" |
| Profit Factor | 1.85 | "For every ₹1 lost, you gained ₹1.85. Above 1.0 means profitable." |
| Sortino Ratio | 1.65 | "Like Sharpe, but only penalizes downside — higher is better" |

> 💡 **The one number that matters most:** If **Win Rate > 50%** AND **Profit Factor > 1.0** AND **Expectancy > 0** → the strategy has historically been profitable. Not guaranteed to work in the future, but it's a positive sign.

---

#### 📂 Step 8 — Raw Data (Optional)

**What you see:** A table showing the last 20 days of raw price data (Open, High, Low, Close, Volume).

This is for advanced users who want to verify the numbers themselves. **Beginners can skip this section entirely.**

---

### Part B — Using Market Scanner (Screen by Screen)

#### 🔎 Step 1 — Switch to Market Scanner

In the sidebar, click "Market Scanner" in the mode selector. Then pick a scan period (e.g., `6mo`).

You'll also see a checkbox: **"Scanner Debug Mode"**. Leave this OFF unless something goes wrong.

#### ⏳ Step 2 — Wait for the Scan

You'll see a spinner saying "Scanning market..." — this takes 30–90 seconds.

**What's happening behind the scenes:** The app is downloading data for all 50 NIFTY stocks, computing 10+ indicators for each one, running anomaly detection on each one, classifying regimes, scoring each stock, and ranking them. All automatically.

#### 📡 Step 3 — Read the Intelligence Feed

**What you see:** 2–4 short messages at the top in quote boxes. Examples:

> 📈 *"Market participation healthy at 62% — broad-based strength."*

> ⚠ *"Sector leadership concentrated in Financial Services. IT sector lagging."*

> 🔄 *"Breadth divergence detected — index rising but majority of stocks bearish."*

**What these mean:**

| Message type | What it tells you |
|-------------|-------------------|
| "Participation at 62%" | 62% of the 50 stocks have decent setups — the market is broadly strong |
| "Participation at 22%" | Only 22% have decent setups — strength is concentrated in a few stocks, be careful |
| "Sector leadership in Financials" | Bank/finance stocks are performing best right now |
| "Breadth divergence" | The NIFTY index is going up, but most individual stocks are going down — this is a warning sign |

#### 📊 Step 4 — Check Breadth Metrics

**What you see:** Four cards showing:

| Metric | Example | What it means |
|--------|---------|---------------|
| Advancing / Declining | 32 / 18 | "32 stocks are bullish, 18 are bearish" |
| Bullish % | 64% | "64% of scanned stocks show bullish signals" |
| Bearish % | 36% | "36% of scanned stocks show bearish signals" |
| Participation | 58% | "58% of stocks have trade quality above 5.0 — meaning more than half the market has reasonable setups" |

> 💡 **Simple interpretation:** Bullish % above 60% = strong market. Below 40% = weak market. In between = mixed.

#### 🏆 Step 5 — Check Top 3 Opportunities

**What you see:** Three card-style panels showing the best-ranked stocks. Example:

| Card | Stock | Score | Conviction | Setup | Regime |
|------|-------|-------|-----------|-------|--------|
| #1 | BAJFINANCE.NS | 8.4 | ⭐⭐⭐⭐ Elite | Breakout | Trending Bullish |
| #2 | TATAMOTORS.NS | 7.6 | ⭐⭐⭐ High | Trend Continuation | Trending Bullish |
| #3 | SUNPHARMA.NS | 7.1 | ⭐⭐⭐ High | Pullback | Trending Bullish |

**How to use this:** The #1 stock has the strongest overall setup. Consider switching to Single Stock Analysis to analyze it in detail before trading.

#### 🛠️ Step 6 — Filter and Explore

**What you see:** Three dropdown filters + four tabs.

**Filters:**

| Filter | Use it to... | Example |
|--------|-------------|---------|
| Sector | See only stocks from one sector | "Financial Services" to see only bank stocks |
| Setup Type | See only stocks with a specific pattern | "Breakout" to see only stocks breaking out |
| Regime | See only stocks in a specific market phase | "Trending Bullish" to see only stocks in uptrends |

**Tabs:**

| Tab | What it shows |
|-----|--------------|
| **All Opportunities** | Every scanned stock, ranked by score |
| **Bullish Setups** | Only stocks with bullish signals |
| **Bearish Setups** | Only stocks with bearish signals |
| **Anomalies** | Only stocks where something unusual is happening |

> 💡 **Beginner tip:** Start with the "Bullish Setups" tab if you want to buy, or the "Anomalies" tab to find interesting situations.

---

## 3. Real End-to-End Examples

### Example 1: RELIANCE.NS — A Strong Buy Setup

**Scenario:** You type `rel` in the sidebar. The dropdown shows `RELIANCE.NS - Reliance Industries Limited`. You select it.

**What the AI Summary shows:**

| Section | What you see | What it means |
|---------|-------------|---------------|
| **Signal Badge** | 🟢 **Strong Bullish** (ML Ensemble) | The ML engine is confident this stock is going up |
| **Confidence** | 72% (green bar) | High confidence — both ML models agree |
| **Momentum** | Strong | Multiple momentum indicators confirm the move |
| **Risk Level** | Low | Few risk factors present |
| **Regime** | Trending Bullish | The stock has been going up for a while |

**AI Key Insight:**
> *"RELIANCE shows strong bullish momentum at ₹2,845.30 with 72% confidence. The setup is supported by RSI momentum direction, trend structure, and volume expansion. Derivatives positioning (Long Buildup) and trending bullish regime confirm the directional bias."*
>
> *📌 Best Use Case: Momentum swing trading (3-5 day hold)*
>
> *⚠ Monitor for regime change and volume confirmation.*

**Secondary Pills:** Win Rate 64.3% | Probability 67% | IV Moderate | Derivatives Bullish | Exp. Move ±2.8%

**What you'd check next:**

1. **Contributing Factors** — Expand to see which ML features drove the signal (RSI rising, volume expanding, trend aligned)
2. **Chart** — Confirm the uptrend visually: green candles, SMA20 above SMA50, price above both
3. **Backtest** — Set 3% stop loss, 5% target, 5-day holding. See if Win Rate > 55% and Profit Factor > 1.0
4. **AI Recommendation** — The narrative already gives you a specific trading strategy

**Decision:** "ML Signal is Strong Bullish with 72% confidence, probability is 67%, derivatives confirm Long Buildup, anomaly is Normal. The contributing factors show RSI momentum, trend structure, and volume are all positive. I'll enter with a 3% stop loss below today's low."

---

### Example 2: TCS.NS — A Watchlist Situation

**Scenario:** You type `tcs`, select `TCS.NS - Tata Consultancy Services Limited`.

**What the Executive Summary shows:**

| Card | Value | What it means for you |
|------|-------|----------------------|
| Signal | 🟡 **Neutral** | No strong direction — the app can't confidently say buy or sell |
| Regime | **Consolidation** | The stock is stuck in a narrow range, moving sideways |
| Setup | **Consolidation** | Tight price range — a breakout (up or down) may happen soon |
| Probability | **48%** | Nearly a coin flip — not great odds for a trade |
| Anomaly | ⚠ **Anomaly Detected** | Volume is unusually high for a stock that's going nowhere — something might be brewing |
| OI Buildup | **Long Buildup** | Despite the flat price, someone is quietly accumulating buy positions |

**What this means:** The stock itself isn't moving, but two things are interesting: (1) the anomaly alert says volume is unusual, and (2) OI shows long buildup. This might mean big players are positioning for an upside breakout.

**Decision:** "I won't buy yet because the signal is Neutral and probability is only 48%. But I'll add TCS to my watchlist. If the signal turns Bullish and price breaks above the Bollinger Upper Band, I'll re-analyze."

---

### Example 3: HDFCBANK.NS — A Clear Avoid

**Scenario:** You type `hdfc`, select `HDFCBANK.NS - HDFC Bank Limited`.

**What the Executive Summary shows:**

| Card | Value | What it means for you |
|------|-------|----------------------|
| Signal | 🔴 **Bearish** | The app thinks the stock is likely to go down |
| Regime | **Trending Bearish** | The stock has been falling consistently |
| Setup | **Trend Continuation** | The downtrend looks like it will continue |
| Probability | **38%** | Only a 38% chance of a bounce — history says this usually keeps falling |
| Derivatives | **Bearish** | Derivatives data agrees — bearish positioning |
| OI Buildup | **Short Buildup** | Big traders are opening new short (sell) positions |

**Decision:** "Everything lines up bearish — signal, regime, derivatives, OI buildup. Probability of a recovery is only 38%. I'll stay away from buying this stock right now. I might look for a short opportunity or simply focus on other stocks."

---

### Example 4: INFY.NS — A Full Deep-Dive Walkthrough

This example walks through EVERY section of the dashboard, exactly as you would see it.

**Scenario:** You type `infosys`, select `INFY.NS - Infosys Limited`, period = 1 year.

**📋 Executive Summary:**

| Card | Value |
|------|-------|
| Current Price | ₹1,565.80 |
| Signal | 🟢 Bullish |
| Regime | Trending Bullish |
| Trade Quality | 6.8 |
| Setup | Pullback |
| Win Rate | 61.5% |
| Probability | 63% |
| IV Regime | Low IV |
| Derivatives | Bullish |
| OI Buildup | Short Covering |
| Anomaly | Normal |
| Expected Move | ±2.1% |

*First impression: Bullish signal with 63% probability. Setup is a Pullback in an uptrend — this is a classic buy-the-dip situation.*

**📊 Chart observations:**
- Price is above SMA20 and SMA50 — uptrend confirmed
- Price recently dipped to touch SMA20 — this is the "pullback"
- Price is bouncing back up from SMA20 — the dip is being bought

**⚡ Signal & Recommendation:**
- Signal: "Bullish" with 0.72 confidence
- Recommendation: "Pullback to moving average in uptrend. Price holding SMA20 support with RSI recovering from 42 to 55. Consider long entry near current levels with stop loss below SMA50."

**🤖 AI Intelligence:**
- Anomaly: Normal (score 18) — "No unusual patterns detected"
- Regime: "Trending Bullish" for 45 bars — stable, long-running uptrend
- Reliability: Win rate 61.5% — "Pullback setups in Infosys have worked about 6 out of 10 times"
- Probability: 63% — "Base rate 58% + volume recovery (+2%) + trend alignment (+3%)"
- Expected Move: ±2.1% over 5 days

**📌 Options & Derivatives:**
- IV: 22.3% (IV Percentile 28%) — options are cheap right now
- OI Buildup: Short Covering — "Traders who bet against Infosys are buying back, driving the price up"
- Max Pain: ₹1,550 — price is slightly above max pain, supportive

**🧪 Backtest (5-day hold, 3% SL, 5% target):**
- Total Trades: 18
- Win Rate: 61.1%
- Sharpe: 1.15
- Max Drawdown: -6.8%
- Expectancy: 0.65%
- Profit Factor: 1.62

**Final Decision:**
"This is a solid pullback entry in an established uptrend. Signal is bullish (63% probability), the dip is being bought, short covering confirms, options are cheap (good for buying calls if interested). Backtest shows 61% win rate with 1.62 profit factor. I'll buy near ₹1,565 with a stop loss at ₹1,520 (below SMA50) and a target of ₹1,640 (about 5% up)."

---

## 4. Daily Workflow — How a Trader Uses the App

### The 2-Minute Morning Routine

Here's exactly what an experienced user does every morning:

| Step | Action | What you're looking for | Time |
|------|--------|------------------------|------|
| 1 | Open app → **Market Scanner** mode | — | 10 sec |
| 2 | Read the **Intelligence Feed** | "Is the market broadly strong or weak today?" | 15 sec |
| 3 | Check **Breadth Metrics** | "Are most stocks bullish (>60%) or bearish?" | 10 sec |
| 4 | Look at **Top 3 Opportunities** | "Which stocks have the highest scores?" | 15 sec |
| 5 | Filter by your sector if needed | "What's the best IT stock? Best bank stock?" | 5 sec |
| 6 | Switch to **Single Stock Analysis** for the top pick | — | 10 sec |
| 7 | Read the **Executive Summary** | "Signal + Probability + Derivatives — do they agree?" | 15 sec |
| 8 | Check **Probability & Reliability** | "Is this above 55%? Has this setup worked before?" | 10 sec |
| 9 | Check **Derivatives Sentiment** | "Does OI buildup confirm? Is it Long Buildup or Short Buildup?" | 10 sec |
| 10 | Run a **Backtest** | "Win Rate > 50%? Profit Factor > 1.0? Positive Expectancy?" | 15 sec |
| 11 | Make your decision | Buy / Sell / Wait / Add to Watchlist | — |

**Total time: ~2 minutes.**

### Decision Checklist

Before making any trade, check these 5 boxes:

- [ ] **Signal is Bullish or Bearish** (not Neutral — Neutral means "wait")
- [ ] **Probability is above 55%** (below 50% is a coin flip)
- [ ] **Derivatives sentiment agrees** with the signal direction
- [ ] **Backtest Win Rate is above 50%** and Profit Factor above 1.0
- [ ] **Anomaly status is Normal** (if Anomaly Detected, investigate before acting)

If all 5 check out → high-confidence trade.
If 3–4 check out → moderate confidence, use smaller position size.
If fewer than 3 → skip this stock, find a better one.

---

## 5. Understanding Colors, Signals & Icons

### Signal Colors

| Color / Icon | Meaning | What to do |
|-------------|---------|-----------|
| 🟢 **Bullish** | Indicators point upward — potential buy opportunity | Consider buying if probability is also above 55% |
| 🔴 **Bearish** | Indicators point downward — potential sell or avoid | Avoid buying. If you already own the stock, consider exiting |
| 🟡 **Neutral** | No strong direction — wait for clarity | Do nothing. Add to watchlist and check again tomorrow |

### Conviction Levels (Scanner Only)

| Level | Score | What it means | What to do |
|-------|-------|---------------|-----------|
| ⭐⭐⭐⭐ **Elite Setup** | 8.0+ | Best-of-the-best opportunity | Analyze immediately — these are rare |
| ⭐⭐⭐ **High Conviction** | 6.5–7.9 | Strong opportunity worth acting on | Prioritize for deep-dive analysis |
| ⭐⭐ **Moderate** | 5.0–6.4 | Decent setup but not the strongest | Analyze only if no Elite/High options exist |
| ⭐ **Weak** | Below 5.0 | Poor alignment — better opportunities exist | Skip — look for higher-ranked stocks |

### Probability Scores

| Range | Label | What it means | Example analogy |
|-------|-------|---------------|----------------|
| 70%+ | ✅ High Probability | History strongly supports this setup | "This restaurant has a 4.5-star rating — very likely to be good" |
| 50–69% | ⚠ Moderate Probability | Reasonable but not certain | "3.5 stars — probably fine, but don't get your hopes too high" |
| Below 50% | ❌ Low Probability | History suggests this setup often fails | "2 stars — most people had a bad experience here" |

### Anomaly Alerts

| Status | What it means | What to do |
|--------|---------------|-----------|
| **Normal** | Price action is within historical norms | Proceed with your analysis normally |
| **Anomaly Detected** | Something statistically rare is happening | Investigate WHY — check volume, news, events. Don't trade blindly on anomalies |

> ⚠ **Important:** Anomalies are NOT buy/sell signals. They are "something unusual is happening — pay attention" alerts. An anomaly could mean a great opportunity OR a dangerous trap. Always investigate.

### Risk & Reliability Labels

| Label | Win Rate | What it means | What to do |
|-------|----------|---------------|-----------|
| ✅ **High Reliability** | 65%+ | This setup type usually works | Trade with normal confidence |
| ⚠ **Moderate Reliability** | 50–65% | Works more often than not, but not consistently | Use smaller position sizes or wait for additional confirmation |
| ❌ **Low Reliability** | Below 50% | This setup frequently fails | Avoid this setup or wait for much stronger confirmation |

---

## 6. AI & ML — Explained Simply

The app uses four "smart engines" behind the scenes. Here's what each one does in plain English, with real-world analogies:

### 🔬 Anomaly Detection

**What it does:** Examines three things — volume, volatility, and momentum — and compares today's values to the last 3–6 months. If today looks very different from "normal," it raises an alert.

**Real-world analogy:** Imagine you track how many customers visit your shop each day. You normally get 100 visitors. One day, 350 visitors show up. That's an anomaly. It might be great (sale going viral) or bad (a flash mob causing chaos). Either way, you need to pay attention.

**Example in the app:**
- TATASTEEL.NS normally trades 5 million shares per day
- Today it traded 18 million shares — 3.6× normal
- The anomaly engine flags: "Anomaly Detected — Score 78"
- **Your action:** Check if there's news (earnings, government policy, merger). The anomaly itself doesn't tell you the direction — just that something is happening.

### 🌡️ Regime Detection

**What it does:** Looks at the trend direction (moving averages), volatility (ATR), and momentum (RSI) to classify the market into one of five phases.

**Real-world analogy:** Think of seasons. A farmer needs to know whether it's planting season (Trending Bullish), harvest season (may be nearing the top), or winter (Trending Bearish). You use different strategies in different seasons.

**Example in the app:**
- MARUTI.NS shows SMA20 > SMA50 and both rising, RSI is 62, ATR is moderate
- Regime: "Trending Bullish" (has been in this regime for 38 bars)
- **Your action:** In Trending Bullish, look for pullback entries (buy dips). Avoid selling short.

### 📊 Signal Reliability

**What it does:** Looks backward through 6–12 months of data, finds every time the same setup type appeared, and counts how many of those led to a profit within 5 days.

**Real-world analogy:** Before trying a new restaurant, you read reviews. "147 people tried this dish; 94 liked it (64% approval)." That's exactly what signal reliability does for trading setups.

**Example in the app:**
- Setup type: "Breakout"
- The app found 21 past breakout setups in BAJFINANCE.NS over the last year
- 14 of those 21 were profitable within 5 days
- Win Rate: 66.7%
- **Your action:** A 66.7% win rate is solid. This setup type is reliable for this stock.

### 🎯 Probability Engine

**What it does:** Starts with the historical win rate and then adjusts it based on what's happening right now:
- Is volume above average? (+2–3% boost)
- Is the trend strong? (+2–4% boost)
- Is momentum aligned? (+1–3% boost)
- Is volatility normal? (no adjustment or small penalty)

**Real-world analogy:** A weather forecast starts with the historical average ("July in Delhi is usually hot") and adjusts based on current conditions ("but today there's cloud cover, so it'll be slightly cooler"). The probability engine does the same for stock setups.

**Example in the app:**
- Base win rate for Pullback setups: 58%
- Current volume is 1.5× average: +3%
- SMA20 > SMA50 and both rising: +4%
- RSI at 55 (healthy, not overbought): +2%
- Final probability: 67%
- Confidence band: 57% – 77%
- **Your action:** 67% is well above the 55% minimum threshold. This is a trade worth taking.

---

## 7. What Should I Look At First?

### If You're Overwhelmed — The Priority Pyramid

```
                    ┌─────────┐
                    │ SIGNAL  │  ← Look at this FIRST
                    │  + PROB │     (5 seconds)
                   ┌┴─────────┴┐
                   │ DERIVATIVES│  ← Does smart money agree?
                   │ SENTIMENT  │     (10 seconds)
                  ┌┴────────────┴┐
                  │   BACKTEST    │  ← Has this worked before?
                  │   RESULTS    │     (15 seconds)
                 ┌┴──────────────┴┐
                 │  CHART + REGIME │  ← Visual confirmation
                 │  + INDICATORS   │     (30 seconds)
                ┌┴────────────────┴┐
                │ OPTIONS + RAW DATA│  ← Deep dive (optional)
                └──────────────────┘
```

### For Single Stock Analysis

| Priority | Section | Time needed | What to look for |
|----------|---------|-------------|-----------------|
| 1st | **Executive Summary** | 5 sec | Signal + Probability + Derivatives — do they agree? |
| 2nd | **Signal & Recommendation** | 10 sec | Read the plain-English recommendation |
| 3rd | **Probability & Reliability** | 10 sec | Probability above 55%? Win Rate above 50%? |
| 4th | **Derivatives Sentiment** | 10 sec | Is OI Buildup confirming the signal direction? |
| 5th | **Backtest** | 15 sec | Win Rate > 50% + Profit Factor > 1.0 + Positive Expectancy? |
| Optional | Chart, indicators, raw data | 30+ sec | Only if you want visual confirmation or deeper analysis |

### For Market Scanner

| Priority | Section | Time needed | What to look for |
|----------|---------|-------------|-----------------|
| 1st | **Intelligence Feed** | 10 sec | Is the market strong or weak overall? |
| 2nd | **Top 3 Opportunities** | 10 sec | Which stocks scored highest? What's their conviction level? |
| 3rd | **Breadth Metrics** | 10 sec | Bullish % above 55%? Participation above 50%? |
| 4th | **Anomalies Tab** | 10 sec | Any stocks flagged with unusual behavior worth investigating? |
| Optional | Filters, full table | 30+ sec | Explore specific sectors or setup types |

### The 30-Second Rule

If you truly have only 30 seconds, look at THREE things:

1. 🚦 **Signal** — Bullish, Bearish, or Neutral?
2. 🎯 **Probability** — Above or below 55%?
3. 📊 **Derivatives Sentiment** — Does it confirm the signal?

If all three agree → strong opportunity.
If they disagree → skip and look at another stock.

---

## 8. Frequently Asked Questions

### Getting Started

**Q: Do I need to know coding to use this app?**
A: No. Just run `streamlit run app.py` once, and everything works in your browser. You don't need to write any code. If you can use Google, you can use this app.

**Q: Do I need to know about stock markets?**
A: Basic knowledge helps (what buying/selling means, what a stock price is), but this guide explains everything you'll see on screen. You'll learn as you explore.

**Q: What stock exchange does this app cover?**
A: It covers stocks listed on the **NSE (National Stock Exchange)** of India. All tickers end with `.NS` (e.g., `RELIANCE.NS`).

### Understanding the App

**Q: Is this app giving me guaranteed trading advice?**
A: No. This app provides *data-driven analysis and historical probabilities*. Think of it as a very smart research assistant, not a crystal ball. All trading involves risk. Past performance does not guarantee future results.

**Q: What does "Anomaly Detected" mean? Should I immediately buy or sell?**
A: No! An anomaly means something *statistically unusual* is happening — like abnormally high volume. It could be bullish (institutional buying) or bearish (panic selling). It's a prompt to investigate further, not a direct trading signal. Check the news, check the chart, then decide.

**Q: What's the difference between Signal and Probability?**
A: Great question.
- The **Signal** tells you the *direction* → "The stock looks bullish"
- The **Probability** tells you *how confident to be* → "And there's a 67% chance this works out"
- A bullish signal with 45% probability is MUCH weaker than one with 75%
- **Always check both.** Direction without confidence is guessing.

**Q: What does "Regime" mean? Why should I care?**
A: The regime tells you *what kind of market you're in*. It matters because different strategies work in different regimes:
- In a **Trending** market → buy pullbacks, ride the trend
- In a **Consolidation** → wait for breakout, don't chase
- In a **High Volatility** regime → use wider stops, trade smaller
- Trying to buy breakouts in a sideways market will lose money. Regime awareness prevents that.

**Q: What does IV Percentile mean in simple terms?**
A: It tells you whether options are *cheap or expensive* right now compared to the past year.
- IV Percentile 80%+ → options are expensive (they cost more than 80% of the past year's prices)
- IV Percentile 20% or less → options are cheap
- For beginners: if you're buying options, cheaper is better. If selling options, more expensive is better.

### Using the Scanner

**Q: Why does the scanner take 30–90 seconds?**
A: The scanner does a LOT of work for each of the 50 stocks:
1. Downloads live price data from Yahoo Finance
2. Computes 10+ technical indicators
3. Runs the anomaly detection ML model
4. Classifies the market regime
5. Scores and ranks the stock
That's 250+ computations per stock × 50 stocks = 12,500+ calculations. Speed depends on your internet connection.

**Q: Can I add my own stocks to the scanner?**
A: Yes! The stock list is defined in `src/data/universe.py`. You can add any NSE-listed stock by adding its Yahoo Finance ticker (like `TATACHEM.NS`) to the `NIFTY_50_STOCKS` list.

**Q: The scanner shows "No scan results available." What do I do?**
A: Enable **"Scanner Debug Mode"** in the sidebar. This shows detailed logs of what failed. Common causes:
- Internet connection issues (Yahoo Finance couldn't be reached)
- All stocks failed to download (temporary Yahoo Finance outage)
- Try again after a minute

### Making Decisions

**Q: How do I know if a setup is worth trading?**
A: Use the 5-box checklist from Section 4:
1. Signal is Bullish or Bearish (not Neutral)
2. Probability is above 55%
3. Derivatives sentiment agrees
4. Backtest shows Win Rate > 50% and Profit Factor > 1.0
5. Anomaly status is Normal
If 4–5 boxes are checked → go for it. If fewer than 3 → skip.

**Q: What's a good stop loss to use?**
A: For most Indian large-cap stocks (NIFTY 50):
- **Swing trades (5–10 days):** 2–4% stop loss
- **Short-term (1–3 days):** 1–2% stop loss
- **Position trades (weeks):** 5–8% stop loss
The "Expected Move" card in the Executive Summary helps — set your stop loss slightly wider than the expected move.

**Q: Should I trust the backtest results?**
A: Backtest results show what WOULD have happened if you traded this setup in the past. They're useful because:
- If a setup lost money historically, it'll probably lose money again
- If a setup made money historically, it has a reasonable (but not guaranteed) chance of working again
- More trades in the backtest = more reliable results (20+ trades is good, fewer than 10 is shaky)

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

### ML Signal Engine (Phase 5)

| Term | Definition |
|------|------------|
| **ML Signal Engine** | An ensemble machine learning classifier that replaces the rule-based signal system. Uses RandomForest + GradientBoosting models trained on each stock's own price history. |
| **Feature Engineering Pipeline** | The process of extracting 22+ quantitative features from raw OHLCV + indicator data for ML model input. |
| **Ensemble Classifier** | A technique that combines predictions from multiple models (RandomForest + GradientBoosting) to produce more accurate and robust signals. |
| **Soft-Vote** | Averaging the probability outputs of multiple models rather than just their class predictions, resulting in smoother confidence scores. |
| **7-Class Signal Taxonomy** | The expanded signal classification: Strong Bullish, Bullish Continuation, Weak Bullish, Neutral/Consolidation, Weak Bearish, Bearish Breakdown, Strong Bearish, and High Volatility/Uncertain. |
| **Contributing Factors** | The top 5 ML features (by importance) that explain WHY a signal was generated, with human-readable descriptions. |
| **Feature Importance** | A measure from the ML model showing how much each input feature contributed to the prediction. |
| **Model Agreement** | How closely the RandomForest and GradientBoosting models agree on the predicted class probabilities (100% = perfect agreement). |
| **Rule-Based Fallback** | The original rule-based signal engine that activates when insufficient data (<100 bars) is available for ML training. |
| **Trend Alignment** | Whether the SMA20 > SMA50 structure supports the directional signal (used to distinguish "Continuation" from "Weak" signals). |

### AI Recommendation Narrator (Phase 5)

| Term | Definition |
|------|------------|
| **AI Narrator** | A module that interprets pre-computed analytics and generates human-readable market intelligence narratives. |
| **Template Fallback** | A zero-cost, high-quality narrative generation system using predefined templates that requires no API key. Works offline. |
| **LLM Provider** | An external AI service (Gemini, OpenAI, or Claude) that can generate richer narratives when an API key is provided. |
| **Key Insight** | A 2-3 sentence AI-generated summary of the stock's current technical situation. |
| **Best Use Case** | A specific, actionable trading strategy recommendation based on the signal class and momentum. |
| **LLM Validation** | Safety checks that reject LLM outputs contradicting the analytics (e.g., an LLM saying "sell" when the signal is bullish). |
| **Intelligence Context** | A structured dict assembling all analytics outputs for the narrator, without raw OHLCV data (safety measure). |

### Executive Summary V2 (Phase 5)

| Term | Definition |
|------|------------|
| **Glassmorphism** | A modern UI design style using translucent backgrounds, blur effects, and subtle borders for a premium look. |
| **Signal Badge** | The large colored card on the left showing the 7-class signal, price, and engine method. |
| **Confidence Bar** | An animated horizontal progress bar showing ML confidence percentage with gradient colors. |
| **Metric Pills** | Small rounded cards showing secondary metrics (Win Rate, Probability, IV Regime, Derivatives, Expected Move). |
| **Insight Card** | The narrative block below the signal badge containing Key Insight, Best Use Case, and Warning. |

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
