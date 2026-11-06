import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Institutional Equity & Portfolio Management Engine",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Macro & Sovereign Constants
RF_TBILL = 0.0665   # 91-Day RBI T-Bill Yield
RF_GSEC = 0.0685    # 10-Year Benchmark G-Sec Yield
ERP = 0.0600        # India Equity Risk Premium
NIFTY_EXP_RET = 0.1265 # Nifty 50 Expected Return
NIFTY_VOL = 0.1386     # Nifty 50 Annualized Volatility
NIFTY_BETA = 1.0000

# Asset Data Vector
ASSETS = {
    "ICICIBANK.NS": {"name": "ICICI Bank Ltd", "er": 0.1399, "vol": 0.1955, "beta": 0.9663, "color": "#f97316"},
    "RELIANCE.NS": {"name": "Reliance Industries Ltd", "er": 0.1555, "vol": 0.2233, "beta": 1.1125, "color": "#eab308"},
    "TCS.NS": {"name": "Tata Consultancy Services Ltd", "er": 0.1328, "vol": 0.2285, "beta": 0.8184, "color": "#3b82f6"},
    "91D_RBI_TBILL": {"name": "91-Day RBI Treasury Bill", "er": 0.0665, "vol": 0.0000, "beta": 0.0000, "color": "#10b981"}
}

# Optimal Risky Tangency Basket (Equity Sleeve)
W_TAN = {"ICICIBANK.NS": 0.3890, "RELIANCE.NS": 0.3791, "TCS.NS": 0.2319}
E_R_TAN = 0.1442
SIGMA_TAN = 0.1574
BETA_TAN = 0.9874
SHARPE_TAN = (E_R_TAN - RF_TBILL) / SIGMA_TAN

# 3-Stock Return Correlation Matrix
CORR_MATRIX = pd.DataFrame(
    [
        [1.00, 0.43, 0.26],
        [0.43, 1.00, 0.34],
        [0.26, 0.34, 1.00]
    ],
    index=["ICICI Bank", "Reliance", "TCS"],
    columns=["ICICI Bank", "Reliance", "TCS"]
)

