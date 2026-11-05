import json
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import openpyxl
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


# Styling Palette
NAVY_HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
SUBHEADER_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
HIGHLIGHT_GREEN = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
HIGHLIGHT_GOLD = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
ACCENT_FILL = PatternFill(start_color="EDF2F8", end_color="EDF2F8", fill_type="solid")

FONT_FAMILY = "Calibri"
TITLE_FONT = Font(name=FONT_FAMILY, size=13, bold=True, color="1F4E78")
SECTION_FONT = Font(name=FONT_FAMILY, size=11, bold=True, color="1F4E78")
HEADER_FONT = Font(name=FONT_FAMILY, size=10, bold=True, color="FFFFFF")
BOLD_FONT = Font(name=FONT_FAMILY, size=10, bold=True, color="000000")
REGULAR_FONT = Font(name=FONT_FAMILY, size=10, bold=False, color="000000")
ITALIC_FONT = Font(name=FONT_FAMILY, size=9, italic=True, color="333333")

THIN_GRAY = Side(border_style="thin", color="D9D9D9")
MED_NAVY = Side(border_style="medium", color="1F4E78")
DOUBLE_BOTTOM = Side(border_style="double", color="1F4E78")

GRID_BORDER = Border(left=THIN_GRAY, right=THIN_GRAY, top=THIN_GRAY, bottom=THIN_GRAY)
TOTAL_BORDER = Border(top=THIN_GRAY, bottom=DOUBLE_BOTTOM, left=THIN_GRAY, right=THIN_GRAY)
HEADER_BORDER = Border(left=THIN_GRAY, right=THIN_GRAY, top=MED_NAVY, bottom=MED_NAVY)

FMT_PRICE = "₹#,##0.00"
FMT_INR = "₹#,##0"
FMT_PCT = "0.00%"
FMT_DEC = "0.0000"


def style_range(ws, min_col, min_row, max_col, max_row, font=None, fill=None, border=None, alignment=None, num_format=None):
    for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
        for cell in row:
            if font:
                cell.font = font
            if fill:
                cell.fill = fill
            if border:
                cell.border = border
            if alignment:
                cell.alignment = alignment
            if num_format:
                cell.number_format = num_format


def auto_fit_columns(ws, min_width=13, max_width=44):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            v_str = str(cell.value or "")
            if v_str.startswith("="):
                max_len = max(max_len, 14)
            else:
                max_len = max(max_len, len(v_str))
        ws.column_dimensions[col_letter].width = max(min_width, min(max_len + 4, max_width))


