# 15-Slide Presentation Deck: Beyond the Consensus

**Project Title:** *Beyond the Consensus: An AI-Augmented Fundamental Valuation of Core Indian Blue Chips with Risk-Calibrated Portfolio Construction*  
**Target Delivery Time:** 10–12 Minutes (~45 Seconds per Slide)  
**Speaker Allocation (5 Slides Each):**
- **Slides 1–5:** **Sasi** (`246213618` — *Fundamental Valuation, DCF/DDM & Accounting Lead*)
- **Slides 6–10:** **Aditi Routray** (`246213548` — *AI Pipeline, FinBERT Sentiment & Behavioral Bias Lead*)
- **Slides 11–15:** **Sankarshana Mulugundam** (`246213080` — *Project Lead & Quantitative Portfolio Architect*)

---

## PART I: UNIVERSE SELECTION, FORENSIC AUDIT & INTRINSIC VALUATION (Speaker: Sasi)

### Slide 1: Title, Team Roster & Central Investment Thesis
- **Speaker:** **Sasi** (`246213618`) | **Pacing:** 45s
- **Visual / Layout:** Title Banner + Single Source of Truth Constants Box (`Cutoff: 2026-10-30`, `10Y G-Sec Rf: 6.85%`, `91D T-Bill Rf: 6.65%`, `India ERP: 6.00%`, `Corporate Tax: 25.17%`).
- **Key Bullet Points:**
  - **The Problem:** Short-term market pricing is systematically distorted by media narrative biases—chasing momentum in private banks, extrapolating temporary refining dips in conglomerates, and panicking over AI staffing disruption in IT.
  - **Our Solution:** A triangulated framework combining **Multi-Model Intrinsic Valuation** (`2-Stage DDM`, `Consolidated FCFF DCF`, `Segmental SOTP`, `Reverse DCF`), **Live `ProsusAI/finbert` NLP**, **1,000-Path GBM Monte Carlo**, and **Utility-Calibrated MVO Portfolio Construction**.
- **Speaker Script (Sasi):** *"Good morning Professor and panel. We present 'Beyond the Consensus'—an institutional framework that bridges fundamental intrinsic valuation, verified FinBERT natural language processing, and utility-based portfolio optimization across three flagship Indian blue chips: ICICI Bank, Reliance Industries, and TCS."*

---

### Slide 2: Three-Pillar Coverage Universe, Rejection Matrix & 10-Stock Correlation Proof
- **Speaker:** **Sasi** (`246213618`) | **Pacing:** 45s
- **Visual / Layout:** 10-Stock Nifty Correlation Heatmap (`01_data/cleaned/correlation_heatmap.png`) + Explicit Rejection Table.
- **Key Bullet Points:**
  - **Three Orthogonal Macro Engines + 1 Sovereign Anchor:** Private Credit (`ICICIBANK.NS`), Consumer/Digital/Energy Capex (`RELIANCE.NS`), Global USD Enterprise Technology (`TCS.NS`), and Sovereign Risk-Free Anchor (`91-Day RBI Treasury Bill @ 6.65%`).
  - **Empirical Diversification Proof ($N = 1,235$ daily log returns):** Pairwise correlations are remarkably low—**`ICICI–TCS = 0.2564`**, **`Reliance–TCS = 0.3401`**, and **`ICICI–Reliance = 0.4316`** (mean `0.3427`), vs. intra-sector pairs like `TCS–Infosys` (`0.7285`).
  - **Explicit 7-Stock Rejection Matrix:** Rejected `ITC` (ESG tobacco tax overhang), `HUL` (52x P/E with 3–4% volume growth = negative margin of safety), `Cummins India` (diesel genset terminal risk), `Coal India` (post-FY35 ESG reserve depletion), `Abbott India` (NLEM price ceiling cuts), `The Indian Hotels Company Ltd (Taj)` (cyclical peak multiples >55x P/E), and `BSE Ltd` (excessive retail options regulatory beta >2.2x).
- **Speaker Script (Sasi):** *"Rather than picking three stocks from one sector, we selected three orthogonal pillars of India's economy alongside the 91-Day RBI Treasury Bill as a risk-free sovereign anchor. Our 10-stock correlation matrix proves that ICICI Bank, Reliance, and TCS exhibit a mean pairwise correlation of just 0.34, providing far superior variance reduction than intra-sector peers."*

---