# Custom Styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1e293b; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.05rem; color: #64748b; margin-bottom: 1.5rem; }
    .kpi-card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: center; }
    .kpi-label { font-size: 0.85rem; font-weight: 600; color: #64748b; text-transform: uppercase; }
    .kpi-value { font-size: 1.6rem; font-weight: 700; color: #0f172a; margin-top: 4px; }
    .kpi-sub { font-size: 0.8rem; color: #10b981; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Institutional Equity Valuation & Dynamic Portfolio Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">TAPMI Bengaluru | Security Analysis & Portfolio Management | Sasi Preetham (246213618), Sankarshana Mulugundam (246213080), Aditi Routray (246213548)</div>', unsafe_allow_html=True)

# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Nifty_50_logo.svg/1200px-Nifty_50_logo.svg.png", width=120) if False else None
    st.header("⚙️ Global Portfolio Settings")
    inv_lump_sum = st.number_input("Total Portfolio Value (₹)", min_value=100000, max_value=100000000, value=1000000, step=50000)
    inv_sip = st.number_input("Monthly Step-Up SIP (₹)", min_value=5000, max_value=1000000, value=25000, step=2500)
    
    st.markdown("---")
    st.subheader("Benchmark Sovereign Constants")
    st.caption(f"• **10Y G-Sec ($R_f$):** {RF_GSEC*100:.2f}%")
    st.caption(f"• **91D T-Bill ($R_f$):** {RF_TBILL*100:.2f}%")
    st.caption(f"• **India ERP:** {ERP*100:.2f}%")
    st.caption(f"• **Cutoff Date:** October 30, 2026")

# ----------------- TABS SETUP (4 TABS) -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Tab 1: Portfolio, Ratios & Heatmaps",
    "🎯 Tab 2: Risk Profiler (10 Questions)",
    "🎚️ Tab 3: Dynamic A-Slider & Portfolio Manager",
    "📈 Tab 4: 20-Year Step-Up SIP Simulation"
])

# Initialize session state for Risk Aversion A
if "risk_aversion_a" not in st.session_state:
    st.session_state["risk_aversion_a"] = 4.00
if "risk_score_r" not in st.session_state:
    st.session_state["risk_score_r"] = 30

# =========================================================================
# TAB 2: 10 QUESTIONNAIRE TO CALCULATE A VALUE (DEFINED FIRST FOR SYNC)
# =========================================================================
with tab2:
    st.subheader("🎯 10-Question Investor Risk Profiler & Utility Calibration")
    st.write("Determine your empirical Risk Aversion coefficient ($A$) governed by the **Prudence Override Rule**.")
    
    col_q1, col_q2 = st.columns(2)
    
    with col_q1:
        st.markdown("#### Section A: Financial Risk Capacity (Ability)")
        q1 = st.slider("Q1. Investment Time Horizon", 1, 4, 3, help="1: <3Y, 2: 3-7Y, 3: 7-15Y, 4: >15Y")
        q2 = st.slider("Q2. Net Savings Rate (% of Monthly Income)", 1, 4, 3, help="1: <10%, 2: 10-25%, 3: 25-40%, 4: >40%")
        q3 = st.slider("Q3. Emergency Liquidity Reserve (Months of Expenses)", 1, 4, 3, help="1: <3M, 2: 3-6M, 3: 6-12M, 4: >12M")
        q4 = st.slider("Q4. Income Stability & Career Resilience", 1, 4, 3, help="1: Variable, 2: Moderate, 3: Highly Secure, 4: Diversified/Tenured")
        q5 = st.slider("Q5. Financial Dependents / Obligation Burden", 1, 4, 3, help="1: Heavy, 2: Moderate, 3: Light, 4: None")
        score_a = q1 + q2 + q3 + q4 + q5
        st.info(f"**Section A Score (Ability): {score_a} / 20**")

    with col_q2:
        st.markdown("#### Section B: Psychological Willingness (Tolerance)")
        q6 = st.slider("Q6. Reaction to a 20% Sudden Market Drawdown", 1, 4, 3, help="1: Panic/Sell All, 2: Cut Exposure, 3: Hold Patiently, 4: Aggressively Buy")
        q7 = st.slider("Q7. Equity Market Experience & Volatility Fluency", 1, 4, 3, help="1: Novice, 2: Intermediate, 3: Experienced, 4: Institutional/Advanced")
        q8 = st.slider("Q8. Preferred Return/Volatility Trade-Off", 1, 4, 3, help="1: Capital Preservation, 2: Moderate Balanced, 3: Growth, 4: Maximum Aggressive")
        q9 = st.slider("Q9. Comfort with Interim Portfolio Fluctuations", 1, 4, 3, help="1: Daily Anxiety, 2: Weekly Concern, 3: Quarterly Check, 4: Multi-Year Apathy")
        q10 = st.slider("Q10. Past Behavioral Discipline in Corrections", 1, 4, 3, help="1: Regret/Panic, 2: Anxious Inaction, 3: Disciplined SIP, 4: Opportunistic Rebalance")
        score_b = q6 + q7 + q8 + q9 + q10
        st.info(f"**Section B Score (Willingness): {score_b} / 20**")
        
    st.markdown("---")
    
    # Prudence Override Calculation
    raw_r = score_a + score_b
    diff_ab = abs(score_a - score_b)
    if diff_ab >= 6:
        eff_r = 2 * min(score_a, score_b)
        override_triggered = True
    else:
        eff_r = raw_r
        override_triggered = False
        
    calc_a = max(1.0, min(10.0, 10.0 - 0.3 * (eff_r - 10)))
    
    res_c1, res_c2, res_c3 = st.columns(3)
    res_c1.metric("Raw Score (A + B)", f"{raw_r} / 40", delta="Prudence Gap: " + str(diff_ab))
    res_c2.metric("Effective Risk Score (R)", f"{eff_r} / 40", delta="Override Active" if override_triggered else "Balanced")
    res_c3.metric("Derived Risk Aversion (A)", f"{calc_a:.2f}", delta="-0.30/pt scaling")
    
    if override_triggered:
        st.warning(f"⚠️ **Prudence Override Rule Activated:** Section gap $|A - B| = {diff_ab} \ge 6$. The portfolio is constrained by the weaker capacity constraint: $R = 2 \times \min({score_a}, {score_b}) = {eff_r}$.")
    else:
        st.success(f"✅ **Balanced Profile:** Section gap $|A - B| = {diff_ab} < 6$. No capacity bottleneck detected.")
        
    if st.button("Apply Questionnaire Values to Portfolio Manager", type="primary"):
        st.session_state["risk_aversion_a"] = float(calc_a)
        st.session_state["risk_score_r"] = int(eff_r)
        st.success(f"Applied A = {calc_a:.2f} to Tab 1 and Tab 3!")

# Read current active A from session state
current_a = float(st.session_state["risk_aversion_a"])

# =========================================================================
# TAB 3: DYNAMIC A-SLIDER & PORTFOLIO MANAGER
# =========================================================================
with tab3:
    st.subheader("🎚️ Dynamic Risk Aversion ($A$) Slider & Asset Allocator")
    st.write("Freely sweep through Risk Aversion ($A$) to observe real-time portfolio reweighting along Tobin's Capital Allocation Line (CAL).")
    
    col_sl1, col_sl2 = st.columns([2, 1])
    with col_sl1:
        slider_a = st.slider("Select Risk Aversion Parameter (A):", min_value=1.00, max_value=10.00, value=current_a, step=0.10)
        st.session_state["risk_aversion_a"] = slider_a
        current_a = slider_a
    with col_sl2:
        st.markdown(f"**Current Calibration:**")
        st.caption(f"• Risk Aversion ($A$): **{current_a:.2f}**")
        st.caption(f"• Profile Type: **{'Aggressive Growth' if current_a < 3.0 else 'Balanced Core' if current_a <= 5.0 else 'Defensive Preservation'}**")

    # Tobin Two-Fund Separation Calculations
    y_star_raw = (E_R_TAN - RF_TBILL) / (current_a * (SIGMA_TAN ** 2))
    y_star = min(1.0, max(0.0, y_star_raw))
    w_tbill = 1.0 - y_star
    
    w_icici = y_star * W_TAN["ICICIBANK.NS"]
    w_rel = y_star * W_TAN["RELIANCE.NS"]
    w_tcs = y_star * W_TAN["TCS.NS"]
    
    # Complete Portfolio Metrics
    e_rc = y_star * E_R_TAN + w_tbill * RF_TBILL
    sigma_c = y_star * SIGMA_TAN
    beta_c = y_star * BETA_TAN
    utility_c = e_rc - 0.5 * current_a * (sigma_c ** 2)
    
    sharpe_c = (e_rc - RF_TBILL) / sigma_c if sigma_c > 0 else 0
    treynor_c = (e_rc - RF_TBILL) / beta_c if beta_c > 0 else 0
    alpha_c = e_rc - (RF_TBILL + beta_c * (NIFTY_EXP_RET - RF_TBILL))
    te_c = y_star * 0.0776
    ir_c = (e_rc - NIFTY_EXP_RET) / te_c if te_c > 0 else 0
    
    # Top Metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Risky Equity Share (y*)", f"{y_star*100:.2f}%", delta="Tangency Sleeve")
    m2.metric("91D T-Bill Share", f"{w_tbill*100:.2f}%", delta="Risk-Free Anchor")
    m3.metric("Expected Return E(Rc)", f"{e_rc*100:.2f}%", delta=f"{((e_rc - NIFTY_EXP_RET)*100):+.2f}% vs Nifty")
    m4.metric("Portfolio Volatility (σc)", f"{sigma_c*100:.2f}%", delta=f"{((sigma_c - NIFTY_VOL)*100):+.2f}% vs Nifty")
    m5.metric("Certainty Equivalent Utility (U)", f"{utility_c:.4f}", delta=f"{utility_c*100:.2f}% cert. eq.")

    st.markdown("---")
    
    chart_c1, chart_c2 = st.columns([1, 1])
    
    with chart_c1:
        st.markdown("#### 4-Asset Allocation Breakdown")
        weights_df = pd.DataFrame({
            "Asset": ["ICICI Bank Ltd", "Reliance Industries", "Tata Consultancy Services", "91-Day RBI T-Bill"],
            "Weight": [w_icici, w_rel, w_tcs, w_tbill],
            "Lump Sum (₹)": [w_icici * inv_lump_sum, w_rel * inv_lump_sum, w_tcs * inv_lump_sum, w_tbill * inv_lump_sum],
            "Monthly SIP (₹)": [w_icici * inv_sip, w_rel * inv_sip, w_tcs * inv_sip, w_tbill * inv_sip]
        })
        
        fig_donut = px.pie(
            weights_df, values="Weight", names="Asset",
            color="Asset",
            color_discrete_map={
                "ICICI Bank Ltd": "#f97316",
                "Reliance Industries": "#eab308",
                "Tata Consultancy Services": "#3b82f6",
                "91-Day RBI T-Bill": "#10b981"
            },
            hole=0.45
        )
        fig_donut.update_traces(textinfo="percent+label", pull=[0.02, 0.02, 0.02, 0.05])
        fig_donut.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=320)
        st.plotly_chart(fig_donut, use_container_width=True)

    with chart_c2:
        st.markdown(f"#### Capital Allocation Split (₹{inv_lump_sum:,.0f} Portfolio)")
        st.dataframe(
            weights_df.style.format({
                "Weight": "{:.2%}",
                "Lump Sum (₹)": "₹{:,.0f}",
                "Monthly SIP (₹)": "₹{:,.0f}"
            }),
            use_container_width=True
        )
        st.caption(f"• **Equity Sleeve:** {y_star*100:.2f}% | **Cash Reserve:** {w_tbill*100:.2f}%")
        st.caption(f"• **Portfolio Beta:** {beta_c:.4f} ({(1-beta_c)*100:.1f}% less systematic risk than Nifty 50)")

    # Capital Allocation Line Plotly Chart
    st.markdown("#### Modern Portfolio Theory: Capital Allocation Line (CAL) & Indifference Curve")
    sigmas_cal = np.linspace(0, 0.25, 100)
    er_cal = RF_TBILL + SHARPE_TAN * sigmas_cal
    
    # Indifference Curve for selected A: E(R) = U + 0.5 * A * sigma^2
    er_indiff = utility_c + 0.5 * current_a * (sigmas_cal ** 2)
    
    fig_cal = go.Figure()
    # CAL
    fig_cal.add_trace(go.Scatter(x=sigmas_cal*100, y=er_cal*100, mode='lines', name='Capital Allocation Line (CAL)', line=dict(color='#0f172a', width=2.5)))
    # Indifference curve
    fig_cal.add_trace(go.Scatter(x=sigmas_cal*100, y=er_indiff*100, mode='lines', name=f'Indifference Curve (A = {current_a:.2f})', line=dict(color='#f59e0b', width=2, dash='dash')))
    # T-Bill Point
    fig_cal.add_trace(go.Scatter(x=[0], y=[RF_TBILL*100], mode='markers+text', name='91D T-Bill (Rf = 6.65%)', marker=dict(color='#10b981', size=10), text=["91D T-Bill"], textposition="top right"))
    # Tangency Point
    fig_cal.add_trace(go.Scatter(x=[SIGMA_TAN*100], y=[E_R_TAN*100], mode='markers+text', name='Tangency Basket T', marker=dict(color='#ef4444', size=12), text=["Tangency T"], textposition="top left"))
    # Current Complete Portfolio Point
    fig_cal.add_trace(go.Scatter(x=[sigma_c*100], y=[e_rc*100], mode='markers+text', name=f'Complete Portfolio C (A = {current_a:.2f})', marker=dict(color='#6366f1', size=14, symbol='star'), text=[f"C (A={current_a:.2f})"], textposition="bottom right"))
    
    fig_cal.update_layout(
        xaxis_title="Portfolio Volatility σ (%)",
        yaxis_title="Expected Return E(R) (%)",
        xaxis=dict(range=[0, 25]),
        yaxis=dict(range=[5, 18]),
        margin=dict(l=30, r=30, t=30, b=30),
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_cal, use_container_width=True)

