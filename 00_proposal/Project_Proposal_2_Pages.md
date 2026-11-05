# Project Proposal: Beyond the Consensus

**Project Title:** *Beyond the Consensus: An AI-Augmented Fundamental Valuation of Core Indian Blue Chips with Risk-Calibrated Portfolio Construction*  
**Team Members:**
1. **Sankarshana Mulugundam (`246213080`)** — *Project Lead, Quantitative Portfolio Architect & ICICI Bank Lead*
2. **Aditi Routray (`246213548`)** — *AI Pipeline, FinBERT Sentiment & Behavioral Bias Lead & Reliance Industries Lead*
3. **Sasi (`246213618`)** — *Fundamental Valuation, DCF/DDM & Forensic Accounting Lead & TCS Lead*

---

## 1. Research Objective & Three-Pillar Coverage Universe
We propose an end-to-end fundamental valuation, AI-driven natural language processing (`ProsusAI/finbert`), and utility-calibrated portfolio optimization study across three flagship Nifty 50 companies representing distinct macroeconomic engines of India:
- **ICICI Bank (`ICICIBANK.NS`):** Private Banking & Domestic Credit Compounder (`2-Stage DDM & Excess Equity Return Model`).
- **Reliance Industries (`RELIANCE.NS`):** Energy, Telecom (`Jio`) & Organized Retail Conglomerate (`Consolidated 2-Stage FCFF DCF & Segmental SOTP`).
- **Tata Consultancy Services (`TCS.NS`):** Global IT Services & Enterprise AI Leader (`2-Stage FCFF DCF & Reverse DCF Implied Growth Model`).

## 2. Locked Methodological Parameters (`config.json`)
- **Market Sample Window:** 5 Years of Daily Adjusted Close Prices (`2021-10-31` to `2026-10-30`, `1,236` trading days).
- **Risk-Free Rates:** `6.85%` (10-Year India G-Sec for long-duration DCF/DDM discounting) and `6.65%` (91-Day RBI T-Bill for money-market portfolio allocation & Sharpe ratio).
- **India Equity Risk Premium (ERP):** `6.00%` | **Effective Corporate Tax Rate:** `25.17%`.
- **AI & Stochastic Modules:** Live `ProsusAI/finbert` across 24 quarterly earnings calls (`Q1_FY25–Q4_FY26`), 90 human gold-standard validation sentences, 12 verbatim-verified annual report footnotes (`0%` hallucination check), 150 news headlines, and 1,000-path GBM Monte Carlo simulations (`seed=42`).
- **Portfolio Architecture:** Blended `50% CAPM Ke + 50% DCF/DDM IRR` expected returns, Markowitz MVO (`Max-Sharpe Tangency` & `GMV`), 10-question risk profiler with **Prudence Override Rule** (`|SecA - SecB| >= 6`), 20-year Step-Up SIP (`₹25,000/mo`, `+10%/yr`), and evaluation across **Sharpe, Treynor, Jensen's Alpha, and Information Ratio**.
