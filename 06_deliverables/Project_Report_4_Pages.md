# Beyond the Consensus: An AI-Augmented Fundamental Valuation of Core Indian Blue Chips with Risk-Calibrated Portfolio Construction

**Course Deliverable:** Final 4-Page Executive Valuation, AI Analytics & Portfolio Architecture Report  
**Team Members:** **Sankarshana Mulugundam** (`246213080` — *Project Lead, Quantitative Portfolio Architect & ICICI Bank Lead*) | **Aditi Routray** (`246213548` — *AI/FinBERT Pipeline, Bias Analytics & Reliance Lead*) | **Sasi** (`246213618` — *Fundamental DCF/DDM Valuation, Forensic Audit & TCS Lead*)  
**Single Source of Truth Constants:** Cutoff Date: `2026-10-30` (`1,236` Trading Days) | Valuation $R_f$ (10Y India G-Sec): `6.85%` | Portfolio $R_f$ (91D RBI T-Bill): `6.65%` | India ERP: `6.00%` | Corporate Tax Rate: `25.17%`

---

## PAGE 1: EXECUTIVE THESIS, THREE-PILLAR COVERAGE UNIVERSE & CORRELATION PROOF

### 1.1 Central Investment Thesis ("Beyond the Consensus")
Short-term Indian equity pricing is frequently distorted by media narrative biases—extrapolating temporary refining margin dips in conglomerates, over-reacting to Generative AI staffing fears in IT services, or chasing momentum in private banks. This study builds an end-to-end, institutional-grade valuation and portfolio architecture across three flagship Nifty 50 leaders—**ICICI Bank (`ICICIBANK.NS`)**, **Reliance Industries (`RELIANCE.NS`)**, and **Tata Consultancy Services (`TCS.NS`)**—integrating multi-model intrinsic valuation (`2-Stage DDM`, `Consolidated FCFF DCF`, `Segmental SOTP`, and `Reverse DCF`) with live **`ProsusAI/finbert` natural language inference**, **1,000-path GBM Monte Carlo simulations**, and **utility-calibrated Mean-Variance Portfolio Optimization**.

### 1.2 Three-Pillar Macroeconomic Coverage & Explicit Rejection Rationale
Rather than selecting three stocks from a single industry, our coverage universe spans the three foundational, orthogonal engines of Indian corporate cash flows while explicitly rejecting structurally flawed alternatives:

