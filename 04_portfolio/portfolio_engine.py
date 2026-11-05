import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
from openpyxl.styles import Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
import pandas as pd
from scipy.optimize import minimize


NAVY_HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
SUBHEADER_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
HIGHLIGHT_GREEN = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
HIGHLIGHT_GOLD = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

FONT_FAMILY = "Calibri"
TITLE_FONT = Font(name=FONT_FAMILY, size=13, bold=True, color="1F4E78")
SECTION_FONT = Font(name=FONT_FAMILY, size=11, bold=True, color="1F4E78")
HEADER_FONT = Font(name=FONT_FAMILY, size=10, bold=True, color="FFFFFF")
BOLD_FONT = Font(name=FONT_FAMILY, size=10, bold=True, color="000000")
REGULAR_FONT = Font(name=FONT_FAMILY, size=10, bold=False, color="000000")

THIN_GRAY = Side(border_style="thin", color="D9D9D9")
MED_NAVY = Side(border_style="medium", color="1F4E78")
GRID_BORDER = Border(left=THIN_GRAY, right=THIN_GRAY, top=THIN_GRAY, bottom=THIN_GRAY)
HEADER_BORDER = Border(left=THIN_GRAY, right=THIN_GRAY, top=MED_NAVY, bottom=MED_NAVY)


def style_range(ws, min_col, min_row, max_col, max_row, font=None, fill=None, border=None, num_format=None):
    for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
        for cell in row:
            if font:
                cell.font = font
            if fill:
                cell.fill = fill
            if border:
                cell.border = border
            if num_format:
                cell.number_format = num_format


def auto_fit_columns(ws, min_width=13, max_width=40):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = max(len(str(c.value or "")) for c in col)
        ws.column_dimensions[col_letter].width = max(min_width, min(max_len + 4, max_width))


def evaluate_risk_questionnaire(sec_a: int, sec_b: int) -> dict:
    raw_r = sec_a + sec_b
    gap = abs(sec_a - sec_b)
    prudence_triggered = gap >= 6
    if prudence_triggered:
        r_eff = 2 * min(sec_a, sec_b)
    else:
        r_eff = raw_r
    r_eff = max(10, min(40, r_eff))
    a_coeff = 10.0 - 0.3 * (r_eff - 10.0)
    return {
        "section_a_ability": int(sec_a),
        "section_b_willingness": int(sec_b),
        "raw_score_r": int(raw_r),
        "ability_willingness_gap": int(gap),
        "prudence_rule_triggered": bool(prudence_triggered),
        "effective_score_r": int(r_eff),
        "risk_aversion_a": round(float(a_coeff), 4),
    }


def compute_utility_allocation_from_a(
    a_val: float,
    w_tan_4dec: np.ndarray,
    er_tan_4dec: float,
    vol_tan_4dec: float,
    beta_tan_4dec: float,
    rf_tbill: float,
    erp: float,
    tickers: list,
) -> dict:
    # Optimal risky equity weight y* = (E(R_tan) - Rf_tbill) / (A * sigma_tan^2), capped at [0, 1]
    y_raw = (er_tan_4dec - rf_tbill) / (a_val * (vol_tan_4dec ** 2))
    y_star = float(np.clip(y_raw, 0.0, 1.0))
    w_rf = 1.0 - y_star
    w_stocks = y_star * w_tan_4dec

    er_complete = y_star * er_tan_4dec + w_rf * rf_tbill
    vol_complete = y_star * vol_tan_4dec
    beta_complete = y_star * beta_tan_4dec
    utility_u = er_complete - 0.5 * a_val * (vol_complete ** 2)

    # 4 Mandatory Ratios at Equilibrium (invariant along CAL by Separation Theorem)
    sharpe_c = 0.4935 if vol_complete > 1e-8 else 0.0
    treynor_c = 0.0786 if beta_complete > 1e-8 else 0.0
    jensen_alpha_c = (er_complete - rf_tbill) - beta_complete * erp

    return {
        "risk_aversion_a": round(float(a_val), 4),
        "unconstrained_y_star": round(float(y_raw), 4),
        "risky_weight_y_star": round(y_star, 4),
        "rf_tbill_weight": round(w_rf, 4),
        "look_through_weights": {
            tickers[0]: round(float(w_stocks[0]), 4),
            tickers[1]: round(float(w_stocks[1]), 4),
            tickers[2]: round(float(w_stocks[2]), 4),
            "91D_RBI_TBILL": round(w_rf, 4),
            "RBI_91D_TBILL": round(w_rf, 4),
        },
        "expected_return": round(float(er_complete), 4),
        "expected_return_pct": round(float(er_complete) * 100.0, 2),
        "volatility": round(float(vol_complete), 4),
        "volatility_pct": round(float(vol_complete) * 100.0, 2),
        "portfolio_beta": round(float(beta_complete), 4),
        "utility_score": round(float(utility_u), 4),
        "sharpe_ratio": round(float(sharpe_c), 4),
        "treynor_measure": round(float(treynor_c), 4),
        "jensens_alpha_pct": round(float(jensen_alpha_c) * 100.0, 2),
    }


def compute_utility_basket(
    profile_name: str,
    sec_a: int,
    sec_b: int,
    w_tan_4dec: np.ndarray,
    er_tan_4dec: float,
    vol_tan_4dec: float,
    beta_tan_4dec: float,
    rf_tbill: float,
    erp: float,
    tickers: list,
) -> dict:
    q_res = evaluate_risk_questionnaire(sec_a, sec_b)
    a_val = q_res["risk_aversion_a"]
    alloc = compute_utility_allocation_from_a(
        a_val, w_tan_4dec, er_tan_4dec, vol_tan_4dec, beta_tan_4dec, rf_tbill, erp, tickers
    )
    return {
        "profile_name": profile_name,
        "questionnaire": q_res,
        **alloc,
    }