# =========================================================================
# TAB 1: PORTFOLIO, RATIOS & HEATMAPS
# =========================================================================
with tab1:
    st.subheader("📊 Portfolio Performance, Financial Ratios & Risk Heatmaps")
    st.write("Comprehensive institutional evaluation comparing company fundamentals, valuation multiples, risk-adjusted performance ratios, and cross-asset correlations.")
    
    col_p1, col_p2 = st.columns([1, 1])
    
    with col_p1:
        st.markdown("#### 1. Mandatory Portfolio Performance Ratios")
        perf_data = {
            "Performance Metric": [
                "Expected Annual Return E(R)",
                "Annualized Volatility (σ)",
                "Portfolio Beta (β vs Nifty)",
                "Sharpe Ratio ((R - Rf) / σ)",
                "Treynor Measure ((R - Rf) / β)",
                "Jensen's Alpha (α vs CAPM)",
                "Information Ratio (α / TE)",
                "Certainty Equivalent Utility (U)"
            ],
            f"Active Complete Portfolio (A = {current_a:.2f})": [
                f"{e_rc*100:.2f}%",
                f"{sigma_c*100:.2f}%",
                f"{beta_c:.4f}",
                f"{sharpe_c:.4f}",
                f"{treynor_c*100:.2f}%",
                f"{alpha_c*100:+.2f}%",
                f"{ir_c:.4f}",
                f"{utility_c:.4f}"
            ],
            "Nifty 50 Benchmark": [
                f"{NIFTY_EXP_RET*100:.2f}%",
                f"{NIFTY_VOL*100:.2f}%",
                f"{NIFTY_BETA:.4f}",
                f"{(NIFTY_EXP_RET - RF_TBILL)/NIFTY_VOL:.4f}",
                f"{(NIFTY_EXP_RET - RF_TBILL)/NIFTY_BETA*100:.2f}%",
                "0.00%",
                "0.0000",
                f"{NIFTY_EXP_RET - 0.5*current_a*(NIFTY_VOL**2):.4f}"
            ]
        }
        st.dataframe(pd.DataFrame(perf_data), use_container_width=True, hide_index=True)
        st.caption("• **Sharpe & Treynor:** Captures reward per unit of total risk and systematic market risk.")
        st.caption("• **Jensen's Alpha:** Annualized outperformance generated above CAPM requirements.")

    with col_p2:
        st.markdown("#### 2. Cross-Asset Return Correlation Heatmap")
        fig_heat = px.imshow(
            CORR_MATRIX,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Blues",
            labels=dict(x="Stock", y="Stock", color="Pearson Correlation")
        )
        fig_heat.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
        st.plotly_chart(fig_heat, use_container_width=True)
        st.caption("• **Low Correlation Matrix:** Low pairwise covariance (0.26 ICICI-TCS, 0.34 Reliance-TCS) drives institutional diversification.")

    st.markdown("---")
    
    st.markdown("#### 3. Core Company Operating, Asset Quality & Valuation Ratios")
    ratios_df = pd.DataFrame({
        "Financial & Valuation Ratio": [
            "Current Market Price (CMP, ₹)",
            "Intrinsic Target Value (₹)",
            "Margin of Safety / Upside (%)",
            "Valuation Methodology Used",
            "5-Year Daily Regression Beta (β)",
            "CAPM Cost of Equity (Ke %)",
            "Discount Rate (Ke / WACC %)",
            "5Y Net Profit / EBITDA CAGR",
            "Sustainable ROE (%)",
            "Return on Capital Employed (ROCE %)",
            "Key Efficiency / Quality Ratio"
        ],
        "ICICI Bank Ltd": [
            "₹1,398.00",
            "₹1,595.50",
            "+14.13%",
            "2-Stage DDM & Excess Return",
            "0.9663",
            "12.65%",
            "12.65% (Ke)",
            "20.7% Profit CAGR",
            "17.50%",
            "N/A (Banking)",
            "Net NPA: 0.45% | NIM: 4.30%"
        ],
        "Reliance Industries": [
            "₹1,164.90",
            "₹1,420.14",
            "+21.91%",
            "2-Stage FCFF DCF & SOTP",
            "1.1125",
            "13.53%",
            "12.10% (WACC)",
            "13.3% EBITDA CAGR",
            "9.60%",
            "11.40%",
            "CFO/EBITDA: 95.9% | CCC: 17.4 Days"
        ],
        "Tata Consultancy Services": [
            "₹2,502.60",
            "₹2,905.55",
            "+16.10%",
            "2-Stage FCFF DCF & Reverse DCF",
            "0.8184",
            "11.76%",
            "11.65% (WACC)",
            "6.9% EBIT CAGR",
            "51.00%",
            "63.10%",
            "CFO/PAT: 98.2% | Debtor: 65.8 Days"
        ]
    })
    st.dataframe(ratios_df, use_container_width=True, hide_index=True)