### Slide 3: 5-Year Historical Financial Trajectory & Forensic Footnote Audit (`FY22–FY26`)
- **Speaker:** **Sasi** (`246213618`) | **Pacing:** 45s
- **Visual / Layout:** 5-Year Ratio Comparison Table + Forensic Audit Badges (`Footnote_&_RPT_Audit` tab).
- **Key Bullet Points:**
  - **ICICI Bank:** NII compounded at `18.1%` CAGR to `₹92,400 Cr`; PAT reached `₹49,540 Cr` with `17.50%` ROE, `4.30%` NIM, and pristine `0.45%` Net NPA.
  - **Reliance Industries:** Consolidated Revenue reached `₹10.15 Lakh Cr` and EBITDA hit `₹1.82 Lakh Cr` (`17.93%` margin) with `95.9%` CFO/EBITDA cash conversion.
  - **TCS:** Revenue reached `₹2.58 Lakh Cr`, EBIT `₹63,200 Cr` (`24.50%` margin), `51.0%` ROE, and `98.2%` CFO/PAT conversion (`65.8` Debtor Days).
  - **Forensic Audit:** 100% of **Ind AS 116 lease liabilities** (`₹24,600 Cr` in Reliance; `₹8,200 Cr` in TCS) deducted in EV bridges; all **Ind AS 24 RPTs** verified as arm's-length; `94%` of ICICI's contingent liabilities are hedged FX swaps.
- **Speaker Script (Sasi):** *"Before modeling future cash flows, we audited five years of financials and footnotes. All three companies demonstrate >95% cash conversion, clean audit opinions, and full Ind AS 116 lease debt adjustments."*

---

### Slide 4: Intrinsic Valuation Models — 2-Stage DDM, Consolidated DCF, SOTP & Reverse DCF
- **Speaker:** **Sasi** (`246213618`) | **Pacing:** 50s
- **Visual / Layout:** Master Valuation Output Table (`Master_Valuation_Model.xlsx`) + Reliance SOTP & TCS Reverse DCF Callouts.
- **Key Bullet Points:**
  - **ICICI Bank (`2-Stage DDM & Excess Return`):** Standard FCFF is invalid for banks. Using $K_e = 12.65\%$ ($\beta = 0.9663$), Stage 1 ROE of `17.20%`, and terminal $g = 5.25\%$, we derive an Intrinsic Value of **`₹1,595.50`** vs. CMP `₹1,398.00` (**`+14.13%` upside — `ACCUMULATE`**).
  - **Reliance (`Consolidated FCFF DCF & SOTP`):** At $\text{WACC} = 12.10\%$ ($\beta = 1.1125$, $K_e = 13.53\%$, $g = 5.00\%$), moderating post-5G capex drives an Intrinsic Value of **`₹1,420.14`** vs. CMP `₹1,164.90` (**`+21.91%` upside — `BUY`**), cross-verified by our Segmental SOTP at **`₹1,441.95/sh`** (O2C `7.5x`, Jio `14.5x`, Retail `24.0x`, New Energy `1.5x IC`).
  - **TCS (`2-Stage FCFF DCF & Reverse DCF`):** At $\text{WACC} = 11.65\%$ ($\beta = 0.8184$, $K_e = 11.76\%$, $g = 4.50\%$), `8.50%` Stage 1 CAGR yields **`₹2,905.55`** vs. CMP `₹2,502.60` (**`+16.10%` upside — `ACCUMULATE`**). Our **Reverse DCF** proves CMP `₹2,502.60` prices in only **`5.13%`** 5Y revenue CAGR (`+337 bps` unpriced growth).
- **Speaker Script (Sasi):** *"We tailored each valuation model to the company's economic structure: a 2-Stage DDM for ICICI Bank yielding Rs 1,595.50, a Consolidated FCFF DCF cross-checked via SOTP for Reliance yielding Rs 1,420.14 (+21.91% upside), and a DCF plus Reverse DCF for TCS proving the market is pricing in an overly pessimistic 5.13% growth rate."*

---