def update_portfolio_model_workbook(root_dir: Path, portfolio_data: dict):
    port_path = root_dir / "04_portfolio" / "Portfolio_Model.xlsx"
    wb = openpyxl.Workbook()

    cov_4x4 = portfolio_data["annualized_covariance_matrix_4x4"]
    four_assets = portfolio_data["four_asset_universe"]
    universe_keys = ["ICICIBANK.NS", "RELIANCE.NS", "TCS.NS", "91D_RBI_TBILL"]
    f4 = portfolio_data["featured_case_a4"]

    # ----------------------------------------------------
    # TAB 1: MVO_&_Covariance
    # ----------------------------------------------------
    ws1 = wb.active
    ws1.title = "MVO_&_Covariance"
    ws1.views.sheetView[0].showGridLines = True
    ws1["A1"] = "4-ASSET UNIVERSE (3 EQUITIES + 91D RBI T-BILL), 4x4 COVARIANCE MATRIX & 4-ASSET WEIGHTS"
    ws1["A1"].font = TITLE_FONT

    ws1["A3"] = "1. 4-ASSET UNIVERSE & BLENDED EXPECTED RETURN VECTOR"
    ws1["A3"].font = SECTION_FONT
    headers_u = ["Asset / Ticker", "Asset Class", "CAPM Ke / Rf (%)", "DCF/DDM 5Y IRR (%)", "Blended E(R) (%)", "Annualized Vol (%)", "Beta (β)"]
    for c_i, h in enumerate(headers_u, 1):
        ws1.cell(row=4, column=c_i, value=h)
    style_range(ws1, 1, 4, len(headers_u), 4, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    for r_i, a_tk in enumerate(universe_keys, start=5):
        u_info = four_assets[a_tk]
        ws1.cell(row=r_i, column=1, value=a_tk).font = BOLD_FONT
        ws1.cell(row=r_i, column=2, value=u_info["asset_class"]).font = REGULAR_FONT
        ws1.cell(row=r_i, column=3, value=u_info["capm_ke_pct"] / 100.0).number_format = FMT_PCT
        ws1.cell(row=r_i, column=4, value=u_info["dcf_5y_irr_pct"] / 100.0).number_format = FMT_PCT
        ws1.cell(row=r_i, column=5, value=u_info["blended_expected_return_pct"] / 100.0).number_format = FMT_PCT
        ws1.cell(row=r_i, column=6, value=u_info["annualized_volatility_pct"] / 100.0).number_format = FMT_PCT
        ws1.cell(row=r_i, column=7, value=u_info["beta"]).number_format = FMT_DEC
        style_range(ws1, 1, r_i, 7, r_i, border=GRID_BORDER)

    ws1["A11"] = "2. 4x4 ANNUALIZED SAMPLE COVARIANCE MATRIX (252 TRADING DAYS)"
    ws1["A11"].font = SECTION_FONT
    ws1.cell(row=12, column=1, value="Asset \\ Asset")
    for c_i, tk in enumerate(universe_keys, start=2):
        ws1.cell(row=12, column=c_i, value=tk)
    style_range(ws1, 1, 12, 5, 12, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    for r_i, tk_r in enumerate(universe_keys, start=13):
        ws1.cell(row=r_i, column=1, value=tk_r).font = BOLD_FONT
        for c_i, tk_c in enumerate(universe_keys, start=2):
            c = ws1.cell(row=r_i, column=c_i, value=cov_4x4[tk_r][tk_c])
            c.number_format = "0.000000"
        style_range(ws1, 1, r_i, 5, r_i, border=GRID_BORDER)

    ws1["A19"] = "3. MEAN-VARIANCE OPTIMIZATION & 4-ASSET COMPLETE PORTFOLIO WEIGHTS (Rf = 91D T-BILL @ 6.65%)"
    ws1["A19"].font = SECTION_FONT
    mvo_4asset_headers = [
        "Portfolio Strategy / Profile", "ICICIBANK.NS", "RELIANCE.NS", "TCS.NS", "91D_RBI_TBILL",
        "Expected Return E[R]", "Volatility (σ)", "Portfolio Beta", "Sharpe Ratio", "Jensen's Alpha (%)"
    ]
    for c_i, h in enumerate(mvo_4asset_headers, 1):
        ws1.cell(row=20, column=c_i, value=h)
    style_range(ws1, 1, 20, len(mvo_4asset_headers), 20, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    mvo_4asset_rows = [
        ("Max-Sharpe Tangency / Aggressive (A=2.20)", 0.3890, 0.3791, 0.2319, 0.0000, 0.1442, 0.1574, 0.9874, 0.4935, 0.0185),
        ("Featured Moderate-Growth Case (A=4.00, R=30)", 0.3050, 0.2972, 0.1818, 0.2159, 0.1274, 0.1234, 0.7742, 0.4935, 0.0145),
        ("Balanced Complete Basket (A=4.90, R=27)", 0.2490, 0.2426, 0.1484, 0.3600, 0.1162, 0.1007, 0.6320, 0.4935, 0.0118),
        ("Defensive Complete Basket (A=8.50, R=15)", 0.1435, 0.1399, 0.0856, 0.6310, 0.0952, 0.0581, 0.3643, 0.4940, 0.0068),
        ("Global Minimum Variance (GMV - Equity Only)", 0.4384, 0.2547, 0.3069, 0.0000, 0.1417, 0.1548, 0.9581, 0.4858, 0.0177),
        ("Equal-Weight Benchmark (1/3 Equity Each)", 0.3333, 0.3333, 0.3333, 0.0000, 0.1427, 0.1564, 0.9657, 0.4875, 0.0183),
    ]
    for r_i, (plabel, w1, w2, w3, w4, er, vol, beta, sh, ja) in enumerate(mvo_4asset_rows, start=21):
        ws1.cell(row=r_i, column=1, value=plabel).font = BOLD_FONT
        ws1.cell(row=r_i, column=2, value=w1).number_format = FMT_PCT
        ws1.cell(row=r_i, column=3, value=w2).number_format = FMT_PCT
        ws1.cell(row=r_i, column=4, value=w3).number_format = FMT_PCT
        ws1.cell(row=r_i, column=5, value=w4).number_format = FMT_PCT
        ws1.cell(row=r_i, column=6, value=er).number_format = FMT_PCT
        ws1.cell(row=r_i, column=7, value=vol).number_format = FMT_PCT
        ws1.cell(row=r_i, column=8, value=beta).number_format = FMT_DEC
        ws1.cell(row=r_i, column=9, value=sh).number_format = FMT_DEC
        ws1.cell(row=r_i, column=10, value=ja).number_format = FMT_PCT
        style_range(ws1, 1, r_i, len(mvo_4asset_headers), r_i, border=GRID_BORDER)
        if "A=4.00" in plabel:
            style_range(ws1, 1, r_i, len(mvo_4asset_headers), r_i, fill=HIGHLIGHT_GREEN, font=BOLD_FONT, border=GRID_BORDER)
            for c_k in [2, 3, 4, 5, 6, 7, 10]:
                ws1.cell(row=r_i, column=c_k).number_format = FMT_PCT
            for c_k in [8, 9]:
                ws1.cell(row=r_i, column=c_k).number_format = FMT_DEC
    auto_fit_columns(ws1)

    # ----------------------------------------------------
    # TAB 2: Utility_Baskets_&_Prudence
    # ----------------------------------------------------
    ws2 = wb.create_sheet(title="Utility_Baskets_&_Prudence")
    ws2.views.sheetView[0].showGridLines = True
    ws2["A1"] = "FEATURED A=4.00 CASE STUDY, RUPEE CAPITAL SPLITS & UTILITY-OPTIMAL COMPLETE PORTFOLIOS"
    ws2["A1"].font = TITLE_FONT

    ws2["A3"] = "1. CANONICAL UTILITY BASKETS, PRUDENCE OVERRIDE & RUPEE CAPITAL SPLITS"
    ws2["A3"].font = SECTION_FONT

    u_headers_extended = [
        "Investor Profile", "Sec A", "Sec B", "Eff. R", "Risk Aversion (A)",
        "Risky Equity (y*)", "91D T-Bill (1-y*)", "w_ICICI (%)", "w_Reliance (%)", "w_TCS (%)", "w_TBill (%)",
        "Complete E[Rc]", "Complete Vol (σc)", "Complete Beta", "Utility Score (U)",
        "Lump Sum: ICICI (₹)", "Lump Sum: Reliance (₹)", "Lump Sum: TCS (₹)", "Lump Sum: T-Bill (₹)", "Total Lump Sum (₹10L)",
        "SIP: ICICI (₹/mo)", "SIP: Reliance (₹/mo)", "SIP: TCS (₹/mo)", "SIP: T-Bill (₹/mo)", "Total SIP (₹25k/mo)"
    ]
    for c_i, h in enumerate(u_headers_extended, 1):
        ws2.cell(row=4, column=c_i, value=h)
    style_range(ws2, 1, 4, len(u_headers_extended), 4, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    profile_keys = ["Featured_Case_A4", "Aggressive", "Balanced", "Defensive", "Prudence_Override_Example"]
    lump_base = 1000000.0
    sip_base = 25000.0

    for r_i, bkey in enumerate(profile_keys, start=5):
        b = portfolio_data["utility_baskets"][bkey]
        q = b["questionnaire"]
        lw = b["look_through_weights"]
        w_icici = lw["ICICIBANK.NS"]
        w_rel = lw["RELIANCE.NS"]
        w_tcs = lw["TCS.NS"]
        w_tb = b["rf_tbill_weight"]

        row_vals = [
            b["profile_name"], q["section_a_ability"], q["section_b_willingness"], q["effective_score_r"], q["risk_aversion_a"],
            b["risky_weight_y_star"], b["rf_tbill_weight"], w_icici, w_rel, w_tcs, w_tb,
            b["expected_return"], b["volatility"], b["portfolio_beta"], b["utility_score"],
            round(lump_base * w_icici), round(lump_base * w_rel), round(lump_base * w_tcs), round(lump_base * w_tb), round(lump_base),
            round(sip_base * w_icici), round(sip_base * w_rel), round(sip_base * w_tcs), round(sip_base * w_tb), round(sip_base),
        ]
        for c_i, val in enumerate(row_vals, 1):
            cell = ws2.cell(row=r_i, column=c_i, value=val)
            if c_i in (6, 7, 8, 9, 10, 11, 12, 13):
                cell.number_format = FMT_PCT
            elif c_i in (5, 14, 15):
                cell.number_format = FMT_DEC
            elif c_i >= 16:
                cell.number_format = FMT_INR
        style_range(ws2, 1, r_i, len(u_headers_extended), r_i, border=GRID_BORDER)
        if bkey == "Featured_Case_A4":
            style_range(ws2, 1, r_i, len(u_headers_extended), r_i, fill=HIGHLIGHT_GREEN, font=BOLD_FONT, border=GRID_BORDER)
            for c_i in (6, 7, 8, 9, 10, 11, 12, 13):
                ws2.cell(row=r_i, column=c_i).number_format = FMT_PCT
            for c_i in (5, 14, 15):
                ws2.cell(row=r_i, column=c_i).number_format = FMT_DEC
            for c_i in range(16, 26):
                ws2.cell(row=r_i, column=c_i).number_format = FMT_INR
        elif bkey == "Prudence_Override_Example":
            style_range(ws2, 1, r_i, len(u_headers_extended), r_i, fill=HIGHLIGHT_GOLD, font=BOLD_FONT, border=GRID_BORDER)
            for c_i in (6, 7, 8, 9, 10, 11, 12, 13):
                ws2.cell(row=r_i, column=c_i).number_format = FMT_PCT
            for c_i in (5, 14, 15):
                ws2.cell(row=r_i, column=c_i).number_format = FMT_DEC
            for c_i in range(16, 26):
                ws2.cell(row=r_i, column=c_i).number_format = FMT_INR

    # Section 2: Continuous Lookup Table
    ws2["A12"] = "2. CONTINUOUS RISK-APPETITE LOOKUP SCHEDULE (R_eff = 40 DOWN TO 10 | A = 1.00 TO 10.00)"
    ws2["A12"].font = SECTION_FONT
    lookup_headers = [
        "Effective Score R", "Risk Aversion A", "Risky Equity y* (%)", "91D T-Bill (%)",
        "w_ICICI (%)", "w_Reliance (%)", "w_TCS (%)", "Complete E[Rc] (%)", "Complete Vol σc (%)",
        "Complete Beta βc", "Utility Score U", "Sharpe Ratio", "Treynor Measure", "Jensen's Alpha (%)"
    ]
    for c_i, h in enumerate(lookup_headers, 1):
        ws2.cell(row=13, column=c_i, value=h)
    style_range(ws2, 1, 13, len(lookup_headers), 13, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    for idx_l, lrow in enumerate(portfolio_data["continuous_risk_lookup_table"], start=14):
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
                c.number_format = FMT_PCT
            elif c_i in (10, 11, 12, 13):
                c.number_format = FMT_DEC
        style_range(ws2, 1, idx_l, len(lookup_headers), idx_l, border=GRID_BORDER)
        if abs(lrow["risk_aversion_a"] - 4.00) < 1e-6:
            style_range(ws2, 1, idx_l, len(lookup_headers), idx_l, fill=HIGHLIGHT_GREEN, font=BOLD_FONT, border=GRID_BORDER)
            ws2.cell(row=idx_l, column=2).number_format = "0.00"
            for c_i in (3, 4, 5, 6, 7, 8, 9, 14):
                ws2.cell(row=idx_l, column=c_i).number_format = FMT_PCT
            for c_i in (10, 11, 12, 13):
                ws2.cell(row=idx_l, column=c_i).number_format = FMT_DEC
    auto_fit_columns(ws2)

    # ----------------------------------------------------
    # TAB 3: 20Y_SIP_Glide_Path
    # ----------------------------------------------------
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

    for r_i, srow in enumerate(portfolio_data["sip_lifecycle_20y"]["yearly_schedule"], start=4):
        vals = [
            srow["year"], srow["investor_age"], srow["lifecycle_phase"], srow["active_basket"],
            srow["risk_aversion_a"], srow["equity_allocation_pct"] / 100.0, srow["tbill_allocation_pct"] / 100.0,
            srow["monthly_sip_inr"], srow["annual_contribution_inr"], srow["cumulative_invested_cr"],
            srow["deterministic_corpus_cr"], srow["mc_p10_corpus_cr"], srow["mc_p50_median_corpus_cr"], srow["mc_p90_corpus_cr"]
        ]
        for c_i, val in enumerate(vals, 1):
            c = ws3.cell(row=r_i, column=c_i, value=val)
            if c_i in (6, 7):
                c.number_format = FMT_PCT
            elif c_i in (8, 9):
                c.number_format = FMT_INR
            elif c_i >= 10:
                c.number_format = "₹#,##0.0000"
        style_range(ws3, 1, r_i, len(sip_headers), r_i, border=GRID_BORDER)
    auto_fit_columns(ws3)

    # ----------------------------------------------------
    # TAB 4: 4_Ratio_Evaluation
    # ----------------------------------------------------
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

    for r_i, rec in enumerate(portfolio_data["evaluation_4_metrics"], start=4):
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
                c.number_format = FMT_PCT
            elif c_i in (2, 6, 7, 9, 12, 13, 15):
                c.number_format = FMT_DEC
            elif c_i == 16:
                c.number_format = FMT_PRICE
        style_range(ws4, 1, r_i, len(eval_headers), r_i, border=GRID_BORDER)
        if "A=4.00" in rec["portfolio"]:
            style_range(ws4, 1, r_i, len(eval_headers), r_i, fill=HIGHLIGHT_GREEN, font=BOLD_FONT, border=GRID_BORDER)
            for c_i in (3, 4, 5, 8, 10, 11, 14):
                ws4.cell(row=r_i, column=c_i).number_format = FMT_PCT
            for c_i in (2, 6, 7, 9, 12, 13, 15):
                ws4.cell(row=r_i, column=c_i).number_format = FMT_DEC
            ws4.cell(row=r_i, column=16).number_format = FMT_PRICE
    auto_fit_columns(ws4)

    wb.calculation.fullCalcOnLoad = True
    wb.save(port_path)
    print(f"Updated {port_path} successfully.")


def update_master_valuation_workbooks(root_dir: Path, portfolio_data: dict):
    master_path = root_dir / "02_excel_valuation" / "Master_Valuation_Model.xlsx"
    deliverable_path = root_dir / "06_deliverables" / "SA_final_workbook.xlsx"

    wb = openpyxl.load_workbook(master_path)

    # 1. Update Tab 1 (Executive_Summary_&_Setup) Universe Selection & Rejection Table
    ws1 = wb["Executive_Summary_&_Setup"]

    # Clear previous rows from row 24 onwards
    max_r = max(ws1.max_row, 36)
    for r in range(24, max_r + 1):
        for c in range(1, 5):
            ws1.cell(row=r, column=c, value=None)

    updated_universe_rows = [
        ("ICICI Bank Ltd (ICICIBANK.NS)", "Private Banking & Financial Services", "SELECTED (Core #1)", "Best-in-class private bank ROE (~17.5%), clean asset quality (Net NPA 0.45%), superior digital underwriting, and ideal candidate for 2-Stage DDM / Excess Equity Return modeling where traditional FCFF is invalid."),
        ("Reliance Industries Ltd (RELIANCE.NS)", "Energy, Telecom (Jio) & Organized Retail", "SELECTED (Core #2)", "India's premier conglomerate transitioning from O2C cash cow to high-growth consumer/digital platforms (Jio + Retail) and New Energy; demonstrates consolidated FCFF DCF cross-checked with Segmental SOTP as 5G capex peaks."),
        ("Tata Consultancy Services (TCS.NS)", "IT Services & AI Consulting", "SELECTED (Core #3)", "Industry-leading ROE (51%), negative working capital intensity, and low Nifty beta (0.82) providing defensive USD revenue hedge; ideal for testing AI disruption fears via Reverse DCF Implied Growth modeling."),
        ("91-Day RBI Treasury Bill (6.65%)", "Risk-Free Sovereign Money Market", "SELECTED (Core #4: Risk-Free Sovereign Anchor)", "Zero-default sovereign money-market instrument providing duration-matched risk-free return (6.65%) for complete portfolio allocation along the Capital Allocation Line (CAL) via Tobin's Two-Fund Separation Theorem, dampening sequence-of-returns drawdowns."),
        ("ITC Ltd (ITC.NS)", "FMCG, Cigarettes & Agri", "REJECTED (Alternative)", "Post-hotel demerger valuation is dominated by ESG tobacco taxation overhang; redundant consumer exposure already captured with higher operating leverage inside Reliance Retail."),
        ("Hindustan Unilever Ltd (HINDUNILVR.NS)", "Staples / FMCG", "REJECTED (Alternative)", "Trading at rich ~52x P/E with muted rural volume recovery (~3-4% volume growth), offering negative margin of safety under disciplined DCF assumptions."),
        ("Cummins India Ltd (CUMMINSIND.NS)", "Capital Goods / Industrials", "REJECTED (Alternative)", "Terminal value is structurally vulnerable to data-center backup genset cyclicality and long-term green hydrogen/battery storage transition risk."),
        ("Coal India Ltd (COALINDIA.NS)", "Mining & Thermal Energy", "REJECTED (Alternative)", "Finite reserve depletion and structural ESG terminal value decay post-FY35 violate perpetual Gordon Growth model assumptions."),
        ("Abbott India Ltd (ABBOTINDIA.NS)", "MNC Pharmaceuticals & Healthcare", "REJECTED (Alternative)", "Rich ~48x P/E with high revenue concentration in off-patent single-molecule therapies exposed to National List of Essential Medicines (NLEM) ceiling price cuts."),
        ("The Indian Hotels Company Ltd (INDHOTEL.NS)", "Hospitality & Leisure / Taj Hotels", "REJECTED (Alternative)", "Trading at cyclical peak multiples (>55x P/E) following post-COVID domestic travel exuberance; high operational gearing exposes earnings to discretionary travel moderation."),
        ("BSE Ltd (BSE.NS)", "Financial Market Infrastructure / Exchange", "REJECTED (Alternative)", "Extreme retail index options volume beta (>2.2x equity market beta) and heightened SEBI regulatory margin/contract size interventions introduce excessive non-fundamental regulatory drawdowns."),
    ]

    for r_i, (cname, sec, dec, rat) in enumerate(updated_universe_rows, start=24):
        ws1.cell(row=r_i, column=1, value=cname).font = BOLD_FONT
        ws1.cell(row=r_i, column=2, value=sec).font = REGULAR_FONT
        c_d = ws1.cell(row=r_i, column=3, value=dec)
        c_d.font = BOLD_FONT
        if "SELECTED" in dec:
            c_d.fill = HIGHLIGHT_GREEN
        else:
            c_d.fill = ACCENT_FILL
        ws1.cell(row=r_i, column=4, value=rat).font = REGULAR_FONT
        style_range(ws1, 1, r_i, 4, r_i, border=GRID_BORDER)

    auto_fit_columns(ws1)

    # 2. Add Dedicated 6th Tab: Portfolio_&_TBill_Allocation
    if "Portfolio_&_TBill_Allocation" in wb.sheetnames:
        del wb["Portfolio_&_TBill_Allocation"]

    ws6 = wb.create_sheet(title="Portfolio_&_TBill_Allocation")
    ws6.views.sheetView[0].showGridLines = True

    ws6["A1"] = "PORTFOLIO CONSTRUCTION & DYNAMIC 4-ASSET UTILITY ALLOCATOR (ICICI + RELIANCE + TCS + 91D T-BILL)"
    ws6["A1"].font = TITLE_FONT
    ws6["A2"] = "Live Formula-Driven Two-Fund Separation along Capital Allocation Line (CAL) | Single Source of Truth Anchors"
    ws6["A2"].font = ITALIC_FONT

    # Section 1: CAL Parameters & Risk Aversion User Input (Cell B6)
    ws6["A4"] = "1. CAPITAL ALLOCATION LINE (CAL) & INVESTOR RISK AVERSION INPUT (CELL B6)"
    ws6["A4"].font = SECTION_FONT
    for c_i, h in enumerate(["Parameter", "Value / Cell", "Formula / Basis", "Methodological Source"], 1):
        ws6.cell(row=5, column=c_i, value=h)
    style_range(ws6, 1, 5, 4, 5, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    cal_input_rows = [
        ("User Risk Aversion Coefficient (A)", 4.00, "Dynamic User Input (Cell B6)", "Default: A = 4.00 (Featured Moderate-Growth Case Study)", "0.00"),
        ("Risk-Free Rate (Rf - 91D RBI T-Bill)", "='Executive_Summary_&_Setup'!C7", "='Executive_Summary_&_Setup'!C7", "Short-Term Sovereign Money-Market Yield", FMT_PCT),
        ("Tangency Portfolio Expected Return E[R_tan]", 0.1442, "SLSQP MVO Solution (50% Ke + 50% DCF IRR)", "Blended Expected Return of Max-Sharpe Tangency Equity Basket", FMT_PCT),
        ("Tangency Portfolio Volatility (σ_tan)", 0.1574, "Sqrt(w' * Sigma * w)", "Annualized Sample Covariance of 3 Core Equities", FMT_PCT),
        ("Tangency Portfolio Beta (β_tan)", 0.9874, "Weighted Regression Beta vs Nifty 50", "5-Year Daily Log-Return OLS Beta", FMT_DEC),
        ("Capital Allocation Line (CAL) Slope / Sharpe", "=(B8-B7)/B9", "=(B8-B7)/B9", "Max-Sharpe Ratio Attainable along CAL", FMT_DEC),
        ("India Equity Risk Premium (ERP)", "='Executive_Summary_&_Setup'!C8", "='Executive_Summary_&_Setup'!C8", "Sovereign-Adjusted India ERP", FMT_PCT),
    ]
    for r_offset, (label, val_or_f, formula_lbl, note, nfmt) in enumerate(cal_input_rows, start=6):
        ws6.cell(row=r_offset, column=1, value=label).font = BOLD_FONT if "Risk Aversion" in label else REGULAR_FONT
        c_v = ws6.cell(row=r_offset, column=2, value=val_or_f)
        c_v.font = BOLD_FONT if "Risk Aversion" in label else REGULAR_FONT
        c_v.number_format = nfmt
        ws6.cell(row=r_offset, column=3, value=formula_lbl).font = ITALIC_FONT
        ws6.cell(row=r_offset, column=4, value=note).font = REGULAR_FONT
        style_range(ws6, 1, r_offset, 4, r_offset, border=GRID_BORDER)
        if "Risk Aversion" in label:
            style_range(ws6, 1, r_offset, 4, r_offset, fill=HIGHLIGHT_GOLD, font=BOLD_FONT, border=GRID_BORDER)
            ws6.cell(row=r_offset, column=2).number_format = "0.00"

    # Optimization Result: y* and 1-y*
    ws6["A14"] = "Optimal Risky Equity Portfolio Weight (y*)"
    ws6["A14"].font = BOLD_FONT
    ws6["B14"] = "=MIN(1.0, (B8-B7)/(B6*(B9^2)))"
    ws6["B14"].font = BOLD_FONT
    ws6["B14"].number_format = FMT_PCT
    ws6["C14"] = "=(B8-B7)/(B6*(B9^2))"
    ws6["C14"].font = ITALIC_FONT
    ws6["D14"] = "Optimal Equity Share along CAL for User Risk Aversion A"
    style_range(ws6, 1, 14, 4, 14, fill=HIGHLIGHT_GREEN, font=BOLD_FONT, border=GRID_BORDER)

    ws6["A15"] = "Optimal 91-Day RBI T-Bill Weight (1 - y*)"
    ws6["A15"].font = BOLD_FONT
    ws6["B15"] = "=1-B14"
    ws6["B15"].font = BOLD_FONT
    ws6["B15"].number_format = FMT_PCT
    ws6["C15"] = "=1-B14"
    ws6["C15"].font = ITALIC_FONT
    ws6["D15"] = "Risk-Free Sovereign Money Market Weight in Complete Portfolio"
    style_range(ws6, 1, 15, 4, 15, fill=HIGHLIGHT_GREEN, font=BOLD_FONT, border=GRID_BORDER)

    # Section 2: Look-Through 4-Asset Allocation & Capital Splits
    ws6["A17"] = "2. LOOK-THROUGH 4-ASSET COMPLETE PORTFOLIO ALLOCATION & RUPEE CAPITAL SPLITS"
    ws6["A17"].font = SECTION_FONT

    ws6["A18"] = "Base Portfolio Lump Sum Capital (₹)"
    ws6["B18"] = 1000000
    ws6["B18"].number_format = FMT_INR
    ws6["C18"] = "User Capital Input"
    ws6["D18"] = "₹10,00,000 Portfolio Base"
    style_range(ws6, 1, 18, 4, 18, border=GRID_BORDER)

    ws6["A19"] = "Base Monthly Step-Up SIP (₹/month)"
    ws6["B19"] = 25000
    ws6["B19"].number_format = FMT_INR
    ws6["C19"] = "User SIP Input"
    ws6["D19"] = "₹25,000/month Initial SIP Contribution"
    style_range(ws6, 1, 19, 4, 19, border=GRID_BORDER)

    sec2_headers = [
        "Asset Name", "Ticker / Instrument", "Asset Class & Role", "Tangency Weight (wi)",
        "Complete Weight (Wc)", "Lump Sum Split (₹)", "Monthly SIP Split (₹)",
        "Blended E[R] (%)", "Annualized Vol (σ)", "Beta (β)"
    ]
    for c_i, h in enumerate(sec2_headers, 1):
        ws6.cell(row=21, column=c_i, value=h)
    style_range(ws6, 1, 21, len(sec2_headers), 21, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    asset_table_rows = [
        ("ICICI Bank Ltd", "ICICIBANK.NS", "Domestic Private Banking Equity", 0.3890, "=$B$14*D22", "=$B$18*E22", "=$B$19*E22", 0.1399, 0.1955, 0.9663),
        ("Reliance Industries Ltd", "RELIANCE.NS", "Conglomerate (O2C, Jio, Retail) Equity", 0.3791, "=$B$14*D23", "=$B$18*E23", "=$B$19*E23", 0.1555, 0.2233, 1.1125),
        ("Tata Consultancy Services Ltd", "TCS.NS", "Global IT Services & AI Equity", 0.2319, "=$B$14*D24", "=$B$18*E24", "=$B$19*E24", 0.1328, 0.2285, 0.8184),
        ("91-Day RBI Treasury Bill", "91D_RBI_TBILL", "Risk-Free Sovereign Money Market", 0.0000, "=$B$15", "=$B$18*E25", "=$B$19*E25", "=$B$7", 0.0000, 0.0000),
    ]
    for r_idx, (aname, tick, aclass, w_tan, f_wc, f_lump, f_sip, er, vol, beta) in enumerate(asset_table_rows, start=22):
        ws6.cell(row=r_idx, column=1, value=aname).font = BOLD_FONT
        ws6.cell(row=r_idx, column=2, value=tick).font = REGULAR_FONT
        ws6.cell(row=r_idx, column=3, value=aclass).font = REGULAR_FONT
        ws6.cell(row=r_idx, column=4, value=w_tan).number_format = FMT_PCT
        ws6.cell(row=r_idx, column=5, value=f_wc).number_format = FMT_PCT
        ws6.cell(row=r_idx, column=6, value=f_lump).number_format = FMT_INR
        ws6.cell(row=r_idx, column=7, value=f_sip).number_format = FMT_INR
        ws6.cell(row=r_idx, column=8, value=er).number_format = FMT_PCT
        ws6.cell(row=r_idx, column=9, value=vol).number_format = FMT_PCT
        ws6.cell(row=r_idx, column=10, value=beta).number_format = FMT_DEC
        style_range(ws6, 1, r_idx, len(sec2_headers), r_idx, border=GRID_BORDER)

    # Total Row 26
    ws6.cell(row=26, column=1, value="Total Complete Portfolio").font = BOLD_FONT
    ws6.cell(row=26, column=2, value="4-Asset Complete").font = ITALIC_FONT
    ws6.cell(row=26, column=3, value="100% Risk-Calibrated").font = ITALIC_FONT
    ws6.cell(row=26, column=4, value="=SUM(D22:D25)").number_format = FMT_PCT
    ws6.cell(row=26, column=5, value="=SUM(E22:E25)").number_format = FMT_PCT
    ws6.cell(row=26, column=6, value="=SUM(F22:F25)").number_format = FMT_INR
    ws6.cell(row=26, column=7, value="=SUM(G22:G25)").number_format = FMT_INR
    ws6.cell(row=26, column=8, value="=B30").number_format = FMT_PCT
    ws6.cell(row=26, column=9, value="=B31").number_format = FMT_PCT
    ws6.cell(row=26, column=10, value="=B32").number_format = FMT_DEC
    style_range(ws6, 1, 26, len(sec2_headers), 26, fill=SUBHEADER_FILL, font=BOLD_FONT, border=TOTAL_BORDER)

    # Section 3: Performance, Risk, Utility & Ratios
    ws6["A28"] = "3. COMPLETE PORTFOLIO EXPECTED RETURN, VOLATILITY, UTILITY & PERFORMANCE RATIOS"
    ws6["A28"].font = SECTION_FONT
    for c_i, h in enumerate(["Performance Metric", "Live Computed Value", "Excel Formula", "Analytical Significance"], 1):
        ws6.cell(row=29, column=c_i, value=h)
    style_range(ws6, 1, 29, 4, 29, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    perf_rows = [
        ("Complete Portfolio Expected Return E[R_c]", "=B14*B8 + B15*B7", "=B14*B8 + B15*B7", "Weighted Return of Equity Basket + 91D T-Bill", FMT_PCT),
        ("Complete Portfolio Volatility (σ_c)", "=B14*B9", "=B14*B9", "Scales linearly with y* along the Capital Allocation Line", FMT_PCT),
        ("Complete Portfolio Beta (β_c)", "=B14*B10", "=B14*B10", "Weighted Beta relative to Nifty 50 Benchmark", FMT_DEC),
        ("Quadratic Utility Score (U)", "=B30 - 0.5*B6*(B31^2)", "=B30 - 0.5*B6*(B31^2)", "U = E(R_c) - 0.5 * A * (σ_c)^2", FMT_DEC),
        ("Sharpe Ratio (CAL Slope)", "=(B30 - B7)/B31", "=(B30 - B7)/B31", "Invariant along CAL by Separation Theorem = 0.4935", FMT_DEC),
        ("Treynor Measure", "=(B30 - B7)/B32", "=(B30 - B7)/B32", "Excess Return per Unit of Systematic Risk = 0.0786", FMT_DEC),
        ("Jensen's Alpha (α)", "=(B30 - B7) - B32*B12", "=(B30 - B7) - B32*B12", "Equilibrium Alpha above CAPM Benchmark = +1.45%", FMT_PCT),
        ("Information Ratio (vs Nifty 50)", 0.0144, "Active Return / Tracking Error (6.84%)", "Active management efficiency relative to market benchmark", FMT_DEC),
    ]
    for r_offset, (label, f_val, f_str, note, nfmt) in enumerate(perf_rows, start=30):
        ws6.cell(row=r_offset, column=1, value=label).font = BOLD_FONT if "Expected Return" in label or "Sharpe" in label or "Alpha" in label else REGULAR_FONT
        c = ws6.cell(row=r_offset, column=2, value=f_val)
        c.font = BOLD_FONT if "Expected Return" in label or "Sharpe" in label or "Alpha" in label else REGULAR_FONT
        c.number_format = nfmt
        ws6.cell(row=r_offset, column=3, value=f_str).font = ITALIC_FONT
        ws6.cell(row=r_offset, column=4, value=note).font = REGULAR_FONT
        style_range(ws6, 1, r_offset, 4, r_offset, border=GRID_BORDER)
        if "Expected Return" in label or "Sharpe" in label or "Alpha" in label:
            style_range(ws6, 1, r_offset, 4, r_offset, fill=HIGHLIGHT_GREEN, font=BOLD_FONT, border=GRID_BORDER)
            ws6.cell(row=r_offset, column=2).number_format = nfmt

    # Section 4: Continuous Sensitivity Lookup Table
    ws6["A39"] = "4. CONTINUOUS RISK-APPETITE SENSITIVITY LOOKUP SCHEDULE (A = 1.00 TO 10.00)"
    ws6["A39"].font = SECTION_FONT
    lookup_hdr = [
        "Eff. Score R", "Risk Aversion A", "Risky Share y* (%)", "91D T-Bill (1-y*) (%)",
        "w_ICICI (%)", "w_Reliance (%)", "w_TCS (%)", "Complete E[Rc]", "Complete Vol σc",
        "Complete Beta βc", "Utility Score U", "Sharpe Ratio", "Treynor Measure", "Jensen's Alpha (%)"
    ]
    for c_i, h in enumerate(lookup_hdr, 1):
        ws6.cell(row=40, column=c_i, value=h)
    style_range(ws6, 1, 40, len(lookup_hdr), 40, font=HEADER_FONT, fill=NAVY_HEADER_FILL, border=HEADER_BORDER)

    for idx_l, lrow in enumerate(portfolio_data["continuous_risk_lookup_table"], start=41):
        vals = [
            lrow["effective_score_r"], lrow["risk_aversion_a"],
            lrow["risky_equity_y_star_pct"] / 100.0, lrow["tbill_weight_pct"] / 100.0,
            lrow["w_icici_pct"] / 100.0, lrow["w_reliance_pct"] / 100.0, lrow["w_tcs_pct"] / 100.0,
            lrow["expected_return_pct"] / 100.0, lrow["volatility_pct"] / 100.0,
            lrow["portfolio_beta"], lrow["utility_score"],
            lrow["sharpe_ratio"], lrow["treynor_measure"], lrow["jensens_alpha_pct"] / 100.0,
        ]
        for c_i, v in enumerate(vals, 1):
            c = ws6.cell(row=idx_l, column=c_i, value=v)
            if c_i == 2:
                c.number_format = "0.00"
            elif c_i in (3, 4, 5, 6, 7, 8, 9, 14):
                c.number_format = FMT_PCT
            elif c_i in (10, 11, 12, 13):
                c.number_format = FMT_DEC
        style_range(ws6, 1, idx_l, len(lookup_hdr), idx_l, border=GRID_BORDER)
        if abs(lrow["risk_aversion_a"] - 4.00) < 1e-6:
            style_range(ws6, 1, idx_l, len(lookup_hdr), idx_l, fill=HIGHLIGHT_GREEN, font=BOLD_FONT, border=GRID_BORDER)
            ws6.cell(row=idx_l, column=2).number_format = "0.00"
            for c_i in (3, 4, 5, 6, 7, 8, 9, 14):
                ws6.cell(row=idx_l, column=c_i).number_format = FMT_PCT
            for c_i in (10, 11, 12, 13):
                ws6.cell(row=idx_l, column=c_i).number_format = FMT_DEC

    auto_fit_columns(ws6)

    # 3. Apply 3-Color Conditional Formatting (Red to Yellow to Green) to all 5x5 Sensitivity Matrices
    rule_3color = ColorScaleRule(
        start_type="min",
        start_color="F8696B",  # Soft Red
        mid_type="percentile",
        mid_value=50,
        mid_color="FFEB84",    # Soft Yellow
        end_type="max",
        end_color="63BE7B",    # Soft Green
    )

    wb["ICICI_Bank_DDM"].conditional_formatting.add("B68:F72", rule_3color)
    wb["Reliance_DCF_SOTP"].conditional_formatting.add("B88:F92", rule_3color)
    wb["TCS_DCF_Reverse"].conditional_formatting.add("B76:F80", rule_3color)

    # 4. Ensure all formula cells are fully cached on load
    wb.calculation.fullCalcOnLoad = True

    # 5. Save Master Valuation Workbook & Deliverable Workbook
    wb.save(master_path)
    shutil.copy2(master_path, deliverable_path)
    print(f"Updated {master_path} successfully.")
    print(f"Copied updated final deliverable to {deliverable_path} successfully.")


def main():
    root_dir = Path(__file__).resolve().parent.parent
    cleaned_dir = root_dir / "01_data" / "cleaned"

    with open(cleaned_dir / "portfolio_results.json", "r", encoding="utf-8") as f:
        portfolio_data = json.load(f)

    print("Step 1: Updating 04_portfolio/Portfolio_Model.xlsx...")
    update_portfolio_model_workbook(root_dir, portfolio_data)

    print("Step 2: Updating 02_excel_valuation/Master_Valuation_Model.xlsx and 06_deliverables/SA_final_workbook.xlsx...")
    update_master_valuation_workbooks(root_dir, portfolio_data)

    print("Step 3: Verification of updated workbooks...")
    for wb_p in [
        root_dir / "04_portfolio" / "Portfolio_Model.xlsx",
        root_dir / "02_excel_valuation" / "Master_Valuation_Model.xlsx",
        root_dir / "06_deliverables" / "SA_final_workbook.xlsx",
    ]:
        loaded_wb = openpyxl.load_workbook(wb_p, data_only=False)
        print(f"  - {wb_p.name}: {len(loaded_wb.sheetnames)} sheets -> {loaded_wb.sheetnames}")

    print("\nAll workbooks successfully updated and verified!")


if __name__ == "__main__":
    main()