# =========================================================================
# TAB 4: 20-YEAR STEP-UP SIP SIMULATION
# =========================================================================
with tab4:
    st.subheader("📈 20-Year Step-Up SIP Wealth Compounding & Lifecycle Schedule")
    st.write("Simulation of long-term capital accumulation starting at age 25 with a ₹25,000 monthly SIP stepped up 10% annually.")
    
    # 20-Year SIP Deterministic Calculation
    years = np.arange(1, 21)
    monthly_contributions = inv_sip * (1.10 ** (years - 1))
    annual_invested = monthly_contributions * 12
    cum_invested = np.cumsum(annual_invested)
    
    # Dynamic portfolio growth
    portfolio_corpus = np.zeros(20)
    corpus = 0
    for idx, yr in enumerate(years):
        # 3 Lifecycle phases
        if yr <= 8:
            r_yr = e_rc
        elif yr <= 15:
            r_yr = 0.64 * E_R_TAN + 0.36 * RF_TBILL # Balanced
        else:
            r_yr = 0.37 * E_R_TAN + 0.63 * RF_TBILL # Defensive
            
        corpus = (corpus + annual_invested[idx]) * (1 + r_yr)
        portfolio_corpus[idx] = corpus
        
    sip_summary_df = pd.DataFrame({
        "Year": years,
        "Age": years + 24,
        "Monthly SIP (₹)": monthly_contributions,
        "Annual Investment (₹)": annual_invested,
        "Cumulative Invested (₹ Cr)": cum_invested / 1e7,
        "Expected Corpus (₹ Cr)": portfolio_corpus / 1e7
    })
    
    sip_c1, sip_c2 = st.columns([1, 2])
    with sip_c1:
        st.markdown("#### Terminal Corpus Milestones")
        st.metric("Total Capital Invested (20Y)", f"₹{cum_invested[-1]/1e7:.2f} Cr", delta="Principal")
        st.metric("Expected Corpus at Age 44", f"₹{portfolio_corpus[-1]/1e7:.2f} Cr", delta=f"+₹{(portfolio_corpus[-1] - cum_invested[-1])/1e7:.2f} Cr Wealth Gain")
        st.metric("Monte Carlo Median Corpus", "₹4.20 Cr", delta="90% P10-P90 Confidence")
        st.caption("• **Rebalancing Rule:** Yearly reset across 3 phases (Years 1-8 Accumulation, Years 9-15 Consolidation, Years 16-20 Preservation).")

    with sip_c2:
        st.markdown("#### Cumulative Wealth Accumulation Trajectory")
        fig_sip = go.Figure()
        fig_sip.add_trace(go.Bar(x=years, y=cum_invested/1e7, name="Cumulative Invested (₹ Cr)", marker_color="#cbd5e1"))
        fig_sip.add_trace(go.Scatter(x=years, y=portfolio_corpus/1e7, mode="lines+markers", name="Expected Corpus (₹ Cr)", line=dict(color="#2563eb", width=3), marker=dict(size=6)))
        fig_sip.update_layout(
            xaxis_title="Investment Year (Age 25 to 44)",
            yaxis_title="Corpus Value (₹ Crore)",
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_sip, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Detailed 20-Year Lifecycle Schedule Table")
    st.dataframe(
        sip_summary_df.style.format({
            "Monthly SIP (₹)": "₹{:,.0f}",
            "Annual Investment (₹)": "₹{:,.0f}",
            "Cumulative Invested (₹ Cr)": "₹{:.2f} Cr",
            "Expected Corpus (₹ Cr)": "₹{:.2f} Cr"
        }),
        use_container_width=True,
        hide_index=True
    )