### Slide 5: `5x5` Sensitivity Matrices & Relative Peer Valuation Multiples
- **Speaker:** **Sasi** (`246213618`) | **Pacing:** 45s
- **Visual / Layout:** Three `5x5` Sensitivity Heatmaps ($\pm 100$ bps $K_e$/WACC vs. $\pm 100$ bps Terminal $g$) + Peer Comps Table.
- **Key Bullet Points:**
  - **ICICI Bank Sensitivity:** Ranges from `₹1,207.85` (`Ke=13.65%, g=4.25%`) to `₹2,275.58` (`Ke=11.65%, g=6.25%`); trades at `3.34x` consolidated P/B, justified by `17.5%` ROE and `₹218/sh` subsidiary SOTP value.
  - **Reliance Sensitivity:** Ranges from `₹1,082.93` (`WACC=13.10%, g=4.00%`) to `₹2,015.42` (`WACC=11.10%, g=6.00%`); consolidated `9.38x EV/EBITDA` is a steep discount to telecom (`Airtel 14.8x`) and retail (`DMart 42.0x`) peers.
  - **TCS Sensitivity:** Ranges from `₹2,345.10` (`WACC=12.65%, g=3.50%`) to `₹3,896.80` (`WACC=10.65%, g=5.50%`); trades at `18.40x` FY26 P/E vs. Tier-1 IT peer average of `21.8x` despite `51%` ROE.
- **Speaker Script (Sasi):** *"Even under a +50 bps discount rate stress test, all three stocks preserve positive intrinsic upside. I now hand over to Aditi to walk through our AI and FinBERT pipeline."*

---

## PART II: AI-AUGMENTED NLP PIPELINE, BENCHMARKING & MONTE CARLO (Speaker: Aditi Routray)

### Slide 6: AI Pipeline Architecture & Deterministic 0%-Hallucination Quote Verifier
- **Speaker:** **Aditi Routray** (`246213548`) | **Pacing:** 45s
- **Visual / Layout:** 4-Stage AI Pipeline Diagram + `verified_quotes.json` Audit Table (`12/12 Verified`).
- **Key Bullet Points:**
  - **Why Domain-Specific NLP Over Raw Generative Prompts:** Unconstrained LLMs hallucinate financial numbers. We built a deterministic, reproducible pipeline combining live **`ProsusAI/finbert`** inference with programmatic **verbatim substring and `difflib.SequenceMatcher` verification**.
  - **Sub-Module 3 Audit Results (`01_data/cleaned/verified_quotes.json`):** Extracted `12` structured JSON records (`guidance`, `capex`, `contingent_liability`, `rpt`) from FY26 Annual Reports.
  - **100.00% Verification Rate / 0.00% Hallucination Rate:** Every quote achieved an exact normalized substring match (`similarity_ratio = 1.0000`, status `VERIFIED_0_HALLUCINATION`).
- **Speaker Script (Aditi):** *"Thank you Sasi. To ensure institutional rigor in our AI pipeline, we paired live PyTorch FinBERT inference with a deterministic verbatim verifier. Across all 12 annual report extractions covering guidance, capex, contingent liabilities, and RPTs, our verifier achieved a 100% exact match rate and a 0% hallucination rate."*

---

### Slide 7: 8-Quarter Concall Sentiment Trajectory & Management Optimism Gap (`Q1_FY25` – `Q4_FY26`)
- **Speaker:** **Aditi Routray** (`246213548`) | **Pacing:** 50s
- **Visual / Layout:** 3-Panel 8-Quarter FinBERT Sentiment & Optimism Gap Chart (`01_data/cleaned/sentiment_trends.png`).
- **Key Bullet Points:**
  - **Methodology:** Scored 24 earnings call transcripts (`Q1_FY25–Q4_FY26`) split into scripted `management_remarks` vs. unscripted `analyst_qa` (`Score = P(Pos) - P(Neg)`).
  - **Empirical Finding — The Management Optimism Gap ($\Delta = \text{Remarks} - \text{Q\&A}$):**
    - **ICICI Bank:** Remarks `+0.8774` vs. Q&A `-0.2153` → **Mean Gap = `+1.0927`** (Q&A Caution Density: `10.95/100w` on deposit pricing & unsecured loan calibration).
    - **Reliance Industries:** Remarks `+0.8909` vs. Q&A `-0.5925` → **Mean Gap = `+1.4833`** (Q&A Caution Density: `11.82/100w` on O2C crack volatility & retail store rationalization).
    - **TCS:** Remarks `+0.7890` vs. Q&A `-0.7482` → **Mean Gap = `+1.5372`** (Q&A Caution Density: `11.78/100w` on GenAI pricing pass-backs & US discretionary delays).
- **Speaker Script (Aditi):** *"When we separate scripted management remarks from unscripted analyst Q&A across 24 quarters, a striking pattern emerges: opening remarks average +0.79 to +0.89, whereas Q&A drops into negative territory with 11 to 12 caution qualifiers per 100 words. ICICI Bank exhibits the smallest optimism gap (+1.09), while TCS (+1.54) and Reliance (+1.48) face intense analyst scrutiny."*

---