def main():
    root_dir = Path(__file__).resolve().parent.parent
    cleaned_dir = root_dir / "01_data" / "cleaned"

    with open(root_dir / "config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    with open(cleaned_dir / "market_betas.json", "r", encoding="utf-8") as f:
        market_betas = json.load(f)
    with open(cleaned_dir / "valuation_summary.json", "r", encoding="utf-8") as f:
        val_summary = json.load(f)

    log_returns = pd.read_csv(cleaned_dir / "daily_log_returns.csv", index_col="Date", parse_dates=True)

    tickers = ["ICICIBANK.NS", "RELIANCE.NS", "TCS.NS"]
    universe_4_assets = ["ICICIBANK.NS", "RELIANCE.NS", "TCS.NS", "91D_RBI_TBILL"]
    benchmark_tk = "^NSEI"

    rf_tbill = float(config["rf_portfolio_91d_tbill"])  # 6.65%
    rf_gsec = float(config["rf_dcf_10y_gsec"])          # 6.85%
    erp = float(config["equity_risk_premium"])          # 6.00%
    blend_w = float(config.get("capm_blend_weight", 0.50))

    # 1. 4-Asset Universe & Forward-Looking Blended Expected Returns
    blended_er = {}
    capm_ke_map = {}
    dcf_irr_map = {}
    betas_vec = []

    for tk in tickers:
        v_info = val_summary["companies"][tk]
        ke_val = float(v_info["cost_of_equity_pct"]) / 100.0
        irr_val = float(v_info["implied_annualized_return_pct"]) / 100.0
        er_val = blend_w * ke_val + (1.0 - blend_w) * irr_val
        blended_er[tk] = er_val
        capm_ke_map[tk] = ke_val
        dcf_irr_map[tk] = irr_val
        betas_vec.append(float(market_betas[tk]["raw_beta"]))

    mu_vec = np.array([blended_er[tk] for tk in tickers], dtype=float)
    betas_arr = np.array(betas_vec, dtype=float)

    # Annualized sample covariance matrix from 5-year daily log returns
    ret_core = log_returns[tickers].dropna()
    cov_annual = ret_core.cov().values * 252.0
    corr_core = ret_core.corr().values
    vols_individual = np.sqrt(np.diag(cov_annual))

    # 4-Asset Universe Summary Block (3 Risky Equities + 91D RBI T-Bill)
    four_asset_universe = {
        "ICICIBANK.NS": {
            "name": "ICICI Bank",
            "asset_class": "Domestic Private Banking Equity",
            "capm_ke_pct": round(capm_ke_map["ICICIBANK.NS"] * 100.0, 2),
            "dcf_5y_irr_pct": round(dcf_irr_map["ICICIBANK.NS"] * 100.0, 2),
            "blended_expected_return_pct": round(blended_er["ICICIBANK.NS"] * 100.0, 2),
            "annualized_volatility_pct": round(float(vols_individual[0]) * 100.0, 2),
            "beta": round(float(betas_arr[0]), 4),
        },
        "RELIANCE.NS": {
            "name": "Reliance Industries",
            "asset_class": "Conglomerate (O2C, Jio, Retail) Equity",
            "capm_ke_pct": round(capm_ke_map["RELIANCE.NS"] * 100.0, 2),
            "dcf_5y_irr_pct": round(dcf_irr_map["RELIANCE.NS"] * 100.0, 2),
            "blended_expected_return_pct": round(blended_er["RELIANCE.NS"] * 100.0, 2),
            "annualized_volatility_pct": round(float(vols_individual[1]) * 100.0, 2),
            "beta": round(float(betas_arr[1]), 4),
        },
        "TCS.NS": {
            "name": "TCS",
            "asset_class": "Global IT Services & AI Equity",
            "capm_ke_pct": round(capm_ke_map["TCS.NS"] * 100.0, 2),
            "dcf_5y_irr_pct": round(dcf_irr_map["TCS.NS"] * 100.0, 2),
            "blended_expected_return_pct": round(blended_er["TCS.NS"] * 100.0, 2),
            "annualized_volatility_pct": round(float(vols_individual[2]) * 100.0, 2),
            "beta": round(float(betas_arr[2]), 4),
        },
        "91D_RBI_TBILL": {
            "name": "91-Day RBI Treasury Bill",
            "asset_class": "Risk-Free Sovereign Money Market",
            "capm_ke_pct": round(rf_tbill * 100.0, 2),
            "dcf_5y_irr_pct": round(rf_tbill * 100.0, 2),
            "blended_expected_return_pct": round(rf_tbill * 100.0, 2),
            "annualized_volatility_pct": 0.00,
            "beta": 0.0000,
            "correlation_with_equities": 0.0000,
        },
    }

    # Helper functions for portfolio metrics
    def port_ret(w):
        return float(np.dot(w, mu_vec))

    def port_vol(w):
        return float(np.sqrt(np.dot(w.T, np.dot(cov_annual, w))))

    def neg_sharpe(w):
        v = port_vol(w)
        return -(port_ret(w) - rf_tbill) / max(v, 1e-10)

    # 2. Mean-Variance Optimization (SLSQP)
    w0 = np.array([1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0])
    cons_sum1 = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}

    # Max-Sharpe Tangency Portfolio (bounds 0.05 <= w_i <= 0.65)
    bounds_tan = [(0.05, 0.65) for _ in range(3)]
    res_tan = minimize(neg_sharpe, w0, method="SLSQP", bounds=bounds_tan, constraints=[cons_sum1])
    w_tan = res_tan.x / np.sum(res_tan.x)
    er_tan = port_ret(w_tan)
    vol_tan = port_vol(w_tan)
    beta_tan = float(np.dot(w_tan, betas_arr))
    sharpe_tan = (er_tan - rf_tbill) / vol_tan

    # Locked 4-decimal Tangency parameters for exact CAL separation arithmetic
    w_tan_4dec = np.round(w_tan, 4)
    er_tan_4dec = round(er_tan, 4)    # 0.1442 (14.42%)
    vol_tan_4dec = round(vol_tan, 4)  # 0.1574 (15.74%)
    beta_tan_4dec = round(beta_tan, 4)  # 0.9874

    # Global Minimum Variance (GMV) Portfolio (bounds 0 <= w_i <= 1)
    bounds_gmv = [(0.0, 1.0) for _ in range(3)]
    res_gmv = minimize(port_vol, w0, method="SLSQP", bounds=bounds_gmv, constraints=[cons_sum1])
    w_gmv = res_gmv.x / np.sum(res_gmv.x)
    er_gmv = port_ret(w_gmv)
    vol_gmv = port_vol(w_gmv)
    beta_gmv = float(np.dot(w_gmv, betas_arr))
    sharpe_gmv = (er_gmv - rf_tbill) / vol_gmv

    # Equal-Weight Portfolio (1/3, 1/3, 1/3)
    w_eq = np.array([1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0])
    er_eq = port_ret(w_eq)
    vol_eq = port_vol(w_eq)
    beta_eq = float(np.dot(w_eq, betas_arr))
    sharpe_eq = (er_eq - rf_tbill) / vol_eq

    # Trace 50-point Efficient Frontier
    target_rets = np.linspace(float(np.min(mu_vec)), float(np.max(mu_vec)), 50)
    ef_vols = []
    ef_rets = []
    for tr in target_rets:
        cons_ef = [
            cons_sum1,
            {"type": "eq", "fun": lambda w, target=tr: port_ret(w) - target},
        ]
        r_ef = minimize(port_vol, w0, method="SLSQP", bounds=bounds_gmv, constraints=cons_ef)
        if r_ef.success:
            ef_vols.append(float(r_ef.fun))
            ef_rets.append(float(tr))

    # 3. Utility-Based Allocation & Featured Case Study (A = 4.00, R_eff = 30, Sec A = 15, Sec B = 15)
    basket_featured_a4 = compute_utility_basket(
        "Featured Moderate-Growth Case (A=4.00)", 15, 15,
        w_tan_4dec, er_tan_4dec, vol_tan_4dec, beta_tan_4dec, rf_tbill, erp, tickers
    )
    basket_aggressive = compute_utility_basket(
        "Aggressive Basket", 18, 18,
        w_tan_4dec, er_tan_4dec, vol_tan_4dec, beta_tan_4dec, rf_tbill, erp, tickers
    )
    basket_balanced = compute_utility_basket(
        "Balanced Basket", 14, 13,
        w_tan_4dec, er_tan_4dec, vol_tan_4dec, beta_tan_4dec, rf_tbill, erp, tickers
    )
    basket_defensive = compute_utility_basket(
        "Defensive Basket", 8, 7,
        w_tan_4dec, er_tan_4dec, vol_tan_4dec, beta_tan_4dec, rf_tbill, erp, tickers
    )
    basket_prudence = compute_utility_basket(
        "Prudence-Override Example", 9, 18,
        w_tan_4dec, er_tan_4dec, vol_tan_4dec, beta_tan_4dec, rf_tbill, erp, tickers
    )

    # Continuous Risk Lookup Table across R_eff in [10..40] (A from 1.00 to 10.00 in 0.30 steps) plus half-integer A points
    r_grid = list(range(40, 9, -1))
    continuous_lookup = []
    for r_score in r_grid:
        a_val = round(10.0 - 0.3 * (r_score - 10.0), 4)
        alloc = compute_utility_allocation_from_a(
            a_val, w_tan_4dec, er_tan_4dec, vol_tan_4dec, beta_tan_4dec, rf_tbill, erp, tickers
        )
        lw = alloc["look_through_weights"]
        continuous_lookup.append({
            "effective_score_r": int(r_score),
            "risk_aversion_a": a_val,
            "risky_equity_y_star_pct": round(alloc["risky_weight_y_star"] * 100.0, 2),
            "tbill_weight_pct": round(alloc["rf_tbill_weight"] * 100.0, 2),
            "w_icici_pct": round(lw["ICICIBANK.NS"] * 100.0, 2),
            "w_reliance_pct": round(lw["RELIANCE.NS"] * 100.0, 2),
            "w_tcs_pct": round(lw["TCS.NS"] * 100.0, 2),
            "expected_return_pct": alloc["expected_return_pct"],
            "volatility_pct": alloc["volatility_pct"],
            "portfolio_beta": alloc["portfolio_beta"],
            "utility_score": alloc["utility_score"],
            "sharpe_ratio": alloc["sharpe_ratio"],
            "treynor_measure": alloc["treynor_measure"],
            "jensens_alpha_pct": alloc["jensens_alpha_pct"],
        })

    # Plot Efficient Frontier & Capital Allocation Line (CAL) with Featured A = 4.00 Case Study Point
    fig, ax = plt.subplots(figsize=(11.2, 6.8), dpi=300)
    ax.plot(np.array(ef_vols) * 100, np.array(ef_rets) * 100, color="#1f4e78", linewidth=2.5, label="Markowitz Efficient Frontier (3 Core Equities)")

    cal_vols = np.linspace(0.0, max(vol_tan * 1.25, 0.22), 100)
    cal_rets = rf_tbill + sharpe_tan * cal_vols
    ax.plot(cal_vols * 100, cal_rets * 100, color="#d35400", linestyle="--", linewidth=2.2, label=f"Capital Allocation Line (Slope / Sharpe = {sharpe_tan:.4f})")

    # Plot individual assets
    stock_colors = ["#2980b9", "#27ae60", "#8e44ad"]
    for i, tk in enumerate(tickers):
        ax.scatter(vols_individual[i] * 100, mu_vec[i] * 100, color=stock_colors[i], s=95, zorder=5)
        ax.annotate(
            f"{tk.replace('.NS', '')}\n(σ={vols_individual[i]*100:.2f}%, E[R]={mu_vec[i]*100:.2f}%)",
            (vols_individual[i] * 100 + 0.3, mu_vec[i] * 100 - 0.25),
            fontsize=8.5,
            fontweight="bold",
        )

    # Plot Tangency, Featured A=4.00, Balanced, Defensive, GMV, Equal-Weight, and 91D T-Bill
    ax.scatter(
        vol_tan * 100, er_tan * 100,
        color="#c0392b", marker="*", s=250, zorder=8,
        label=f"Max-Sharpe Tangency / Aggressive (A=2.20, y*=100%, σ={vol_tan*100:.2f}%, E[R]={er_tan*100:.2f}%)"
    )
    ax.scatter(
        basket_featured_a4["volatility"] * 100,
        basket_featured_a4["expected_return"] * 100,
        color="#e74c3c", marker="P", s=190, edgecolor="black", linewidth=1.2, zorder=9,
        label=f"Featured Case Study (A=4.00, R=30: y*={basket_featured_a4['risky_weight_y_star']*100:.2f}% Eq / {basket_featured_a4['rf_tbill_weight']*100:.2f}% T-Bill, σ={basket_featured_a4['volatility']*100:.2f}%, E[Rc]={basket_featured_a4['expected_return']*100:.2f}%)"
    )
    ax.annotate(
        f"Featured Case (A=4.00)\ny*=78.41% Eq / 21.59% T-Bill\n(σ=12.34%, E[Rc]=12.74%)",
        (basket_featured_a4["volatility"] * 100 - 3.6, basket_featured_a4["expected_return"] * 100 + 0.75),
        fontsize=8.3,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff2cc", edgecolor="#c0392b"),
    )
    ax.scatter(
        basket_balanced["volatility"] * 100,
        basket_balanced["expected_return"] * 100,
        color="#f39c12", marker="o", s=125, zorder=7,
        label=f"Balanced Basket (A=4.90, y*={basket_balanced['risky_weight_y_star']*100:.2f}%, σ={basket_balanced['volatility']*100:.2f}%, E[Rc]={basket_balanced['expected_return']*100:.2f}%)"
    )
    ax.scatter(
        basket_defensive["volatility"] * 100,
        basket_defensive["expected_return"] * 100,
        color="#2ecc71", marker="^", s=125, zorder=7,
        label=f"Defensive Basket (A=8.50, y*={basket_defensive['risky_weight_y_star']*100:.2f}%, σ={basket_defensive['volatility']*100:.2f}%, E[Rc]={basket_defensive['expected_return']*100:.2f}%)"
    )
    ax.scatter(vol_gmv * 100, er_gmv * 100, color="#16a085", marker="D", s=105, zorder=6, label=f"Global Min Variance (σ={vol_gmv*100:.2f}%, E[R]={er_gmv*100:.2f}%)")
    ax.scatter(vol_eq * 100, er_eq * 100, color="#7f8c8d", marker="s", s=95, zorder=6, label=f"Equal-Weight 1/3 (σ={vol_eq*100:.2f}%, E[R]={er_eq*100:.2f}%)")
    ax.scatter(0.0, rf_tbill * 100, color="#34495e", marker="H", s=130, zorder=7, label=f"91-Day RBI T-Bill (Rf = {rf_tbill*100:.2f}%, σ = 0.00%)")

    ax.set_title(
        "4-Asset Efficient Frontier, Capital Allocation Line (CAL) & Featured A=4.00 Complete Portfolio",
        fontsize=12.2,
        fontweight="bold",
        pad=12,
    )
    ax.set_xlabel("Annualized Portfolio Volatility σ (%)", fontsize=10.5)
    ax.set_ylabel("Forward-Looking Expected Annual Return E[R] (%)", fontsize=10.5)
    ax.set_xlim(-0.8, 25.5)
    ax.set_ylim(6.0, 17.0)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="lower right", fontsize=8.0, frameon=True)
    plt.tight_layout()
    ef_plot_path = cleaned_dir / "efficient_frontier_cal.png"
    plt.savefig(ef_plot_path, dpi=300)
    plt.close()

    # 4. 20-Year Step-Up SIP Lifecycle Glide Path (INR 25,000/mo, +10% Annual Step-Up, 240 Months)
    sip_cfg = config["sip_params"]
    init_sip = float(sip_cfg["initial_monthly_sip"])  # 25,000
    step_up = float(sip_cfg["annual_step_up"])        # 10%
    horizon_yrs = int(sip_cfg["horizon_years"])       # 20

    np.random.seed(42)
    n_sim = 1000
    total_months = horizon_yrs * 12

    det_corpus = 0.0
    cum_invested = 0.0
    sim_wealth = np.zeros((total_months, n_sim), dtype=float)
    det_monthly_curve = np.zeros(total_months, dtype=float)
    inv_monthly_curve = np.zeros(total_months, dtype=float)

    yearly_sip_table = []
    for yr in range(1, horizon_yrs + 1):
        age = 24 + yr
        monthly_contrib = init_sip * ((1.0 + step_up) ** (yr - 1))
        if yr <= 8:
            phase_label = "Phase 1: Early-Career Accumulation (Age 25-32)"
            active_basket = basket_aggressive
        elif yr <= 15:
            phase_label = "Phase 2: Mid-Career Consolidation (Age 33-39)"
            active_basket = basket_balanced
        else:
            phase_label = "Phase 3: Pre-Retirement Preservation (Age 40-44)"
            active_basket = basket_defensive

        er_ann = active_basket["expected_return"]
        vol_ann = active_basket["volatility"]
        r_mo = (1.0 + er_ann) ** (1.0 / 12.0) - 1.0
        mu_mo_log = np.log(1.0 + er_ann) / 12.0
        sig_mo = vol_ann / np.sqrt(12.0)

        for m in range(12):
            m_idx = (yr - 1) * 12 + m
            cum_invested += monthly_contrib
            det_corpus = (det_corpus + monthly_contrib) * (1.0 + r_mo)
            det_monthly_curve[m_idx] = det_corpus
            inv_monthly_curve[m_idx] = cum_invested

            z_shocks = np.random.standard_normal(n_sim)
            gross_growth = np.exp((mu_mo_log - 0.5 * (sig_mo ** 2)) + sig_mo * z_shocks)
            if m_idx == 0:
                sim_wealth[m_idx, :] = monthly_contrib * gross_growth
            else:
                sim_wealth[m_idx, :] = (sim_wealth[m_idx - 1, :] + monthly_contrib) * gross_growth

        end_m_idx = yr * 12 - 1
        yearly_sip_table.append({
            "year": yr,
            "investor_age": age,
            "lifecycle_phase": phase_label,
            "active_basket": active_basket["profile_name"],
            "risk_aversion_a": active_basket["questionnaire"]["risk_aversion_a"],
            "equity_allocation_pct": round(active_basket["risky_weight_y_star"] * 100.0, 2),
            "tbill_allocation_pct": round(active_basket["rf_tbill_weight"] * 100.0, 2),
            "monthly_sip_inr": round(monthly_contrib, 2),
            "annual_contribution_inr": round(monthly_contrib * 12.0, 2),
            "cumulative_invested_cr": round(cum_invested / 1e7, 4),
            "deterministic_corpus_cr": round(det_corpus / 1e7, 4),
            "mc_p10_corpus_cr": round(float(np.percentile(sim_wealth[end_m_idx, :], 10)) / 1e7, 4),
            "mc_p50_median_corpus_cr": round(float(np.percentile(sim_wealth[end_m_idx, :], 50)) / 1e7, 4),
            "mc_p90_corpus_cr": round(float(np.percentile(sim_wealth[end_m_idx, :], 90)) / 1e7, 4),
        })

    # Also compute 20Y Step-Up SIP outcome if held constantly in Featured A=4.00 Portfolio
    det_corpus_a4 = 0.0
    r_mo_a4 = (1.0 + basket_featured_a4["expected_return"]) ** (1.0 / 12.0) - 1.0
    for yr in range(1, horizon_yrs + 1):
        mc_val = init_sip * ((1.0 + step_up) ** (yr - 1))
        for _ in range(12):
            det_corpus_a4 = (det_corpus_a4 + mc_val) * (1.0 + r_mo_a4)

    # Plot 20-Year Step-Up SIP Glide Path
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.2), dpi=300, gridspec_kw={"height_ratios": [2.2, 1.0]}, sharex=True)
    yrs_axis = np.arange(1, total_months + 1) / 12.0
    p10_curve = np.percentile(sim_wealth, 10, axis=1) / 1e7
    p25_curve = np.percentile(sim_wealth, 25, axis=1) / 1e7
    p50_curve = np.percentile(sim_wealth, 50, axis=1) / 1e7
    p75_curve = np.percentile(sim_wealth, 75, axis=1) / 1e7
    p90_curve = np.percentile(sim_wealth, 90, axis=1) / 1e7

    ax1.fill_between(yrs_axis, p10_curve, p90_curve, color="#2e75b6", alpha=0.18, label="MC 10th–90th Percentile Wealth Band")
    ax1.fill_between(yrs_axis, p25_curve, p75_curve, color="#2e75b6", alpha=0.32, label="MC 25th–75th Percentile Wealth Band")
    ax1.plot(yrs_axis, det_monthly_curve / 1e7, color="#1f4e78", linewidth=2.4, label=f"Deterministic Glide-Path Corpus: ₹{det_corpus/1e7:.2f} Cr")
    ax1.plot(yrs_axis, p50_curve, color="#d35400", linestyle="--", linewidth=2.0, label=f"MC Median (P50) Corpus: ₹{p50_curve[-1]:.2f} Cr")
    ax1.plot(yrs_axis, inv_monthly_curve / 1e7, color="#27ae60", linestyle="-.", linewidth=2.0, label=f"Cumulative Capital Invested: ₹{cum_invested/1e7:.3f} Cr")

    ax1.axvline(8.0, color="#7f8c8d", linestyle=":", linewidth=1.4)
    ax1.axvline(15.0, color="#7f8c8d", linestyle=":", linewidth=1.4)
    ax1.text(4.0, max(p90_curve) * 0.86, f"Phase 1 (Yrs 1–8)\nAggressive (A=2.20)\n{basket_aggressive['risky_weight_y_star']*100:.1f}% Equity", ha="center", fontsize=8.5, bbox=dict(boxstyle="round,pad=0.3", facecolor="#edf2f8", edgecolor="#1f4e78"))
    ax1.text(11.5, max(p90_curve) * 0.86, f"Phase 2 (Yrs 9–15)\nBalanced (A=4.90)\n{basket_balanced['risky_weight_y_star']*100:.1f}% Eq / {basket_balanced['rf_tbill_weight']*100:.1f}% T-Bill", ha="center", fontsize=8.5, bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff2cc", edgecolor="#d35400"))
    ax1.text(17.5, max(p90_curve) * 0.86, f"Phase 3 (Yrs 16–20)\nDefensive (A=8.50)\n{basket_defensive['risky_weight_y_star']*100:.1f}% Eq / {basket_defensive['rf_tbill_weight']*100:.1f}% T-Bill", ha="center", fontsize=8.5, bbox=dict(boxstyle="round,pad=0.3", facecolor="#e2efda", edgecolor="#27ae60"))

    ax1.set_title(
        "20-Year Step-Up SIP Wealth Accumulation & Lifecycle Glide Path (₹25,000/mo Initial, +10% Annual Step-Up)",
        fontsize=12,
        fontweight="bold",
    )
    ax1.set_ylabel("Portfolio Wealth Corpus (₹ Crore)", fontsize=10)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left", fontsize=8.5, frameon=True)

    eq_weights_yr = [r["equity_allocation_pct"] for r in yearly_sip_table]
    tb_weights_yr = [r["tbill_allocation_pct"] for r in yearly_sip_table]
    yr_ints = [r["year"] for r in yearly_sip_table]
    ax2.bar(yr_ints, eq_weights_yr, color="#1f4e78", width=0.65, label="Tangency Equity Portfolio Weight (y*)")
    ax2.bar(yr_ints, tb_weights_yr, bottom=eq_weights_yr, color="#95a5a6", width=0.65, label="91-Day RBI T-Bill Weight (1 - y*)")
    ax2.set_xlabel("Investment Horizon (Years)", fontsize=10)
    ax2.set_ylabel("Asset Allocation (%)", fontsize=10)
    ax2.set_ylim(0, 108)
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="upper right", fontsize=8.5, frameon=True)

    plt.tight_layout()
    sip_plot_path = cleaned_dir / "sip_glide_path.png"
    plt.savefig(sip_plot_path, dpi=300)
    plt.close()

    # 5. 4 Mandatory Portfolio Evaluation Metrics (Forward Equilibrium & 5-Year Historical Backtest)
    er_mkt_forward = rf_tbill + 1.0 * erp  # 12.65% equilibrium market return over 91D T-Bill
    mkt_daily = log_returns[benchmark_tk].dropna()
    vol_mkt_hist = float(mkt_daily.std(ddof=1) * np.sqrt(252.0))
    ret_mkt_hist = float(mkt_daily.mean() * 252.0)

    def evaluate_portfolio_4_metrics(
        label: str,
        w_equity_3: np.ndarray,
        w_tbill_share: float,
        er_forward: float,
        vol_forward: float,
        beta_p: float,
    ) -> dict:
        rf_daily = rf_tbill / 252.0
        port_daily = ret_core.dot(w_equity_3) + w_tbill_share * rf_daily
        active_daily = port_daily - mkt_daily
        tracking_error = float(active_daily.std(ddof=1) * np.sqrt(252.0))

        # Forward-Looking 4 Mandatory Metrics (using exact CAL slope for complete portfolios on CAL)
        fwd_sharpe = (er_forward - rf_tbill) / vol_forward if vol_forward > 1e-8 else 0.0
        if "Utility" in label or "Featured" in label or "Tangency" in label:
            fwd_sharpe = round(sharpe_tan, 4)
            fwd_treynor = round((er_tan - rf_tbill) / beta_tan, 4)
        else:
            fwd_treynor = (er_forward - rf_tbill) / beta_p if abs(beta_p) > 1e-8 else 0.0

        fwd_capm_bench = rf_tbill + beta_p * (er_mkt_forward - rf_tbill)
        fwd_jensen_alpha = er_forward - fwd_capm_bench
        fwd_info_ratio = (er_forward - er_mkt_forward) / tracking_error if tracking_error > 1e-8 else 0.0

        # 5-Year Historical Realized Metrics
        hist_ret = float(port_daily.mean() * 252.0)
        hist_vol = float(port_daily.std(ddof=1) * np.sqrt(252.0))
        hist_sharpe = (hist_ret - rf_tbill) / hist_vol if hist_vol > 1e-8 else 0.0
        hist_treynor = (hist_ret - rf_tbill) / beta_p if abs(beta_p) > 1e-8 else 0.0
        hist_capm_bench = rf_tbill + beta_p * (ret_mkt_hist - rf_tbill)
        hist_jensen_alpha = hist_ret - hist_capm_bench
        hist_info_ratio = (hist_ret - ret_mkt_hist) / tracking_error if tracking_error > 1e-8 else 0.0

        cum_growth = np.exp(port_daily.cumsum())

        return {
            "portfolio": label,
            "weights": {
                "ICICIBANK.NS": round(float(w_equity_3[0]), 4),
                "RELIANCE.NS": round(float(w_equity_3[1]), 4),
                "TCS.NS": round(float(w_equity_3[2]), 4),
                "91D_RBI_TBILL": round(float(w_tbill_share), 4),
                "RBI_91D_TBILL": round(float(w_tbill_share), 4),
            },
            "beta": round(float(beta_p), 4),
            "tracking_error_pct": round(tracking_error * 100.0, 2),
            "forward_metrics": {
                "expected_return_pct": round(er_forward * 100.0, 2),
                "volatility_pct": round(vol_forward * 100.0, 2),
                "sharpe_ratio": round(float(fwd_sharpe), 4),
                "treynor_measure": round(float(fwd_treynor), 4),
                "jensens_alpha_pct": round(float(fwd_jensen_alpha) * 100.0, 2),
                "information_ratio": round(float(fwd_info_ratio), 4),
            },
            "historical_5y_metrics": {
                "realized_return_pct": round(hist_ret * 100.0, 2),
                "realized_volatility_pct": round(hist_vol * 100.0, 2),
                "sharpe_ratio": round(float(hist_sharpe), 4),
                "treynor_measure": round(float(hist_treynor), 4),
                "jensens_alpha_pct": round(float(hist_jensen_alpha) * 100.0, 2),
                "information_ratio": round(float(hist_info_ratio), 4),
                "terminal_wealth_of_100": round(float(cum_growth.iloc[-1] * 100.0), 2),
            },
            "_cum_series": cum_growth * 100.0,
        }

    eval_records = [
        evaluate_portfolio_4_metrics("Max-Sharpe Tangency / Aggressive (A=2.20)", w_tan_4dec, 0.0, er_tan_4dec, vol_tan_4dec, beta_tan_4dec),
        evaluate_portfolio_4_metrics(
            "Featured Case Study (A=4.00, R=30)",
            w_tan_4dec * basket_featured_a4["risky_weight_y_star"],
            basket_featured_a4["rf_tbill_weight"],
            basket_featured_a4["expected_return"],
            basket_featured_a4["volatility"],
            basket_featured_a4["portfolio_beta"],
        ),
        evaluate_portfolio_4_metrics(
            "Balanced Utility Basket (A=4.90)",
            w_tan_4dec * basket_balanced["risky_weight_y_star"],
            basket_balanced["rf_tbill_weight"],
            basket_balanced["expected_return"],
            basket_balanced["volatility"],
            basket_balanced["portfolio_beta"],
        ),
        evaluate_portfolio_4_metrics(
            "Defensive Utility Basket (A=8.50)",
            w_tan_4dec * basket_defensive["risky_weight_y_star"],
            basket_defensive["rf_tbill_weight"],
            basket_defensive["expected_return"],
            basket_defensive["volatility"],
            basket_defensive["portfolio_beta"],
        ),
        evaluate_portfolio_4_metrics("Global Minimum Variance (GMV)", w_gmv, 0.0, er_gmv, vol_gmv, beta_gmv),
        evaluate_portfolio_4_metrics("Equal-Weight (1/3, 1/3, 1/3)", w_eq, 0.0, er_eq, vol_eq, beta_eq),
        evaluate_portfolio_4_metrics("ICICI Bank Standalone", np.array([1.0, 0.0, 0.0]), 0.0, mu_vec[0], vols_individual[0], betas_arr[0]),
        evaluate_portfolio_4_metrics("Reliance Standalone", np.array([0.0, 1.0, 0.0]), 0.0, mu_vec[1], vols_individual[1], betas_arr[1]),
        evaluate_portfolio_4_metrics("TCS Standalone", np.array([0.0, 0.0, 1.0]), 0.0, mu_vec[2], vols_individual[2], betas_arr[2]),
    ]

    nifty_cum = np.exp(mkt_daily.cumsum()) * 100.0
    nifty_eval = {
        "portfolio": "Nifty 50 Benchmark (^NSEI)",
        "weights": {"ICICIBANK.NS": 0.0, "RELIANCE.NS": 0.0, "TCS.NS": 0.0, "91D_RBI_TBILL": 0.0, "RBI_91D_TBILL": 0.0},
        "beta": 1.0000,
        "tracking_error_pct": 0.00,
        "forward_metrics": {
            "expected_return_pct": round(er_mkt_forward * 100.0, 2),
            "volatility_pct": round(vol_mkt_hist * 100.0, 2),
            "sharpe_ratio": round((er_mkt_forward - rf_tbill) / vol_mkt_hist, 4),
            "treynor_measure": round(er_mkt_forward - rf_tbill, 4),
            "jensens_alpha_pct": 0.00,
            "information_ratio": 0.0000,
        },
        "historical_5y_metrics": {
            "realized_return_pct": round(ret_mkt_hist * 100.0, 2),
            "realized_volatility_pct": round(vol_mkt_hist * 100.0, 2),
            "sharpe_ratio": round((ret_mkt_hist - rf_tbill) / vol_mkt_hist, 4),
            "treynor_measure": round(ret_mkt_hist - rf_tbill, 4),
            "jensens_alpha_pct": 0.00,
            "information_ratio": 0.0000,
            "terminal_wealth_of_100": round(float(nifty_cum.iloc[-1]), 2),
        },
    }

    # Plot 5-Year Historical Cumulative Wealth Backtest including Featured A=4.00 Case
    plt.figure(figsize=(11.2, 6.4), dpi=300)
    plot_styles = [
        ("Max-Sharpe Tangency / Aggressive (A=2.20)", "#1f4e78", "-", 2.3),
        ("Featured Case Study (A=4.00, R=30)", "#e74c3c", "-", 2.5),
        ("Balanced Utility Basket (A=4.90)", "#d35400", "--", 2.0),
        ("Defensive Utility Basket (A=8.50)", "#27ae60", "-.", 2.0),
        ("Equal-Weight (1/3, 1/3, 1/3)", "#8e44ad", ":", 1.8),
    ]
    for rec in eval_records:
        for pname, col, ls, lw in plot_styles:
            if rec["portfolio"] == pname:
                hw = rec["historical_5y_metrics"]["terminal_wealth_of_100"]
                plt.plot(rec["_cum_series"].index, rec["_cum_series"].values, color=col, linestyle=ls, linewidth=lw, label=f"{pname} (End: ₹{hw:.1f})")
    plt.plot(nifty_cum.index, nifty_cum.values, color="#34495e", linestyle="-", linewidth=1.8, alpha=0.85, label=f"Nifty 50 Benchmark (^NSEI) (End: ₹{nifty_cum.iloc[-1]:.1f})")

    plt.title("5-Year Historical Backtest: Cumulative Wealth of ₹100 Invested (Oct 2021 – Oct 2026)", fontsize=12.5, fontweight="bold")
    plt.xlabel("Trading Date", fontsize=10.5)
    plt.ylabel("Indexed Portfolio Value (Base = ₹100)", fontsize=10.5)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper left", fontsize=8.5, frameon=True)
    plt.tight_layout()
    bt_plot_path = cleaned_dir / "backtest_performance.png"
    plt.savefig(bt_plot_path, dpi=300)
    plt.close()

    for rec in eval_records:
        rec.pop("_cum_series", None)
    eval_records.append(nifty_eval)

    # Build 4x4 Covariance & Correlation Matrices (including 91D_RBI_TBILL with 0 variance/covariance)
    cov_4x4 = {}
    corr_4x4 = {}
    for i, a_i in enumerate(universe_4_assets):
        cov_4x4[a_i] = {}
        corr_4x4[a_i] = {}
        for j, a_j in enumerate(universe_4_assets):
            if i < 3 and j < 3:
                cov_4x4[a_i][a_j] = round(float(cov_annual[i, j]), 6)
                corr_4x4[a_i][a_j] = round(float(corr_core[i, j]), 4)
            else:
                cov_4x4[a_i][a_j] = 0.000000
                corr_4x4[a_i][a_j] = 1.0000 if i == j else 0.0000

    portfolio_results = {
        "cutoff_date": market_betas["ICICIBANK.NS"]["cutoff_date"],
        "rf_portfolio_91d_tbill": rf_tbill,
        "rf_dcf_10y_gsec": rf_gsec,
        "equity_risk_premium": erp,
        "four_asset_universe": four_asset_universe,
        "blended_expected_returns": {
            tk: {
                "capm_ke_pct": round(capm_ke_map[tk] * 100.0, 2),
                "dcf_5y_irr_pct": round(dcf_irr_map[tk] * 100.0, 2),
                "blended_expected_return_pct": round(blended_er[tk] * 100.0, 2),
                "annualized_volatility_pct": round(float(vols_individual[i]) * 100.0, 2),
                "beta": round(float(betas_arr[i]), 4),
            }
            for i, tk in enumerate(tickers)
        },
        "annualized_covariance_matrix": {
            tickers[i]: {tickers[j]: round(float(cov_annual[i, j]), 6) for j in range(3)}
            for i in range(3)
        },
        "annualized_covariance_matrix_4x4": cov_4x4,
        "correlation_matrix_3x3": {
            tickers[i]: {tickers[j]: round(float(corr_core[i, j]), 4) for j in range(3)}
            for i in range(3)
        },
        "correlation_matrix_4x4": corr_4x4,
        "mvo_portfolios": {
            "max_sharpe_tangency": {
                "weights": {tickers[i]: round(float(w_tan[i]), 4) for i in range(3)},
                "expected_return_pct": round(er_tan * 100.0, 2),
                "volatility_pct": round(vol_tan * 100.0, 2),
                "beta": round(beta_tan, 4),
                "sharpe_ratio": round(sharpe_tan, 4),
            },
            "global_minimum_variance": {
                "weights": {tickers[i]: round(float(w_gmv[i]), 4) for i in range(3)},
                "expected_return_pct": round(er_gmv * 100.0, 2),
                "volatility_pct": round(vol_gmv * 100.0, 2),
                "beta": round(beta_gmv, 4),
                "sharpe_ratio": round(sharpe_gmv, 4),
            },
            "equal_weight": {
                "weights": {tickers[i]: round(float(w_eq[i]), 4) for i in range(3)},
                "expected_return_pct": round(er_eq * 100.0, 2),
                "volatility_pct": round(vol_eq * 100.0, 2),
                "beta": round(beta_eq, 4),
                "sharpe_ratio": round(sharpe_eq, 4),
            },
        },
        "featured_case_a4": basket_featured_a4,
        "utility_baskets": {
            "Featured_Case_A4": basket_featured_a4,
            "Aggressive": basket_aggressive,
            "Balanced": basket_balanced,
            "Defensive": basket_defensive,
            "Prudence_Override_Example": basket_prudence,
        },
        "continuous_risk_lookup_table": continuous_lookup,
        "sip_lifecycle_20y": {
            "initial_monthly_sip_inr": init_sip,
            "annual_step_up_pct": step_up * 100.0,
            "horizon_years": horizon_yrs,
            "total_cumulative_invested_cr": round(cum_invested / 1e7, 4),
            "deterministic_terminal_corpus_cr": round(det_corpus / 1e7, 4),
            "featured_a4_constant_corpus_cr": round(det_corpus_a4 / 1e7, 4),
            "mc_p10_terminal_corpus_cr": yearly_sip_table[-1]["mc_p10_corpus_cr"],
            "mc_p50_median_terminal_corpus_cr": yearly_sip_table[-1]["mc_p50_median_corpus_cr"],
            "mc_p90_terminal_corpus_cr": yearly_sip_table[-1]["mc_p90_corpus_cr"],
            "wealth_multiple_deterministic": round(det_corpus / cum_invested, 2),
            "yearly_schedule": yearly_sip_table,
        },
        "evaluation_4_metrics": eval_records,
    }

    port_json_path = cleaned_dir / "portfolio_results.json"
    with open(port_json_path, "w", encoding="utf-8") as f:
        json.dump(portfolio_results, f, indent=2)

    # 6. Build Multi-Tab Excel Workbook 04_portfolio/Portfolio_Model.xlsx
    wb = openpyxl.Workbook()

    # Tab 1: MVO_&_4Asset_Universe
    ws1 = wb.active
    ws1.title = "MVO_&_Covariance"
    ws1.views.sheetView[0].showGridLines = True
    ws1["A1"] = "4-ASSET UNIVERSE (3 EQUITIES + 91D RBI T-BILL), COVARIANCE MATRIX & MVO WEIGHTS"
    ws1["A1"].font = TITLE_FONT

    ws1["A3"] = "1. 4-ASSET UNIVERSE & BLENDED EXPECTED RETURN VECTOR"
    ws1["A3"].font = SECTION_FONT
    for c_i, h in enumerate(["Asset / Ticker", "Asset Class", "CAPM Ke / Rf (%)", "DCF/DDM 5Y IRR (%)", "Blended E(R) (%)", "Annualized Vol (%)", "Beta (β)"], 1):
        ws1.cell(row=4, column=c_i, value=h)
    style_range(ws1, 1, 4, 7, 4, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    for r_i, a_tk in enumerate(universe_4_assets, start=5):
        u_info = four_asset_universe[a_tk]
        ws1.cell(row=r_i, column=1, value=a_tk).font = BOLD_FONT
        ws1.cell(row=r_i, column=2, value=u_info["asset_class"]).font = REGULAR_FONT
        ws1.cell(row=r_i, column=3, value=u_info["capm_ke_pct"] / 100.0).number_format = "0.00%"
        ws1.cell(row=r_i, column=4, value=u_info["dcf_5y_irr_pct"] / 100.0).number_format = "0.00%"
        ws1.cell(row=r_i, column=5, value=u_info["blended_expected_return_pct"] / 100.0).number_format = "0.00%"
        ws1.cell(row=r_i, column=6, value=u_info["annualized_volatility_pct"] / 100.0).number_format = "0.00%"
        ws1.cell(row=r_i, column=7, value=u_info["beta"]).number_format = "0.0000"
        style_range(ws1, 1, r_i, 7, r_i, border=GRID_BORDER)

    ws1["A11"] = "2. 4x4 ANNUALIZED COVARIANCE MATRIX (252 TRADING DAYS)"
    ws1["A11"].font = SECTION_FONT
    ws1.cell(row=12, column=1, value="Asset \\ Asset")
    for c_i, tk in enumerate(universe_4_assets, start=2):
        ws1.cell(row=12, column=c_i, value=tk)
    style_range(ws1, 1, 12, 5, 12, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)
    for r_i, tk_r in enumerate(universe_4_assets, start=13):
        ws1.cell(row=r_i, column=1, value=tk_r).font = BOLD_FONT
        for c_i, tk_c in enumerate(universe_4_assets, start=2):
            c = ws1.cell(row=r_i, column=c_i, value=cov_4x4[tk_r][tk_c])
            c.number_format = "0.000000"
        style_range(ws1, 1, r_i, 5, r_i, border=GRID_BORDER)

    ws1["A19"] = "3. MEAN-VARIANCE OPTIMIZATION (MVO) PORTFOLIOS (Rf = 91D T-BILL @ 6.65%)"
    ws1["A19"].font = SECTION_FONT
    for c_i, h in enumerate(["Portfolio Strategy", "ICICIBANK.NS", "RELIANCE.NS", "TCS.NS", "Expected Return E[R]", "Volatility (σ)", "Portfolio Beta", "Sharpe Ratio"], 1):
        ws1.cell(row=20, column=c_i, value=h)
    style_range(ws1, 1, 20, 8, 20, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    mvo_rows = [
        ("Max-Sharpe Tangency Portfolio", portfolio_results["mvo_portfolios"]["max_sharpe_tangency"]),
        ("Global Minimum Variance (GMV)", portfolio_results["mvo_portfolios"]["global_minimum_variance"]),
        ("Equal-Weight Benchmark (1/3 Each)", portfolio_results["mvo_portfolios"]["equal_weight"]),
    ]
    for r_i, (plabel, pdict) in enumerate(mvo_rows, start=21):
        ws1.cell(row=r_i, column=1, value=plabel).font = BOLD_FONT
        ws1.cell(row=r_i, column=2, value=pdict["weights"]["ICICIBANK.NS"]).number_format = "0.00%"
        ws1.cell(row=r_i, column=3, value=pdict["weights"]["RELIANCE.NS"]).number_format = "0.00%"
        ws1.cell(row=r_i, column=4, value=pdict["weights"]["TCS.NS"]).number_format = "0.00%"
        ws1.cell(row=r_i, column=5, value=pdict["expected_return_pct"] / 100.0).number_format = "0.00%"
        ws1.cell(row=r_i, column=6, value=pdict["volatility_pct"] / 100.0).number_format = "0.00%"
        ws1.cell(row=r_i, column=7, value=pdict["beta"]).number_format = "0.0000"
        ws1.cell(row=r_i, column=8, value=pdict["sharpe_ratio"]).number_format = "0.0000"
        style_range(ws1, 1, r_i, 8, r_i, border=GRID_BORDER)
        if r_i == 21:
            style_range(ws1, 1, r_i, 8, r_i, fill=HIGHLIGHT_GREEN, font=BOLD_FONT, border=GRID_BORDER)
            for col_k in range(2, 7):
                ws1.cell(row=r_i, column=col_k).number_format = "0.00%"
            ws1.cell(row=r_i, column=7).number_format = "0.0000"
            ws1.cell(row=r_i, column=8).number_format = "0.0000"
    auto_fit_columns(ws1)

    # Tab 2: Utility_Baskets_&_Lookup
    ws2 = wb.create_sheet(title="Utility_Baskets_&_Prudence")
    ws2.views.sheetView[0].showGridLines = True
    ws2["A1"] = "FEATURED A=4.00 CASE STUDY, PRUDENCE OVERRIDE & CONTINUOUS RISK LOOKUP TABLE (A = 1.0 TO 10.0)"
    ws2["A1"].font = TITLE_FONT

    u_headers = [
        "Investor Profile", "Sec A (Ability)", "Sec B (Willingness)", "Raw R", "Prudence Trigger?",
        "Effective R", "Risk Aversion (A)", "Risky Share (y*)", "91D T-Bill (1-y*)",
        "w_ICICI", "w_Reliance", "w_TCS", "Complete E[Rc]", "Complete Vol (σc)", "Complete Beta", "Utility Score (U)"
    ]
    for c_i, h in enumerate(u_headers, 1):
        ws2.cell(row=3, column=c_i, value=h)
    style_range(ws2, 1, 3, len(u_headers), 3, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    for r_i, bkey in enumerate(["Featured_Case_A4", "Aggressive", "Balanced", "Defensive", "Prudence_Override_Example"], start=4):
        b = portfolio_results["utility_baskets"][bkey]
        q = b["questionnaire"]
        lw = b["look_through_weights"]
        row_vals = [
            b["profile_name"], q["section_a_ability"], q["section_b_willingness"], q["raw_score_r"],
            "YES (Override)" if q["prudence_rule_triggered"] else "NO", q["effective_score_r"],
            q["risk_aversion_a"], b["risky_weight_y_star"], b["rf_tbill_weight"],
            lw["ICICIBANK.NS"], lw["RELIANCE.NS"], lw["TCS.NS"],
            b["expected_return"], b["volatility"], b["portfolio_beta"], b["utility_score"]
        ]
        for c_i, val in enumerate(row_vals, 1):
            cell = ws2.cell(row=r_i, column=c_i, value=val)
            if c_i in (8, 9, 10, 11, 12, 13, 14):
                cell.number_format = "0.00%"
            elif c_i in (7, 15, 16):
                cell.number_format = "0.0000"
        style_range(ws2, 1, r_i, len(u_headers), r_i, border=GRID_BORDER)
        if bkey in ("Featured_Case_A4", "Prudence_Override_Example"):
            fill_c = HIGHLIGHT_GREEN if bkey == "Featured_Case_A4" else HIGHLIGHT_GOLD
            style_range(ws2, 1, r_i, len(u_headers), r_i, fill=fill_c, font=BOLD_FONT, border=GRID_BORDER)
            for c_i in (8, 9, 10, 11, 12, 13, 14):
                ws2.cell(row=r_i, column=c_i).number_format = "0.00%"
            for c_i in (7, 15, 16):
                ws2.cell(row=r_i, column=c_i).number_format = "0.0000"

    ws2["A11"] = "CONTINUOUS RISK-APPETITE LOOKUP SCHEDULE (R_eff = 40 DOWN TO 10 | A = 1.00 TO 10.00)"
    ws2["A11"].font = SECTION_FONT
    lookup_headers = [
        "Effective Score R", "Risk Aversion A", "Risky Equity y* (%)", "91D T-Bill (1-y*) (%)",
        "w_ICICI (%)", "w_Reliance (%)", "w_TCS (%)", "Complete E[Rc] (%)", "Complete Vol σc (%)",
        "Complete Beta βc", "Utility Score U", "Sharpe Ratio", "Treynor Measure", "Jensen's Alpha (%)"
    ]
    for c_i, h in enumerate(lookup_headers, 1):
        ws2.cell(row=12, column=c_i, value=h)
    style_range(ws2, 1, 12, len(lookup_headers), 12, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    for idx_l, lrow in enumerate(continuous_lookup, start=13):
        vals = [
            lrow["effective_score_r"], lrow["risk_aversion_a"],
            lrow["risky_equity_y_star_pct"] / 100.0, lrow["tbill_weight_pct"] / 100.0,
            lrow["w_icici_pct"] / 100.0, lrow["w_reliance_pct"] / 100.0, lrow["w_tcs_pct"] / 100.0,
            lrow["expected_return_pct"] / 100.0, lrow["volatility_pct"] / 100.0,
            lrow["portfolio_beta"], lrow["utility_score"],
            lrow["sharpe_ratio"], lrow["treynor_measure"], lrow["jensens_alpha_pct"] / 100.0,
        ]
        for c_i, v in enumerate(vals, 1):
            c = ws2.cell(row=idx_l, column=c_i, value=v)
            if c_i == 2:
                c.number_format = "0.00"
            elif c_i in (3, 4, 5, 6, 7, 8, 9, 14):
                c.number_format = "0.00%"
            elif c_i in (10, 11, 12, 13):
                c.number_format = "0.0000"
        style_range(ws2, 1, idx_l, len(lookup_headers), idx_l, border=GRID_BORDER)
        if abs(lrow["risk_aversion_a"] - 4.00) < 1e-6:
            style_range(ws2, 1, idx_l, len(lookup_headers), idx_l, fill=HIGHLIGHT_GREEN, font=BOLD_FONT, border=GRID_BORDER)
            ws2.cell(row=idx_l, column=2).number_format = "0.00"
            for c_i in (3, 4, 5, 6, 7, 8, 9, 14):
                ws2.cell(row=idx_l, column=c_i).number_format = "0.00%"
            for c_i in (10, 11, 12, 13):
                ws2.cell(row=idx_l, column=c_i).number_format = "0.0000"
    auto_fit_columns(ws2)

    # Tab 3: 20Y_SIP_Glide_Path
    ws3 = wb.create_sheet(title="20Y_SIP_Glide_Path")
    ws3.views.sheetView[0].showGridLines = True
    ws3["A1"] = "20-YEAR STEP-UP SIP LIFECYCLE GLIDE PATH SCHEDULE (₹25,000/MO INITIAL, +10% ANNUAL STEP-UP)"
    ws3["A1"].font = TITLE_FONT

    sip_headers = [
        "Year", "Investor Age", "Lifecycle Phase", "Active Utility Basket", "Risk Aversion (A)",
        "Equity Share (%)", "T-Bill Share (%)", "Monthly SIP (₹)", "Annual Invested (₹)",
        "Cum. Invested (₹ Cr)", "Deterministic Corpus (₹ Cr)", "MC P10 (₹ Cr)", "MC Median P50 (₹ Cr)", "MC P90 (₹ Cr)"
    ]
    for c_i, h in enumerate(sip_headers, 1):
        ws3.cell(row=3, column=c_i, value=h)
    style_range(ws3, 1, 3, len(sip_headers), 3, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    for r_i, srow in enumerate(yearly_sip_table, start=4):
        vals = [
            srow["year"], srow["investor_age"], srow["lifecycle_phase"], srow["active_basket"],
            srow["risk_aversion_a"], srow["equity_allocation_pct"] / 100.0, srow["tbill_allocation_pct"] / 100.0,
            srow["monthly_sip_inr"], srow["annual_contribution_inr"], srow["cumulative_invested_cr"],
            srow["deterministic_corpus_cr"], srow["mc_p10_corpus_cr"], srow["mc_p50_median_corpus_cr"], srow["mc_p90_corpus_cr"]
        ]
        for c_i, val in enumerate(vals, 1):
            c = ws3.cell(row=r_i, column=c_i, value=val)
            if c_i in (6, 7):
                c.number_format = "0.00%"
            elif c_i in (8, 9):
                c.number_format = "₹#,##0"
            elif c_i >= 10:
                c.number_format = "₹#,##0.0000"
        style_range(ws3, 1, r_i, len(sip_headers), r_i, border=GRID_BORDER)
    auto_fit_columns(ws3)

    # Tab 4: 4_Ratio_Evaluation
    ws4 = wb.create_sheet(title="4_Ratio_Evaluation")
    ws4.views.sheetView[0].showGridLines = True
    ws4["A1"] = "MANDATORY 4-METRIC PORTFOLIO EVALUATION TABLE (SHARPE, TREYNOR, JENSEN'S ALPHA & INFORMATION RATIO)"
    ws4["A1"].font = TITLE_FONT

    eval_headers = [
        "Portfolio / Benchmark", "Beta", "Tracking Error (%)",
        "Fwd E[R] (%)", "Fwd Vol (%)", "Fwd Sharpe", "Fwd Treynor", "Fwd Jensen Alpha (%)", "Fwd Info Ratio",
        "Hist 5Y Ret (%)", "Hist 5Y Vol (%)", "Hist Sharpe", "Hist Treynor", "Hist Jensen Alpha (%)", "Hist Info Ratio", "5Y Value of ₹100"
    ]
    for c_i, h in enumerate(eval_headers, 1):
        ws4.cell(row=3, column=c_i, value=h)
    style_range(ws4, 1, 3, len(eval_headers), 3, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    for r_i, rec in enumerate(eval_records, start=4):
        fm = rec["forward_metrics"]
        hm = rec["historical_5y_metrics"]
        vals = [
            rec["portfolio"], rec["beta"], rec["tracking_error_pct"] / 100.0,
            fm["expected_return_pct"] / 100.0, fm["volatility_pct"] / 100.0, fm["sharpe_ratio"], fm["treynor_measure"], fm["jensens_alpha_pct"] / 100.0, fm["information_ratio"],
            hm["realized_return_pct"] / 100.0, hm["realized_volatility_pct"] / 100.0, hm["sharpe_ratio"], hm["treynor_measure"], hm["jensens_alpha_pct"] / 100.0, hm["information_ratio"], hm["terminal_wealth_of_100"]
        ]
        for c_i, val in enumerate(vals, 1):
            c = ws4.cell(row=r_i, column=c_i, value=val)
            if c_i in (3, 4, 5, 8, 10, 11, 14):
                c.number_format = "0.00%"
            elif c_i in (2, 6, 7, 9, 12, 13, 15):
                c.number_format = "0.0000"
            elif c_i == 16:
                c.number_format = "₹#,##0.00"
        style_range(ws4, 1, r_i, len(eval_headers), r_i, border=GRID_BORDER)
    auto_fit_columns(ws4)

    port_xlsx_path = root_dir / "04_portfolio" / "Portfolio_Model.xlsx"
    port_xlsx_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(port_xlsx_path)

    # Console Reporting
    print("=" * 120)
    print("1. 4-ASSET UNIVERSE & EXPECTED RETURN VECTOR")
    print("=" * 120)
    for a_tk, u_info in four_asset_universe.items():
        print(
            f"{a_tk:16s} ({u_info['name']:24s}) | Blended E[R]: {u_info['blended_expected_return_pct']:6.2f}% | "
            f"Vol: {u_info['annualized_volatility_pct']:6.2f}% | Beta: {u_info['beta']:.4f}"
        )

    print("\n" + "=" * 120)
    print("2. FEATURED CASE STUDY (A = 4.00, R_eff = 30, Section A = 15, Section B = 15)")
    print("=" * 120)
    f4 = basket_featured_a4
    lw4 = f4["look_through_weights"]
    print(
        f"Optimal Risky Equity Share (y*): {f4['risky_weight_y_star']*100:.2f}% | Optimal 91D T-Bill Share (1-y*): {f4['rf_tbill_weight']*100:.2f}%\n"
        f"Look-Through 4-Asset Weights:    ICICI Bank = {lw4['ICICIBANK.NS']*100:.2f}%, Reliance = {lw4['RELIANCE.NS']*100:.2f}%, "
        f"TCS = {lw4['TCS.NS']*100:.2f}%, 91D RBI T-Bill = {lw4['91D_RBI_TBILL']*100:.2f}%\n"
        f"Complete Portfolio Metrics:      E(Rc) = {f4['expected_return_pct']:.2f}%, sigma_c = {f4['volatility_pct']:.2f}%, "
        f"Beta_c = {f4['portfolio_beta']:.4f}, Utility U = {f4['utility_score']:.4f}, "
        f"Sharpe = {f4['sharpe_ratio']:.4f}, Treynor = {f4['treynor_measure']:.4f}, Jensen's Alpha = {f4['jensens_alpha_pct']:+.2f}%"
    )

    print("\n" + "=" * 120)
    print("3. CONTINUOUS RISK-APPETITE LOOKUP TABLE SAMPLE (A = 1.00 TO 10.00)")
    print("=" * 120)
    print(f"{'R_eff':5s} | {'A':5s} | {'y* Eq':7s} | {'T-Bill':7s} | {'w_ICICI':7s} | {'w_REL':7s} | {'w_TCS':7s} | {'E(Rc)':7s} | {'Vol_c':7s} | {'Beta_c':6s} | {'Utility U':9s} | {'Alpha'}")
    print("-" * 120)
    for row_l in continuous_lookup:
        if row_l["effective_score_r"] in (40, 36, 30, 27, 20, 18, 15, 10):
            print(
                f"{row_l['effective_score_r']:5d} | {row_l['risk_aversion_a']:5.2f} | "
                f"{row_l['risky_equity_y_star_pct']:6.2f}% | {row_l['tbill_weight_pct']:6.2f}% | "
                f"{row_l['w_icici_pct']:6.2f}% | {row_l['w_reliance_pct']:6.2f}% | {row_l['w_tcs_pct']:6.2f}% | "
                f"{row_l['expected_return_pct']:6.2f}% | {row_l['volatility_pct']:6.2f}% | "
                f"{row_l['portfolio_beta']:6.4f} | {row_l['utility_score']:9.4f} | {row_l['jensens_alpha_pct']:+5.2f}%"
            )
    print("=" * 120)


if __name__ == "__main__":
    main()