| Evaluated Company | Sector / Macro Pillar | Decision | Quantitative & Structural Selection / Rejection Rationale |
| :--- | :--- | :---: | :--- |
| **ICICI Bank** (`ICICIBANK.NS`) | Private Banking & Credit | **SELECTED (#1)** | Best-in-class `17.50%` ROE, `4.30%` NIM, and `0.45%` Net NPA; demonstrates **2-Stage DDM & Excess Equity Return** modeling where standard FCFF is invalid because deposits are operating raw material. |
| **Reliance Industries** (`RELIANCE.NS`) | Energy, Telecom (Jio) & Retail | **SELECTED (#2)** | Captures India's digital/consumer platform scaling (>56% of EBITDA) as 5G capex moderates; pairs **Consolidated 2-Stage FCFF DCF** with **Segmental SOTP** cross-verification. |
| **TCS** (`TCS.NS`) | IT Services & AI Consulting | **SELECTED (#3)** | Industry-leading `51.0%` ROE, `98.2%` CFO/PAT conversion, and low Nifty Beta (`0.8184`); ideal for testing AI disruption narratives via **Reverse DCF Implied Growth** modeling. |
| **ITC Ltd** (`ITC.NS`) | Cigarettes & FMCG | *REJECTED* | Post-hotel demerger terminal multiple remains capped by ESG punitive tobacco taxation risk; domestic consumption growth is captured with higher operating leverage inside Reliance Retail. |
| **Hindustan Unilever** (`HINDUNILVR.NS`) | Consumer Staples | *REJECTED* | Trading at ~52x P/E despite muted 3–4% rural volume growth, yielding a negative margin of safety under disciplined DCF assumptions. |
| **Cummins India** (`CUMMINSIND.NS`) | Capital Goods | *REJECTED* | Terminal value faces structural vulnerability as data-center diesel backup gensets face long-term battery storage and green hydrogen substitution. |
| **Coal India** (`COALINDIA.NS`) | Thermal Mining | *REJECTED* | Finite reserve depletion and post-FY35 energy transition headwinds violate perpetual Gordon Growth terminal value assumptions. |

### 1.3 Empirical 10-Stock Return Correlation Proof (`2021-10-31` to `2026-10-30`, $N = 1,235$ Daily Log Returns)
Across a 10-stock Nifty 50 universe (our 3 core stocks plus `HDFCBANK.NS`, `INFY.NS`, `ITC.NS`, `LT.NS`, `SUNPHARMA.NS`, `MARUTI.NS`, and `NTPC.NS`), our core triad exhibits exceptionally low pairwise correlations—**`ICICI–TCS = 0.2564`**, **`Reliance–TCS = 0.3401`**, and **`ICICI–Reliance = 0.4316`**—compared to intra-sector pairs (`TCS–Infosys = 0.7285`, `ICICI–HDFC Bank = 0.5412`), proving superior cross-sector variance reduction:

| Ticker | `ICICIBANK` | `RELIANCE` | `TCS` | `HDFCBANK` | `INFY` | `ITC` | `LT` | `SUNPHARMA` | `MARUTI` | `NTPC` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`ICICIBANK.NS`** | **1.0000** | **0.4316** | **0.2564** | 0.5412 | 0.2890 | 0.2614 | 0.4620 | 0.2145 | 0.3418 | 0.3510 |
| **`RELIANCE.NS`** | **0.4316** | **1.0000** | **0.3401** | 0.4105 | 0.3380 | 0.2980 | 0.4490 | 0.2580 | 0.3690 | 0.3925 |
| **`TCS.NS`** | **0.2564** | **0.3401** | **1.0000** | 0.2490 | 0.7285 | 0.1950 | 0.3120 | 0.2640 | 0.2380 | 0.2190 |

---

## PAGE 2: FUNDAMENTAL ANALYSIS, INTRINSIC VALUATION MODELS & FORENSIC AUDIT

### 2.1 5-Year Historical Financial Trajectory & Quality Ratios (`FY22` – `FY26`)

| Company | Key Top-Line (`FY22` → `FY26`) | Key Operating Profit (`FY22` → `FY26`) | Net Profit PAT (`FY22` → `FY26`) | `FY26` ROE / ROCE | `FY26` Margin / Asset Quality | `FY26` Cash / Balance Sheet Quality |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ICICI Bank** | NII: `₹47,466` → `₹92,400 Cr` (`+18.1%` CAGR) | PPOP: `₹39,250` → `₹73,150 Cr` (`+16.8%` CAGR) | `₹23,339` → `₹49,540 Cr` (`+20.7%` CAGR) | ROE: `17.50%` \| ROA: `2.25%` | NIM: `4.30%` \| Net NPA: `0.45%` | Tier-1 CAR: `16.25%` \| CASA: `41.80%` |
| **Reliance Ind.** | Rev: `₹7.22L` → `₹10.15L Cr` (`+8.9%` CAGR) | EBITDA: `₹1.10L` → `₹1.82L Cr` (`+13.3%` CAGR) | `₹60,705` → `₹79,500 Cr` (`+7.0%` CAGR) | ROE: `9.60%` \| ROCE: `11.40%` | EBITDA Margin: `17.93%` | CFO: `₹1.745L Cr` (`95.9%` CFO/EBITDA) |
| **TCS** | Rev: `₹1.92L` → `₹2.58L Cr` (`+7.7%` CAGR) | EBIT: `₹48,453` → `₹63,200 Cr` (`+6.9%` CAGR) | `₹38,327` → `₹49,200 Cr` (`+6.4%` CAGR) | ROE: `51.00%` \| ROCE: `63.10%` | EBIT Margin: `24.50%` | CFO/PAT: `98.17%` \| Debtor Days: `65.8` |

### 2.2 Master Intrinsic Valuation Summary, SOTP Cross-Check & Reverse DCF Proof

| Company (`Ticker`) | Primary Valuation Methodology | 5Y Raw $\beta$ | CAPM $K_e$ | Discount Rate ($K_e$ / WACC) | Terminal $g$ | Intrinsic Value (INR) | Cutoff CMP (INR) | Implied Upside / MoS | Implied 5Y IRR | Actionable Rating |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ICICI Bank** (`ICICIBANK.NS`) | **2-Stage DDM & Excess Return** (`704.8 Cr` sh) | `0.9663` | `12.65%` | `12.65%` ($K_e$) | `5.25%` | **`₹1,595.50`** | `₹1,398.00` | **`+14.13%`** | `15.33%` | **ACCUMULATE** |
| **Reliance** (`RELIANCE.NS`) | **Consolidated 2-Stage FCFF DCF & SOTP** (`1,353.2 Cr` sh) | `1.1125` | `13.53%` | `12.10%` (WACC) | `5.00%` | **`₹1,420.14`** | `₹1,164.90` | **`+21.91%`** | `17.57%` | **BUY** |
| **TCS** (`TCS.NS`) | **2-Stage FCFF DCF & Reverse DCF** (`361.8 Cr` sh) | `0.8184` | `11.76%` | `11.65%` (WACC) | `4.50%` | **`₹2,905.55`** | `₹2,502.60` | **`+16.10%`** | `14.79%` | **ACCUMULATE** |

- **ICICI Bank Excess Equity Return & Justified P/B Check:** Stage 1 (`FY27E–FY31E`) models sustainable `17.20%` ROE with dividend payout ramping from `20%` to `28%` as loan growth normalizes, generating positive Excess Equity Return `(ROE - Ke) > +455 bps` annually. Stage 2 applies Gordon Growth (`g = 5.25%`, `72%` steady-state consolidated distributable payout) yielding **`₹1,595.50`** (`PV of Stage 1 DPS = ₹77.81` + `PV of Terminal Value = ₹1,517.69`).
- **Reliance Segmental SOTP Sanity Check (`₹1,441.95/share`):** Cross-checking our Consolidated FCFF DCF (`₹1,420.14`) via `FY27E` Sum-of-the-Parts values O2C at `7.5x EBITDA` (`₹4,83,750 Cr` = `₹357.49/sh`), Jio Digital Services at `14.5x EBITDA` (`₹9,88,900 Cr` = `₹730.79/sh`), Organized Retail at `24.0x EBITDA` (`₹6,09,600 Cr` = `₹450.49/sh`), and New Energy at `1.5x Invested Capital` (`₹67,500 Cr` = `₹49.88/sh`), less Net Debt (`₹1,30,000 Cr`) and Minority Interest (`₹68,500 Cr`) = **`₹1,441.95/share`** (within `1.5%` of DCF).
- **TCS Reverse DCF Implied Growth Proof (`5.13%` vs. `8.50%`):** Solving for the 5-year revenue CAGR required at `WACC = 11.65%` and `24.5%` EBIT margin to justify TCS's current market price of `₹2,502.60` yields **`5.13%`**. Given TCS's `USD 41B+` annual TCV bookings (`~8.50%` fundamental CAGR), the market is over-discounting GenAI deflation by **`337 bps`** of annual growth.

### 2.3 `5x5` WACC / $K_e$ vs. Terminal Growth ($g$) Sensitivity Bounds & Forensic Audit Summary
- **Sensitivity Ranges ($\pm 100$ bps Discount Rate $\times \pm 100$ bps Terminal $g$):**
  - **ICICI Bank (`CMP ₹1,398.00`):** Bear (`Ke=13.65%, g=4.25%`) = `₹1,207.85` | **Base (`Ke=12.65%, g=5.25%`) = `₹1,595.50`** | Bull (`Ke=11.65%, g=6.25%`) = `₹2,275.58`.
  - **Reliance (`CMP ₹1,164.90`):** Bear (`WACC=13.10%, g=4.00%`) = `₹1,082.93` | **Base (`WACC=12.10%, g=5.00%`) = `₹1,420.14`** | Bull (`WACC=11.10%, g=6.00%`) = `₹2,015.42`.
  - **TCS (`CMP ₹2,502.60`):** Bear (`WACC=12.65%, g=3.50%`) = `₹2,345.10` | **Base (`WACC=11.65%, g=4.50%`) = `₹2,905.55`** | Bull (`WACC=10.65%, g=5.50%`) = `₹3,896.80`.
- **Forensic Accounting & Ind AS 24 RPT Audit:** All 3 companies carry **unqualified statutory audit opinions**, zero promoter loan tunneling, full deduction of **Ind AS 116 lease liabilities** (`₹24,600 Cr` in Reliance Gross Debt; `₹8,200 Cr` in TCS EV bridge), and manageable disputed tax contingencies (`2.85%` of Net Worth at ICICI; `7.80%` at Reliance; `13.9%` at TCS with `₹6,150 Cr` pre-deposited).

---

## PAGE 3: AI-AUGMENTED NLP PIPELINE, HUMAN BENCHMARKING & MONTE CARLO SCENARIOS

### 3.1 Live `ProsusAI/finbert` 8-Quarter Concall Sentiment & Management Optimism Gap (`Q1_FY25` – `Q4_FY26`)
We scored 24 quarterly earnings call transcripts (`Q1_FY25` to `Q4_FY26`) split into CEO/CFO `management_remarks` and `analyst_qa` using live `ProsusAI/finbert` (`Sentiment = P(Positive) - P(Negative)`):

| Company (`Ticker`) | 8Q Mean Prepared Remarks | 8Q Mean Analyst Q&A | **Mean Optimism Gap ($\Delta$)** | `Q4_FY26` Remarks / Q&A | Prepared Remarks Caution (`/100w`) | **Analyst Q&A Caution (`/100w`)** | Primary Q&A Discussion Friction |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **ICICI Bank** (`ICICIBANK.NS`) | `+0.8774` | `-0.2153` | **`+1.0927`** | `+0.8926` / `-0.5174` | `0.00` | **`10.95`** | Term deposit repricing & calibrated unsecured retail credit |
| **Reliance Ind.** (`RELIANCE.NS`) | `+0.8909` | `-0.5925` | **`+1.4833`** | `+0.9167` / `-0.5698` | `0.21` | **`11.82`** | O2C refining crack volatility & retail store rationalization |
| **TCS** (`TCS.NS`) | `+0.7890` | `-0.7482` | **`+1.5372`** | `+0.8888` / `-0.8780` | `0.00` | **`11.78`** | GenAI productivity pass-backs & North America discretionary lag |

### 3.2 90-Sentence Human Gold-Standard Validation & 0%-Hallucination Quote Verification
- **90-Sentence FinBERT Validation Benchmark (`01_data/cleaned/human_benchmark_90_scored.csv`):**
  - **Overall Accuracy:** **`95.56%`** (`86 / 90` sentences correctly classified) | **Macro-F1 Score:** **`0.9555`** | **Cohen's Kappa ($\kappa$):** **`0.9333`** (*Almost Perfect Agreement*).
  - **Per-Company Accuracy:** `ICICI Bank = 93.33%` (`28/30`), `Reliance Industries = 96.67%` (`29/30`), `TCS = 96.67%` (`29/30`).
  - **3x3 Confusion Matrix** (Rows = Human `[Pos, Neu, Neg]`, Cols = FinBERT `[Pos, Neu, Neg]`): `[[30, 0, 0], [0, 29, 1], [3, 0, 27]]`. The 4 edge-case divergences occur when management pairs cautious qualifiers (`"calibrated"`, `"moderating"`) with positive financial milestones, causing FinBERT to weight the positive financial metric over the hedging qualifier.
- **Deterministic Verbatim Footnote Verifier (`verified_quotes.json`):** `12 / 12` structured JSON extractions across Guidance, Capex Commitments, Contingent Liabilities, and Ind AS 24 RPTs achieved a **`100.00%` exact normalized substring match** (`difflib.SequenceMatcher` ratio = `1.0000`, **`0.00%` hallucination rate**).

### 3.3 150-Headline Behavioral Bias Distribution vs. Fundamental Valuation Dislocation

| Company | Net Media Sentiment | Dominant Media Bias Bucket | Hype / FOMO | Recency Bias | Loss Aversion | Neutral / Factual | 1Y Street EPS Rev | DCF/DDM Upside & Dislocation Verdict |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **ICICI Bank** | `+0.2217` | **Hype / FOMO (`58%`)** | **`29` (`58%`)** | `4` (`8%`) | `3` (`6%`) | `14` (`28%`) | `+4.80%` | **`+14.13%` (ACCUMULATE):** Consensus quality leader; buy on dips rather than chasing FOMO breakouts. |
| **Reliance** | `-0.2879` | **Recency Bias (`34%`)** | `5` (`10%`) | **`17` (`34%`)** | `9` (`18%`) | `19` (`38%`) | `-1.40%` | **`+21.91%` (BUY):** Media extrapolates short-term O2C cracks, missing Jio/Retail FCF inflection. |
| **TCS** | `-0.3438` | **Loss Aversion (`50%`)** | `6` (`12%`) | `5` (`10%`) | **`25` (`50%`)** | `14` (`28%`) | `-2.10%` | **`+16.10%` (ACCUMULATE):** AI disruption panic prices in 5.13% growth vs. 8.50% TCV-backed reality. |

### 3.4 Technical Momentum & 1-Year (252-Day, 1,000-Path) GBM Monte Carlo Price Distribution (`seed=42`)

| Stock (`Ticker`) | Spot CMP | 50-DMA / 200-DMA | 14-Day RSI & Regime | MACD / Signal (Hist) | MC P10 (INR) | MC P25 (INR) | **MC Median P50 (INR)** | MC P75 (INR) | MC P90 (INR) | DCF Target Percentile in MC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`ICICIBANK.NS`** | `₹1,398.00` | `₹1,377.99` / `₹1,347.15` | `56.97` (Bullish) | `8.36` / `4.59` (`+3.76`) | `₹1,201.99` | `₹1,354.09` | **`₹1,553.35` (`+11.11%`)** | `₹1,769.83` | `₹1,983.98` | `₹1,595.50` (~55th Pct) |
| **`RELIANCE.NS`** | `₹1,164.90` | `₹1,235.88` / `₹1,326.19` | `40.27` (Weak/Oversold) | `-15.64` / `-16.00` (`+0.36`) | `₹850.14` | `₹978.25` | **`₹1,125.15` (`-3.41%`)** | `₹1,318.05` | `₹1,512.87` | `₹1,420.14` (~82nd Pct) |
| **`TCS.NS`** | `₹2,502.60` | `₹2,255.25` / `₹2,393.67` | `67.56` (Bullish) | `91.08` / `74.85` (`+16.22`) | `₹1,759.28` | `₹2,010.15` | **`₹2,354.84` (`-5.90%`)** | `₹2,774.45` | `₹3,134.15` | `₹2,905.55` (~81st Pct) |

---

## PAGE 4: QUANTITATIVE PORTFOLIO OPTIMIZATION, UTILITY ALLOCATION, 20Y SIP & 4-RATIO EVALUATION

### 4.1 Blended Forward Expected Returns & Mean-Variance Optimization (`Rf = 91D T-Bill @ 6.65%`)
To prevent backward-looking cyclical derating (`Reliance +0.27%`, `TCS -3.77%` historical log drift) from distorting forward asset allocation, we blend `50% CAPM Ke + 50% DCF/DDM 5Y Implied IRR`, yielding forward expected returns of **`13.99%` (`ICICIBANK.NS`)**, **`15.55%` (`RELIANCE.NS`)**, and **`13.28%` (`TCS.NS`)**. Solving for the **Max-Sharpe Tangency Portfolio** (`SLSQP`) yields weights of **`38.90%` ICICI Bank**, **`37.91%` Reliance**, and **`23.19%` TCS**, achieving $E(R_p) = 14.42\%$, $\sigma_p = 15.74\%$, $\beta_p = 0.9874$, and **Sharpe Ratio = `0.4935`** (outperforming the Nifty 50 forward Sharpe of `0.4328`).

### 4.2 10-Question Risk Profiler, Prudence Override Rule & Utility-Optimal Baskets ($U = E(R_c) - 0.5 A \sigma_c^2$)
Our 10-question risk profiler scores **Section A (Financial Ability: 5–20)** and **Section B (Psychological Willingness: 5–20)**. If $|A - B| \ge 6$, the **Prudence Override Rule** sets $R_{\text{eff}} = 2 \times \min(\text{Sec A}, \text{Sec B})$ and maps $A = 10 - 0.3(R_{\text{eff}} - 10)$ to compute optimal risky share $y^* = \min\left(1.0, \frac{E(R_{\text{tan}}) - R_f}{A \sigma_{\text{tan}}^2}\right)$:

| Investor Basket Profile | Sec A / Sec B | Effective $R_{\text{eff}}$ | Risk Aversion $A$ | Risky Equity $y^*$ | 91D T-Bill ($1-y^*$) | `w_ICICI` | `w_Reliance` | `w_TCS` | Complete $E(R_c)$ | Complete $\sigma_c$ | Complete $\beta_c$ | Utility $U$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Aggressive Basket** | `18` / `18` | `36` | **`2.20`** | **`100.00%`** | `0.00%` | `38.90%` | `37.91%` | `23.19%` | **`14.42%`** | `15.74%` | `0.9874` | `0.1169` |
| **Balanced Basket** | `14` / `13` | `27` | **`4.90`** | **`64.00%`** | `36.00%` | `24.90%` | `24.26%` | `14.85%` | **`11.62%`** | `10.07%` | `0.6320` | `0.0914` |
| **Defensive Basket** | `8` / `7` | `15` | **`8.50`** | **`36.90%`** | `63.10%` | `14.35%` | `13.99%` | `8.56%` | **`9.52%`** | `5.81%` | `0.3643` | `0.0808` |
| **Prudence-Override Case** | `9` / `18` ($\Delta=9$) | **`18` (Overridden)** | **`7.60`** | **`41.27%`** | `58.73%` | `16.05%` | `15.64%` | `9.57%` | **`9.85%`** | `6.49%` | `0.4075` | `0.0825` |

### 4.3 20-Year Step-Up SIP Lifecycle Glide Path (`₹25,000/mo` Initial, `+10%` Annual Step-Up)
Across a 240-month horizon (`Age 25–44`), an investor contributing `₹25,000/mo` stepped up by `10%/year` invests **`₹1.7182 Cr`** cumulatively (`₹1,71,82,500`) across three automated lifecycle phases: **Years 1–8 in Aggressive (`A=2.20`, `100%` Equity)** → **Years 9–15 in Balanced (`A=4.90`, `64.0%` Equity)** → **Years 16–20 in Defensive (`A=8.50`, `36.9%` Equity)**. This dynamic glide path compounds to a **Deterministic Terminal Corpus of `₹4.3241 Cr` (`2.52x` multiple)** and a **Monte Carlo Median (`P50`) of `₹4.1962 Cr`** (`P10 = ₹3.1765 Cr`, `P90 = ₹5.7370 Cr`), protecting late-career wealth from sequence-of-returns crash risk.

### 4.4 Mandatory 4-Metric Portfolio Evaluation Table & Strategic Conclusion

| Portfolio / Benchmark | Portfolio $\beta_p$ | Tracking Error | Fwd $E(R_p)$ | Fwd $\sigma_p$ | **1. Sharpe Ratio** | **2. Treynor Measure** | **3. Jensen's $\alpha$** | **4. Information Ratio** | 5Y Backtest Value of `₹100` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Max-Sharpe Tangency / Aggressive ($A=2.20$)** | `0.9874` | `7.76%` | `14.42%` | `15.74%` | **`0.4935`** | **`0.0786`** | **`+1.84%`** | **`+0.2274`** | `₹121.24` |
| **Balanced Utility Basket ($A=4.90$)** | `0.6320` | `7.12%` | `11.62%` | `10.07%` | **`0.4935`** | **`0.0786`** | **`+1.18%`** | `-0.1446` | `₹127.20` |
| **Defensive Utility Basket ($A=8.50$)** | `0.3643` | `9.26%` | `9.52%` | `5.81%` | **`0.4940`** | **`0.0788`** | **`+0.68%`** | `-0.3378` | `₹131.88` |
| **Global Minimum Variance (GMV)** | `0.9581` | `7.96%` | `14.17%` | `15.48%` | `0.4858` | `0.0785` | `+1.77%` | `+0.1906` | `₹122.92` |
| **Equal-Weight (`1/3`, `1/3`, `1/3`)** | `0.9657` | `8.10%` | `14.27%` | `15.64%` | `0.4875` | `0.0789` | `+1.83%` | `+0.2004` | `₹115.07` |
| **Nifty 50 Benchmark (`^NSEI`)** | `1.0000` | `0.00%` | `12.65%` | `13.86%` | `0.4328` | `0.0600` | `+0.00%` | `0.0000` | `₹128.58` |

- **Final Investment Verdict & Limitations:** We recommend **BUY on Reliance Industries (`+21.91%` upside)** as 5G capex moderation unlocks free cash flow masked by media recency bias, **ACCUMULATE on TCS (`+16.10%` upside)** where AI loss aversion has compressed market-implied growth to `5.13%`, and **ACCUMULATE on ICICI Bank (`+14.13%` upside)** as a core compounder (`38.90%` MVO weight). Key limitations include FinBERT's sensitivity to double-barreled hedging phrasing (`4/90` benchmark misses), GBM's log-normal constant-volatility assumption, and static 5-year OLS Betas during regime shifts.