### Slide 8: 90-Sentence Human Gold-Standard FinBERT Validation Benchmark
- **Speaker:** **Aditi Routray** (`246213548`) | **Pacing:** 45s
- **Visual / Layout:** 3x3 Confusion Matrix Heatmap + Validation Metrics Card (`model_validation_metrics.json`).
- **Key Bullet Points:**
  - **Gold-Standard Benchmark Design:** 90 representative concall sentences (`30 per company`, balanced across `30 Positive`, `30 Neutral`, `30 Negative`) independently labeled by the research team.
  - **Quantitative Validation Metrics:**
    - **Overall Accuracy:** **`95.56%`** (`86 / 90` correct)
    - **Macro-F1 Score:** **`0.9555`**
    - **Cohen's Kappa ($\kappa$):** **`0.9333`** (*Almost Perfect Agreement*)
    - **Per-Company Accuracy:** `ICICI Bank: 93.33%` (`28/30`) | `Reliance: 96.67%` (`29/30`) | `TCS: 96.67%` (`29/30`).
  - **Failure-Mode Analysis:** In the 4 misclassified sentences (`3 Negative → Positive`, `1 Neutral → Negative`), management combined cautious qualifiers (`"calibrated"`, `"moderating"`) with strong numeric metrics, causing FinBERT to overweight the financial figure.
- **Speaker Script (Aditi):** *"Rather than trusting FinBERT blindly, we benchmarked it against 90 human-labeled concall sentences. FinBERT achieved 95.56% accuracy, a Macro-F1 of 0.9555, and a Cohen's Kappa of 0.9333, with our confusion matrix pinpointing the exact 4 double-barreled sentences where FinBERT diverged."*

---

### Slide 9: 150-Headline Behavioral Bias Framing vs. Valuation Dislocation
- **Speaker:** **Aditi Routray** (`246213548`) | **Pacing:** 45s
- **Visual / Layout:** Stacked Bias Distribution Chart + Narrative Dislocation Synthesis Table (`bias_framing_results.csv`).
- **Key Bullet Points:**
  - **ICICI Bank (`58% Hype / FOMO`, Media Sent `+0.2217`):** Media crowns ICICI the "unstoppable banking king" (+4.8% EPS revisions). Our DDM shows `+14.13%` upside—warranting disciplined **`ACCUMULATE`**, not FOMO chasing.
  - **Reliance (`34% Recency Bias / Extrapolation`, Media Sent `-0.2879`):** Traders extrapolate 2 quarters of O2C margin dips and retail store closures (`-1.4%` EPS trim), ignoring the post-5G free cash flow surge (**`+21.91%` DCF upside — contrarian `BUY`**).
  - **TCS (`50% Loss Aversion / Disruption Fear`, Media Sent `-0.3438`):** Media fixates on existential GenAI staffing fears (`-2.1%` EPS trim), compressing market-implied growth to `5.13%` vs. `8.50%` TCV-backed DCF reality (**`+16.10%` upside — `ACCUMULATE`**).
- **Speaker Script (Aditi):** *"Classifying 150 financial news headlines reveals *why* our DCF valuations diverge from market prices: Reliance suffers from 34% Recency Bias over short-term O2C cracks, and TCS suffers from 50% Loss Aversion over AI disruption fears—creating our two largest fundamental value dislocations."*

---

### Slide 10: Technical Momentum Indicators & 1,000-Path GBM Monte Carlo Fan Charts
- **Speaker:** **Aditi Routray** (`246213548`) | **Pacing:** 45s
- **Visual / Layout:** 3-Panel GBM Monte Carlo Fan Chart (`01_data/cleaned/mc_fan_charts.png`) + Technical Regime Table.
- **Key Bullet Points:**
  - **ICICI Bank (`CMP ₹1,398.00`):** Strong Uptrend (`Price > 50-DMA ₹1,378 > 200-DMA ₹1,347`), `RSI = 56.97`, bullish `MACD Hist = +3.76`. 1Y MC Median (`P50`) = **`₹1,553.35` (`+11.11%`)**, closely matching our `₹1,595.50` DDM target.
  - **Reliance (`CMP ₹1,164.90`):** Trading below `50-DMA (₹1,236)` and `200-DMA (₹1,326)`, `RSI = 40.27` (oversold), but early bullish `MACD Hist = +0.36`. Backward-looking GBM Median is `₹1,125.15`, whereas our forward DCF target (`₹1,420.14`) sits at the `82nd percentile` (`P75 = ₹1,318`, `P90 = ₹1,513`).
  - **TCS (`CMP ₹2,502.60`):** Rebounding above `50-DMA (₹2,255)` & `200-DMA (₹2,394)`, `RSI = 67.56`, `MACD Hist = +16.22`. Forward DCF target (`₹2,905.55`) sits between `P75 (₹2,774)` and `P90 (₹3,134)`.
- **Speaker Script (Aditi):** *"Our 1,000-path GBM Monte Carlo simulation illustrates why backward-looking price drift cannot replace fundamental valuation during cyclical inflections: Reliance shows an early MACD positive crossover near oversold RSI levels, setting up convergence toward our Rs 1,420 DCF target. I now hand over to Sankarshana for portfolio construction."*

---

## PART III: MVO, UTILITY ALLOCATION, 20Y SIP & 4-METRIC BACKTEST (Speaker: Sankarshana Mulugundam)

### Slide 11: Blended Expected Returns, MVO Tangency Portfolio & Efficient Frontier
- **Speaker:** **Sankarshana Mulugundam** (`246213080`) | **Pacing:** 50s
- **Visual / Layout:** Efficient Frontier & Capital Allocation Line (`01_data/cleaned/efficient_frontier_cal.png`).
- **Key Bullet Points:**
  - **Solving the Historical Drift Trap:** 5Y historical log returns (`Reliance +0.27%`, `TCS -3.77%`) reflect past valuation derating. We blend **`50% CAPM Ke + 50% DCF/DDM 5Y Implied IRR`**:
    - `ICICIBANK.NS`: $0.5(12.65\%) + 0.5(15.33\%) = \mathbf{13.99\%}$ ($\sigma = 19.55\%, \beta = 0.9663$)
    - `RELIANCE.NS`: $0.5(13.53\%) + 0.5(17.57\%) = \mathbf{15.55\%}$ ($\sigma = 22.33\%, \beta = 1.1125$)
    - `TCS.NS`: $0.5(11.76\%) + 0.5(14.79\%) = \mathbf{13.28\%}$ ($\sigma = 22.85\%, \beta = 0.8184$)
  - **Max-Sharpe Tangency Portfolio (`Rf = 91D T-Bill @ 6.65%`):**
    - Optimal Weights: **`38.90%` ICICI Bank**, **`37.91%` Reliance**, **`23.19%` TCS**
    - Portfolio Metrics: **$E(R_p) = 14.42\%$**, **$\sigma_p = 15.74\%$** (`400–700 bps` lower vol than standalone stocks!), **$\beta_p = 0.9874$**, **Sharpe = `0.4935`** (vs. Nifty 50 forward Sharpe `0.4328`).
- **Speaker Script (Sankarshana):** *"Thank you Aditi. To prevent past cyclical derating from corrupting Markowitz optimization, we blended 50% CAPM equilibrium returns with 50% DCF implied IRRs. Our Max-Sharpe Tangency Portfolio allocates 38.9% to ICICI Bank, 37.9% to Reliance, and 23.2% to TCS—cutting standalone volatility down to 15.74% and delivering a 0.4935 Sharpe ratio."*

---

### Slide 12: 10-Question Risk Profiler, Prudence Override Rule & Featured Case Study (A = 4.00)
- **Speaker:** **Sankarshana Mulugundam** (`246213080`) | **Pacing:** 50s
- **Visual / Layout:** Utility Allocation Table (`Portfolio_Model.xlsx` Tab 2) + Prudence Rule Architecture Diagram.
- **Key Bullet Points:**
  - **Two-Dimensional Risk Scoring ($R \in [10, 40]$):** Section A measures **Financial Ability (`5–20`)** and Section B measures **Psychological Willingness (`5–20`)**.
  - **The Prudence Override Rule:** If $|\text{Sec A} - \text{Sec B}| \ge 6$, we override $R_{\text{eff}} = 2 \times \min(\text{Sec A}, \text{Sec B})$ so an emotionally aggressive investor with a fragile balance sheet (or vice versa) is protected.
  - **Linear Risk Aversion & CAL Separation Theorem:** $A = 10 - 0.3(R_{\text{eff}} - 10)$ determines optimal risky share $y^* = \min\left(1.0, \frac{E(R_{\text{tan}}) - R_f}{A \sigma_{\text{tan}}^2}\right)$.
  - **Featured Moderate-Growth Case Study ($A = 4.00$, $R = 30$, Sec A = 15, Sec B = 15):**
    - **Asset Weights:** **`30.50%` ICICI Bank**, **`29.72%` Reliance Industries**, **`18.18%` TCS**, **`21.59%` 91D RBI T-Bill** ($y^* = 78.41\%$, $1 - y^* = 21.59\%$).
    - **Performance Metrics:** $E(R_c) = 12.74\%$, $\sigma_c = 12.34\%$, $\beta_c = 0.7742$, Sharpe = `0.4935`, Jensen's Alpha = `+1.45%`, Utility $U = 0.0970$.
    - **₹10 Lakh Lump Sum Splits:** ICICI = `₹3,05,000`, Reliance = `₹2,97,200`, TCS = `₹1,81,800`, 91D T-Bill = `₹2,15,900`.
    - **₹25,000/mo SIP Splits:** ICICI = `₹7,625`, Reliance = `₹7,430`, TCS = `₹4,545`, 91D T-Bill = `₹5,398` (Total = ₹25,000).
  - **Other Canonical Baskets:**
    - **Aggressive (`18/18` → $A=2.20$):** `100.0%` Equity / `0.0%` T-Bill | $E(R_c)=14.42\%, \sigma_c=15.74\%, U=0.1169$.
    - **Balanced (`14/13` → $A=4.90$):** `64.0%` Equity / `36.0%` T-Bill | $E(R_c)=11.62\%, \sigma_c=10.07\%, U=0.0914$.
    - **Defensive (`8/7` → $A=8.50$):** `36.9%` Equity / `63.1%` T-Bill | $E(R_c)=9.52\%, \sigma_c=5.81\%, U=0.0808$.
    - **Prudence Override (`9/18` → $|9-18|=9 \ge 6 \Rightarrow R_{\text{eff}}=18, A=7.60$):** Caps equity at **`41.27%`** instead of `64.00%`!
- **Speaker Script (Sankarshana):** *"By Tobin's Separation Theorem, all investors hold the same Tangency equity mix but scale their risky share y-star along the Capital Allocation Line according to their risk aversion A. In our featured moderate-growth case study at A = 4.00, the optimal allocation is 78.41% equity and 21.59% T-Bills—translating to exactly Rs 3.05 Lakh in ICICI, Rs 2.97 Lakh in Reliance, Rs 1.82 Lakh in TCS, and Rs 2.16 Lakh in T-Bills for a 10 Lakh Rupee portfolio."*

---

### Slide 13: 20-Year Step-Up SIP Lifecycle Glide Path (`₹25,000/mo`, `+10%` Annual Step-Up)
- **Speaker:** **Sankarshana Mulugundam** (`246213080`) | **Pacing:** 45s
- **Visual / Layout:** 20-Year Step-Up SIP Wealth & Asset Allocation Glide Path Chart (`01_data/cleaned/sip_glide_path.png`).
- **Key Bullet Points:**
  - **Dynamic Lifecycle Rebalancing (`240 Months`, `Age 25–44`):**
    - **Phase 1 (Years 1–8, Age 25–32):** Early-career accumulation in **Aggressive Basket (`A=2.20`, `100%` Equity)**.
    - **Phase 2 (Years 9–15, Age 33–39):** Mid-career consolidation in **Balanced Basket (`A=4.90`, `64.0%` Equity / `36.0%` T-Bill)**.
    - **Phase 3 (Years 16–20, Age 40–44):** Pre-retirement preservation in **Defensive Basket (`A=8.50`, `36.9%` Equity / `63.1%` T-Bill)**.
  - **Terminal Wealth Outcomes:**
    - **Total Cumulative Capital Invested:** **`₹1.7182 Crore`** (`₹1,71,82,500`)
    - **Deterministic Expected Corpus:** **`₹4.3241 Crore`** (**`2.52x`** wealth multiple)
    - **1,000-Path Stochastic Monte Carlo:** `P10 = ₹3.1765 Cr` | **`Median (P50) = ₹4.1962 Cr`** | `P90 = ₹5.7370 Cr`.
- **Speaker Script (Sankarshana):** *"Deploying this framework into a 20-year Step-Up SIP starting at Rs 25,000 per month with a 10% annual step-up invests Rs 1.72 Crore and compounds to an expected corpus of Rs 4.32 Crore, while automatically shifting 63.1% into risk-free T-Bills in the final five years to lock in gains."*

---

### Slide 14: Mandatory 4-Metric Portfolio Evaluation & 5-Year Historical Backtest
- **Speaker:** **Sankarshana Mulugundam** (`246213080`) | **Pacing:** 45s
- **Visual / Layout:** 4-Metric Evaluation Table + 5-Year Cumulative Wealth Chart (`01_data/cleaned/backtest_performance.png`).
- **Key Bullet Points:**
  - **Complete Evaluation Across All 4 Course Metrics (vs. Nifty 50 `^NSEI`):**
    1. **Sharpe Ratio:** Tangency (`0.4935`), Featured $A=4.00$ (`0.4935`), Balanced (`0.4935`), and Defensive (`0.4940`) all beat Nifty 50 (`0.4328`) and Equal-Weight (`0.4875`).
    2. **Treynor Measure:** All CAL portfolios achieve **`0.0786`** excess return per unit of Beta vs. Nifty 50 (`0.0600`).
    3. **Jensen's Alpha ($\alpha$):** Featured $A=4.00$ generates **`+1.45%`** and Tangency generates **`+1.84%`** annual equilibrium alpha (`Balanced +1.18%`, `Defensive +0.68%`).
    4. **Information Ratio ($IR$):** Active return per unit of tracking error (Tangency `+0.2274` at `7.76%` TE, Featured $A=4.00$ `+0.0144` at `6.84%` TE).
  - **Mathematical Invariance along CAL:** By Tobin's Separation Theorem, Sharpe and Treynor are mathematically identical along the CAL because excess return and volatility scale linearly with $y^*$.
  - **5-Year Historical Backtest (`2021–2026`):** Demonstrates why capital preservation in the Defensive (`₹131.88`) and Balanced (`₹127.20`) baskets cushioned TCS and Reliance's cyclical derating while ICICI Bank surged (`₹180.79`).
- **Speaker Script (Sankarshana):** *"Evaluating our portfolios across all four mandatory course metrics—Sharpe, Treynor, Jensen's Alpha, and Information Ratio—proves that our Tangency and Featured A = 4.00 portfolios beat the Nifty 50 across every dimension, generating positive Jensen's Alpha and matching the optimal 0.4935 CAL Sharpe ratio."*

---

### Slide 15: Final Synthesis, Actionable Verdict, Limitations & Live Dashboard Demo
- **Speaker:** **Sankarshana Mulugundam** (`246213080`) | **Pacing:** 45s
- **Visual / Layout:** Triangulated Synthesis Matrix + Screenshot/Link to Offline 9-Block Streamlit App (`05_dashboard/app.py`).
- **Key Bullet Points:**
  - **Final Triangulated Recommendations:**
    - **Reliance Industries (`RELIANCE.NS` — `BUY`, `37.91%` MVO Weight):** `+21.91%` DCF upside (`₹1,420.14`), cross-verified by SOTP (`₹1,441.95`); contrarian dislocation against `34%` media recency bias.
    - **ICICI Bank (`ICICIBANK.NS` — `ACCUMULATE`, `38.90%` MVO Weight):** `+14.13%` DDM upside (`₹1,595.50`), lowest concall optimism gap (`+1.09`), core compounding anchor.
    - **TCS (`TCS.NS` — `ACCUMULATE`, `23.19%` MVO Weight):** `+16.10%` DCF upside (`₹2,905.55`), Reverse DCF proves `5.13%` implied CAGR over-discounts AI fears, lowest Nifty correlation (`0.26` with ICICI).
  - **Key Limitations:** Double-barreled concall sentences in FinBERT (`4/90` misses), log-normal constant-volatility GBM assumption, and static 5-year OLS Betas.
- **Speaker Script (Sankarshana):** *"In conclusion, combining fundamental DCF/DDM models with verified FinBERT sentiment allows us to look beyond media noise and construct risk-calibrated portfolios. All 9 interactive modules are live in our offline-cached Streamlit dashboard. We welcome your questions."*

---

## APPENDIX: VIVA / Q&A DEFENSE CHEAT SHEET (6 TOUGHEST FACULTY QUESTIONS)

### Q1 (To Sasi): *"Why did you use a 2-Stage DDM & Excess Return model for ICICI Bank instead of the FCFF DCF model you used for Reliance and TCS?"*
- **Crisp Quantitative Answer:** In a commercial bank, debt and customer deposits (`₹18.02 Lakh Cr` at ICICI Bank) are not financing decisions—they are the bank's operational raw material used to generate Net Interest Income (`₹92,400 Cr`). Consequently, operating cash flow, working capital (`ΔNWC`), and pre-interest WACC cannot be meaningfully separated from financing cash flows. Valuing equity directly via **2-Stage DDM and Excess Equity Return (`(ROE - Ke) × Beginning_BVPS`)** discounted at **CAPM $K_e = 12.65\%$** is the only theoretically sound intrinsic framework for financial institutions.

### Q2 (To Sasi): *"TCS's 5-year historical stock return is negative (-3.77% annualized log return). How can you justify an intrinsic upside of +16.10% (₹2,905.55)?"*
- **Crisp Quantitative Answer:** TCS's share price de-rated from ~32x P/E in 2021 to `18.40x` FY26 P/E today due to post-COVID multiple compression and GenAI staffing fears—even while its underlying Revenue grew from `₹1.92L Cr` to `₹2.58L Cr` and PAT rose from `₹38,327 Cr` to `₹49,200 Cr` with a `51.0%` ROE. Our **Reverse DCF** proves that at `WACC = 11.65%` and `24.5%` EBIT margin, the current market price of `₹2,502.60` implies only a **`5.13%` 5-year revenue CAGR**, whereas TCS's `USD 41B+` annual TCV order book supports an **`8.50%` CAGR** (`+337 bps` unpriced growth).

### Q3 (To Aditi): *"How do you guarantee that your AI pipeline didn't hallucinate any financial numbers or annual report footnotes?"*
- **Crisp Quantitative Answer:** First, all valuation and portfolio math is executed in deterministic Python (`numpy`, `scipy`, `openpyxl`) rather than generative text prompts. Second, for qualitative annual report extraction (Sub-Module 3), we built a **deterministic verbatim verification function** (`verify_quote_against_source`) that checks both exact normalized-whitespace substring inclusion and `difflib.SequenceMatcher` similarity (`>= 0.95`) against the raw source document. All `12/12` extracted quotes achieved a **`1.0000` similarity ratio (`0.00%` hallucination rate)**.

### Q4 (To Aditi): *"In your 90-sentence human validation benchmark, FinBERT achieved 95.56% accuracy (86/90). What caused the 4 misclassifications?"*
- **Crisp Quantitative Answer:** Looking at our `3x3` confusion matrix (`[[30, 0, 0], [0, 29, 1], [3, 0, 27]]`), `3` human-labeled Negative Q&A sentences were predicted as Positive by FinBERT, and `1` Neutral sentence was predicted as Negative. Those 3 Q&A sentences contained **double-barreled Indian corporate phrasing**—where management acknowledged a risk using a soft qualifier (`"calibrated unsecured growth"`, `"margin expansion remains subject to deposit repricing"`) alongside a positive operational noun. This is precisely why we supplemented raw FinBERT scores with our explicit **Hedging/Caution Qualifier Density Index (`~11–12 per 100 words` in Q&A)**.

### Q5 (To Sankarshana): *"Why did you use two different risk-free rates—6.85% (10Y G-Sec) in DCF/DDM and 6.65% (91D T-Bill) in Portfolio Optimization?"*
- **Crisp Quantitative Answer:** This follows **duration matching**:
  1. In **DCF/DDM valuation**, we discount perpetual corporate cash flows spanning 5 to $\infty$ years; matching the duration of long-term equity cash flows requires the **10-Year India Sovereign G-Sec yield (`6.85%`)**.
  2. In **Mean-Variance Portfolio Allocation and Sharpe Ratio calculation**, the risk-free asset in the complete portfolio $(1 - y^*)$ must be a zero-duration, liquid money-market instrument free of interest-rate mark-to-market price risk—which is the **91-Day RBI Treasury Bill (`6.65%`)**.

### Q6 (To Sankarshana): *"Why do the Tangency, Balanced, and Defensive portfolios all have virtually the same Forward Sharpe Ratio (~0.4935) and Treynor Ratio (~0.0786), whereas their Information Ratios differ?"*
- **Crisp Quantitative Answer:** By **Tobin's Two-Fund Separation Theorem**, the Balanced (`y* = 64.0%`) and Defensive (`y* = 36.9%`) baskets are linear combinations of the **Max-Sharpe Tangency Portfolio** and the **Risk-Free 91D T-Bill (`6.65%`)** along the **Capital Allocation Line (CAL)**. Because both excess return $E(R_c) - R_f = y^*(E(R_{\text{tan}}) - R_f)$ and volatility $\sigma_c = y^* \sigma_{\text{tan}}$ (as well as $\beta_c = y^* \beta_{\text{tan}}$) scale linearly with $y^*$, their **Sharpe Ratio (the slope of the CAL = `0.4935`)** and **Treynor Measure (`0.0786`)** are mathematically invariant to $y^*$! By contrast, the **Information Ratio** benchmarks against the **Nifty 50 (`100%` equity)** rather than $R_f$, so holding `36%–63%` in T-Bills lowers active return relative to a `100%` equity index during bull markets while protecting capital during drawdowns.
