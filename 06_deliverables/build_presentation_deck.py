import json
import os
import shutil
import sys
from pathlib import Path

import pptx
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Palette
DARK_NAVY = RGBColor(10, 25, 47)       # #0A192F
SLATE_NAVY = RGBColor(31, 78, 120)     # #1F4E78
MID_BLUE = RGBColor(41, 128, 185)      # #2980B9
LIGHT_BG = RGBColor(248, 250, 252)     # #F8FAFC
CARD_BG = RGBColor(255, 255, 255)      # #FFFFFF
CARD_ALT_BG = RGBColor(241, 245, 249)  # #F1F5F9
BORDER_COLOR = RGBColor(226, 232, 240) # #E2E8F0
TEXT_DARK = RGBColor(15, 23, 42)       # #0F172A
TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B
TEXT_LIGHT = RGBColor(255, 255, 255)   # #FFFFFF
ACCENT_GREEN = RGBColor(16, 185, 129)  # #10B981
ACCENT_GOLD = RGBColor(217, 119, 6)    # #D97706
ACCENT_RED = RGBColor(239, 68, 68)     # #EF4444


def create_header(slide, slide_num, section_name, speaker_name, roll_no, timing, title_text, subtitle_text):
    # Top banner background
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    banner.fill.solid()
    banner.fill.fore_color.rgb = DARK_NAVY
    banner.line.color.rgb = DARK_NAVY

    # Metadata badges: Slide Number, Section, Speaker
    meta_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.12), Inches(12.133), Inches(0.3))
    tf_meta = meta_box.text_frame
    tf_meta.word_wrap = True
    tf_meta.margin_left = tf_meta.margin_top = tf_meta.margin_right = tf_meta.margin_bottom = 0
    p_meta = tf_meta.paragraphs[0]
    
    # Slide Pill
    run_num = p_meta.add_run()
    run_num.text = f"SLIDE {slide_num:02d}/15   |   "
    run_num.font.bold = True
    run_num.font.size = Pt(9.5)
    run_num.font.color.rgb = ACCENT_GOLD

    # Section Pill
    run_sec = p_meta.add_run()
    run_sec.text = f"{section_name}   |   "
    run_sec.font.bold = True
    run_sec.font.size = Pt(9.5)
    run_sec.font.color.rgb = RGBColor(147, 197, 253)

    # Speaker Pill
    run_spk = p_meta.add_run()
    run_spk.text = f"Speaker: {speaker_name} (Roll: {roll_no})   |   Pacing: {timing}"
    run_spk.font.bold = False
    run_spk.font.size = Pt(9.5)
    run_spk.font.color.rgb = TEXT_LIGHT

    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.38), Inches(12.133), Inches(0.45))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    run_t = p_t.add_run()
    run_t.text = title_text
    run_t.font.bold = True
    run_t.font.size = Pt(17)
    run_t.font.color.rgb = TEXT_LIGHT

    # Slide Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.82), Inches(12.133), Inches(0.25))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    run_s = p_s.add_run()
    run_s.text = subtitle_text
    run_s.font.italic = True
    run_s.font.size = Pt(10)
    run_s.font.color.rgb = RGBColor(203, 213, 225)


def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card


def set_speaker_notes(slide, script_text, key_points, viva_tip):
    full_notes = (
        f"=== VERBATIM SPOKEN SCRIPT (45s) ===\n{script_text}\n\n"
        f"=== KEY AUDIT POINTS TO EMPHASIZE ===\n{key_points}\n\n"
        f"=== ANTICIPATED FACULTY QUESTION / DEFENSE ===\n{viva_tip}"
    )
    slide.notes_slide.notes_text_frame.text = full_notes


def build_powerpoint(root_dir: Path):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    cleaned_dir = root_dir / "01_data" / "cleaned"

    # =========================================================================
    # SLIDE 1: Title & Overview (Sasi)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    create_header(
        s1, 1, "EXECUTIVE OVERVIEW & SETUP", "Sasi", "246213618", "45 Seconds",
        "Beyond the Consensus: AI-Augmented Valuation & Risk-Calibrated Portfolio Construction",
        "Triangulated Academic Defense across Three Macro Engines: ICICI Bank, Reliance Industries & TCS"
    )

    # Left Card: Investment Thesis & Problem Statement
    add_card(s1, Inches(0.6), Inches(1.35), Inches(5.9), Inches(5.7))
    tbox1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.4))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "1. The Investment Problem & Academic Hypothesis"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    bullets_s1 = [
        ("Systematic Market Distortions:", " Short-term market pricing is distorted by media narrative biases—FOMO hype in private credit, extrapolating temporary refining cracks in conglomerates, and existential AI panic in Tier-1 IT."),
        ("Triangulated Solution:", " We construct an institutional research pipeline combining Multi-Model Intrinsic Valuation (2-Stage DDM, Consolidated DCF, Segmental SOTP, Reverse DCF), Live HuggingFace FinBERT NLP across 24 quarters of concalls, and Utility-Optimal Portfolio Optimization."),
        ("Three Macro Engines:", " Financial Intermediation (ICICI Bank), Capex & Consumer Compounder (Reliance), and Dollar-Denominated IP/Tech Consulting (TCS)."),
        ("Single Source of Truth:", " All market inputs locked as of 2026-10-30: 10Y G-Sec @ 6.85%, 91D T-Bill @ 6.65%, ERP @ 6.00%, Tax @ 25.17%, with zero circular dependencies.")
    ]
    for b_title, b_desc in bullets_s1:
        p_b = tf1.add_paragraph()
        p_b.space_before = Pt(8)
        r1 = p_b.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = TEXT_MUTED

    # Right Card: Team Roster & Methodological Constants Table
    add_card(s1, Inches(6.8), Inches(1.35), Inches(5.9), Inches(5.7))
    tbox1_r = s1.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.5), Inches(5.4))
    tf1_r = tbox1_r.text_frame
    tf1_r.word_wrap = True

    p_r = tf1_r.paragraphs[0]
    p_r.text = "2. Team Roster & Single Source of Truth Constants"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = SLATE_NAVY

    team_members = [
        ("Sasi (246213618)", "Fundamental Valuation & Accounting Lead", "Slides 1–5: DDM, DCF, SOTP & Forensic Audit"),
        ("Aditi Routray (246213548)", "AI Pipeline, FinBERT & Behavioral Lead", "Slides 6–10: Concall NLP, Benchmarks & MC"),
        ("Sankarshana Mulugundam (246213080)", "Project Lead & Portfolio Architect", "Slides 11–15: MVO, Utility Baskets & Backtest")
    ]
    for t_name, t_role, t_scope in team_members:
        p_t = tf1_r.add_paragraph()
        p_t.space_before = Pt(6)
        r_n = p_t.add_run()
        r_n.text = f"{t_name} — "
        r_n.font.bold = True
        r_n.font.size = Pt(10)
        r_n.font.color.rgb = TEXT_DARK
        r_r = p_t.add_run()
        r_r.text = f"{t_role}\nScope: {t_scope}"
        r_r.font.size = Pt(9.5)
        r_r.font.color.rgb = TEXT_MUTED

    # Constants Table
    p_c = tf1_r.add_paragraph()
    p_c.space_before = Pt(14)
    p_c.text = "Locked Macroeconomic Constants (config.json):"
    p_c.font.bold = True
    p_c.font.size = Pt(10.5)
    p_c.font.color.rgb = SLATE_NAVY

    constants_data = [
        ("Cutoff Price Date", "2026-10-30", "5Y Daily Window (1,236 Days)"),
        ("10Y G-Sec Yield (Rf_dcf)", "6.85%", "Duration-Matched for DCF/DDM"),
        ("91D T-Bill Yield (Rf_tbill)", "6.65%", "Money Market Sovereign Anchor"),
        ("Equity Risk Premium (ERP)", "6.00%", "India Sovereign-Adjusted ERP"),
        ("Effective Corporate Tax", "25.17%", "Statutory Base (Sec 115BAA)")
    ]
    for c_lbl, c_val, c_src in constants_data:
        p_row = tf1_r.add_paragraph()
        p_row.space_before = Pt(3)
        r_l = p_row.add_run()
        r_l.text = f"• {c_lbl}: "
        r_l.font.bold = True
        r_l.font.size = Pt(9.5)
        r_v = p_row.add_run()
        r_v.text = f"{c_val} ({c_src})"
        r_v.font.size = Pt(9)
        r_v.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s1,
        "Good morning Professor and members of the panel. We present 'Beyond the Consensus'—an institutional valuation study that bridges multi-model fundamental valuation, live FinBERT natural language processing, and utility-based portfolio optimization across three flagship Indian blue chips: ICICI Bank, Reliance Industries, and TCS. I am Sasi, handling Part I on fundamental valuation and forensic accounting; Aditi will present Part II on our AI pipeline; and Sankarshana will present Part III on portfolio construction.",
        "Highlight duration-matched dual risk-free rates (6.85% 10Y G-Sec vs 6.65% 91D T-Bill) and exact price cutoff of 2026-10-30.",
        "Q: Why did you choose these three stocks? A: They represent three orthogonal economic drivers—domestic credit, capex/consumption, and export technology—delivering superior diversification."
    )

    # =========================================================================
    # SLIDE 2: Universe & 10-Stock Correlation Proof (Sasi)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    create_header(
        s2, 2, "PART I: UNIVERSE SELECTION & AUDIT", "Sasi", "246213618", "45 Seconds",
        "Three-Pillar Coverage Universe, Rejection Matrix & 10-Stock Correlation Proof",
        "Empirical Diversification across 1,235 Daily Log Returns vs. Intra-Sector Clustered Peers"
    )

    # Left: Explanation & Rejections
    add_card(s2, Inches(0.6), Inches(1.35), Inches(5.9), Inches(5.7))
    tbox2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.4))
    tf2 = tbox2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "1. Coverage Rationale & 7 Rejected Alternatives"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    bullets_s2 = [
        ("Core #1 ICICI Bank:", " Best-in-class ROE (~17.5%), clean asset quality (Net NPA 0.45%), and ideal candidate for 2-Stage DDM where FCFF is invalid."),
        ("Core #2 Reliance Industries:", " Transitioning from O2C cash cow to high-growth consumer/digital platforms (Jio + Retail) and New Energy; FCFF DCF cross-verified via SOTP."),
        ("Core #3 TCS:", " Exceptional 51% ROE, negative working capital intensity, low beta (0.82), providing defensive USD revenue hedge; tested via Reverse DCF."),
        ("Core #4 91D RBI T-Bill (6.65%):", " Sovereign money-market risk-free asset for two-fund separation along the Capital Allocation Line (CAL)."),
        ("Explicit Rejection Matrix:", " Rejected ITC (tobacco tax overhang), HUL (rich 52x P/E with muted 3-4% volume growth), Cummins (diesel genset terminal risk), Coal India (post-FY35 reserve depletion), Abbott India (NLEM price ceiling cuts), INDHOTEL (cyclical peak >55x P/E), and BSE Ltd (excessive retail options regulatory beta >2.2x).")
    ]
    for b_title, b_desc in bullets_s2:
        p_b = tf2.add_paragraph()
        p_b.space_before = Pt(6)
        r1 = p_b.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_MUTED

    # Right: Correlation Heatmap Image
    add_card(s2, Inches(6.8), Inches(1.35), Inches(5.9), Inches(5.7))
    img_corr = cleaned_dir / "correlation_heatmap.png"
    if img_corr.exists():
        s2.shapes.add_picture(str(img_corr), Inches(7.0), Inches(1.5), width=Inches(5.5))

    set_speaker_notes(
        s2,
        "Rather than picking three stocks from a single sector, we selected three orthogonal pillars of the Indian economy: private credit, consumer conglomerate capex, and global USD enterprise technology. Our 10-stock correlation matrix across 1,235 daily returns proves our core triad has an average correlation of just 0.34 (ICICI-TCS is 0.26, Reliance-TCS is 0.34), far superior to intra-sector pairs like TCS and Infosys at 0.73.",
        "Stress the 7 explicit rejections—especially rejecting HUL and ITC to avoid consumer staples valuation traps—and introducing the 91D T-Bill as Core #4.",
        "Q: Why did you reject HDFC Bank? A: ICICI Bank delivered superior underwriting RoA (2.3% vs 1.9%) and avoided the post-merger deposit mobilization margin drag of HDFC Bank."
    )

    # =========================================================================
    # SLIDE 3: 5-Year Historical Financial Trajectory & Forensic Audit (Sasi)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    create_header(
        s3, 3, "PART I: UNIVERSE SELECTION & AUDIT", "Sasi", "246213618", "45 Seconds",
        "5-Year Financial Trajectory & Forensic Footnote Audit (FY22–FY26)",
        "Audit of Cash Conversion, Operating Leverage & Ind AS 116 / 24 / 37 Footnote Adjustments"
    )

    # Left: Financial Summary Table
    add_card(s3, Inches(0.6), Inches(1.35), Inches(6.4), Inches(5.7))
    tbox3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.4))
    tf3 = tbox3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "1. 5-Year Audited Financial Performance (FY22–FY26)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    fin_cards = [
        ("ICICI Bank Ltd (Domestic Private Credit Lead)", [
            "Net Interest Income (NII): Compounded at 18.1% CAGR to ₹92,400 Cr (FY26)",
            "Net Profit (PAT): ₹49,540 Cr with 17.50% Return on Equity (ROE)",
            "Underwriting Quality: Net NPA down to pristine 0.45%; NIM robust @ 4.30%",
            "Capital Adequacy: Tier-1 CAR @ 15.80% (well above RBI 11.5% regulatory floor)"
        ]),
        ("Reliance Industries Ltd (Energy & Consumer Conglomerate)", [
            "Consolidated Revenue: Reached ₹10.15 Lakh Cr; EBITDA @ ₹1.82 Lakh Cr (17.9% margin)",
            "Cash Flow Conversion: ₹1.74 Lakh Cr CFO (95.9% conversion of EBITDA)",
            "Segmental Transition: Consumer businesses (Jio + Retail) now generate >50% EBITDA",
            "Leverage Profile: Net Debt/EBITDA contained at 0.64x despite 5G capex"
        ]),
        ("Tata Consultancy Services Ltd (Global IT Services)", [
            "Revenue & EBIT: Revenue ₹2.58 Lakh Cr; EBIT ₹63,200 Cr (24.50% operating margin)",
            "Capital Efficiency: Stellar 51.0% ROE with negative working capital intensity",
            "Cash Generation: CFO/PAT of 98.2% (₹48,300 Cr CFO); Debtor days lean @ 65.8 days",
            "Balance Sheet: Zero long-term debt; ₹42,000 Cr cash and liquid sovereign investments"
        ])
    ]
    for c_title, c_points in fin_cards:
        p_c = tf3.add_paragraph()
        p_c.space_before = Pt(6)
        r_ct = p_c.add_run()
        r_ct.text = c_title
        r_ct.font.bold = True
        r_ct.font.size = Pt(10)
        r_ct.font.color.rgb = TEXT_DARK
        for pt in c_points:
            p_pt = tf3.add_paragraph()
            p_pt.space_before = Pt(2)
            r_pt = p_pt.add_run()
            r_pt.text = f"  • {pt}"
            r_pt.font.size = Pt(9)
            r_pt.font.color.rgb = TEXT_MUTED

    # Right: Forensic Footnote Audit Badges
    add_card(s3, Inches(7.3), Inches(1.35), Inches(5.4), Inches(5.7))
    tbox3_r = s3.shapes.add_textbox(Inches(7.5), Inches(1.5), Inches(5.0), Inches(5.4))
    tf3_r = tbox3_r.text_frame
    tf3_r.word_wrap = True

    p_r = tf3_r.paragraphs[0]
    p_r.text = "2. Forensic Footnote & CARO Audit Checklist"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = SLATE_NAVY

    audit_badges = [
        ("Ind AS 116 Lease Liabilities", "Capitalized lease commitments (Reliance ₹24,600 Cr; TCS ₹8,200 Cr) fully deducted from Enterprise Value as debt equivalents in DCF EV-to-Equity bridges."),
        ("Ind AS 24 Related Party Transactions", "Audited all promoter and subsidiary transactions; 100% verified as conducted at arm's-length with clean CARO disclosures."),
        ("Ind AS 37 Contingent Liabilities", "Audited tax and legal claims: 94% of ICICI's contingent liabilities are customer-hedged FX forward/derivative contracts; Reliance and TCS legal claims assessed at <1% of net worth."),
        ("Revenue Recognition & Auditor Opinions", "All 3 companies received Unmodified (Clean) Auditor Opinions from Big-4 auditors (BSR, Walker Chandiok, Deloitte) with zero qualification on Ind AS 115 revenue timing.")
    ]
    for a_name, a_desc in audit_badges:
        p_a = tf3_r.add_paragraph()
        p_a.space_before = Pt(8)
        r_an = p_a.add_run()
        r_an.text = f"✓ {a_name}\n"
        r_an.font.bold = True
        r_an.font.size = Pt(10)
        r_an.font.color.rgb = ACCENT_GREEN
        r_ad = p_a.add_run()
        r_ad.text = a_desc
        r_ad.font.size = Pt(9.5)
        r_ad.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s3,
        "Before projecting cash flows, we conducted a rigorous 5-year financial trajectory and forensic footnote audit across FY22 to FY26. All three firms exhibit superior cash conversion: Reliance converts 96% of EBITDA to operating cash flow, TCS converts 98% of PAT, and ICICI maintains a clean 0.45% Net NPA. On the forensic side, we adjusted for Ind AS 116 lease liabilities in all EV bridges and verified that 94% of ICICI's contingent liabilities are hedged FX swaps.",
        "Emphasize the deduction of Ind AS 116 lease liabilities from EV to prevent equity value overstatement.",
        "Q: Why deduct leases from EV if they are already accounted for in operating expenses? A: Under Ind AS 116, leases are capitalized as debt; failing to deduct them from EV would overstate intrinsic equity value."
    )

    # =========================================================================
    # SLIDE 4: Intrinsic Valuation Models (Sasi)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    create_header(
        s4, 4, "PART I: VALUATION & SENSITIVITY", "Sasi", "246213618", "50 Seconds",
        "Intrinsic Valuation Models: 2-Stage DDM, Consolidated DCF, SOTP & Reverse DCF",
        "Master Intrinsic Valuation Output Table & Model Rationales Tailored to Corporate Architecture"
    )

    # Table Card
    add_card(s4, Inches(0.6), Inches(1.35), Inches(12.133), Inches(2.5))
    tbl_shape4 = s4.shapes.add_table(4, 9, Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.2))
    tbl4 = tbl_shape4.table

    headers_tbl4 = ["Company", "Ticker", "Valuation Model", "Cost of Capital", "Intrinsic Target", "Market Price", "Margin / Upside", "5Y Implied IRR", "Recommendation"]
    col_widths4 = [Inches(1.5), Inches(1.1), Inches(1.8), Inches(1.1), Inches(1.2), Inches(1.1), Inches(1.2), Inches(1.1), Inches(1.4)]
    for i, w in enumerate(col_widths4):
        tbl4.columns[i].width = w

    for i, h in enumerate(headers_tbl4):
        c = tbl4.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = DARK_NAVY
        for p in c.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = TEXT_LIGHT

    rows_val_data = [
        ("ICICI Bank Ltd", "ICICIBANK.NS", "2-Stage DDM & Excess Return", "Ke = 12.65%", "₹1,595.50", "₹1,398.00", "+14.13%", "15.33%", "ACCUMULATE"),
        ("Reliance Industries", "RELIANCE.NS", "Consol. FCFF DCF & SOTP", "WACC = 12.10%", "₹1,420.14", "₹1,164.90", "+21.91%", "17.57%", "BUY"),
        ("Tata Consultancy Serv.", "TCS.NS", "2-Stage FCFF & Reverse DCF", "WACC = 11.65%", "₹2,905.55", "₹2,502.60", "+16.10%", "14.79%", "ACCUMULATE")
    ]
    for r_idx, row_vals in enumerate(rows_val_data, start=1):
        for c_idx, val in enumerate(row_vals):
            c = tbl4.cell(r_idx, c_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = CARD_ALT_BG if r_idx % 2 == 0 else CARD_BG
            for p in c.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER if c_idx >= 3 else PP_ALIGN.LEFT
                for r in p.runs:
                    r.font.size = Pt(9.5)
                    if c_idx == 6 and "+" in val:
                        r.font.bold = True
                        r.font.color.rgb = ACCENT_GREEN
                    elif c_idx == 8:
                        r.font.bold = True
                        r.font.color.rgb = ACCENT_GREEN if val == "BUY" else MID_BLUE

    # Bottom 3 Cards: Model Deep-Dives
    add_card(s4, Inches(0.6), Inches(4.05), Inches(3.8), Inches(3.0))
    tbox4_1 = s4.shapes.add_textbox(Inches(0.75), Inches(4.15), Inches(3.5), Inches(2.8))
    tf4_1 = tbox4_1.text_frame
    tf4_1.word_wrap = True
    p1 = tf4_1.paragraphs[0]
    p1.text = "ICICI Bank: DDM Rationale"
    p1.font.bold = True
    p1.font.size = Pt(11)
    p1.font.color.rgb = SLATE_NAVY
    icici_pts = [
        "Why DDM: Traditional FCFF is invalid for banks as deposits are operational inventory, not debt.",
        "Model Parameters: Stage 1 ROE = 17.20%, Ke = 12.65% (Beta 0.9663), Terminal g = 5.25%.",
        "Excess Equity Return: Captures economic value added over cost of equity.",
        "Verdict: Target ₹1,595.50 (+14.13% upside) supports steady ACCUMULATE."
    ]
    for pt in icici_pts:
        p_pt = tf4_1.add_paragraph()
        p_pt.space_before = Pt(3)
        p_pt.text = f"• {pt}"
        p_pt.font.size = Pt(8.5)
        p_pt.font.color.rgb = TEXT_MUTED

    add_card(s4, Inches(4.75), Inches(4.05), Inches(3.8), Inches(3.0))
    tbox4_2 = s4.shapes.add_textbox(Inches(4.9), Inches(4.15), Inches(3.5), Inches(2.8))
    tf4_2 = tbox4_2.text_frame
    tf4_2.word_wrap = True
    p2 = tf4_2.paragraphs[0]
    p2.text = "Reliance: DCF & SOTP Cross-Check"
    p2.font.bold = True
    p2.font.size = Pt(11)
    p2.font.color.rgb = SLATE_NAVY
    rel_pts = [
        "Consolidated DCF: WACC = 12.10%, Terminal g = 5.00% yields ₹1,420.14 (+21.91% upside).",
        "Segmental SOTP Cross-Check: ₹1,441.95/sh (+23.78% upside):",
        "  - O2C: 7.5x EV/EBITDA (₹3,73,500 Cr)",
        "  - Jio Telecom: 14.5x EV/EBITDA (₹8,26,500 Cr)",
        "  - Organized Retail: 24.0x EV/EBITDA (₹9,40,800 Cr)",
        "  - New Energy: 1.5x Invested Capital (₹1,05,000 Cr)",
        "Verdict: Deepest value dislocation -> High-Conviction BUY."
    ]
    for pt in rel_pts:
        p_pt = tf4_2.add_paragraph()
        p_pt.space_before = Pt(2)
        p_pt.text = f"• {pt}"
        p_pt.font.size = Pt(8.5)
        p_pt.font.color.rgb = TEXT_MUTED

    add_card(s4, Inches(8.9), Inches(4.05), Inches(3.8), Inches(3.0))
    tbox4_3 = s4.shapes.add_textbox(Inches(9.05), Inches(4.15), Inches(3.5), Inches(2.8))
    tf4_3 = tbox4_3.text_frame
    tf4_3.word_wrap = True
    p3 = tf4_3.paragraphs[0]
    p3.text = "TCS: DCF & Reverse DCF Proof"
    p3.font.bold = True
    p3.font.size = Pt(11)
    p3.font.color.rgb = SLATE_NAVY
    tcs_pts = [
        "2-Stage FCFF DCF: WACC = 11.65%, Beta = 0.8184, g = 4.50% yields ₹2,905.55 (+16.10% upside).",
        "Reverse DCF Implied Growth Proof: At CMP ₹2,502.60, market prices in only 5.13% 5Y revenue CAGR.",
        "TCV Backstop: $41B+ order book and GenAI pipeline support 8.50% CAGR (+337 bps unpriced growth).",
        "Verdict: Defensive tech compounder -> ACCUMULATE."
    ]
    for pt in tcs_pts:
        p_pt = tf4_3.add_paragraph()
        p_pt.space_before = Pt(3)
        p_pt.text = f"• {pt}"
        p_pt.font.size = Pt(8.5)
        p_pt.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s4,
        "Here we present our master valuation outputs, which we specifically tailored to each company's capital architecture. For ICICI Bank, standard FCFF is invalid because deposits are operational raw material; our 2-Stage DDM derives an intrinsic value of Rs 1,595.50 (+14.13% upside). For Reliance, our consolidated FCFF DCF target of Rs 1,420.14 (+21.91% upside) is cross-verified by our segmental SOTP at Rs 1,441.95. For TCS, our DCF target is Rs 2,905.55 (+16.10% upside); our Reverse DCF reveals that the market is pricing in an overly pessimistic 5.13% growth rate against an 8.50% reality.",
        "Highlight that Reliance has the largest margin of safety (+21.91%), making it our top BUY.",
        "Q: How did you calculate WACC for Reliance? A: 55.4% equity at Ke = 13.53% plus 44.6% debt at after-tax Kd = 5.54%, yielding WACC = 12.10%."
    )

    # =========================================================================
    # SLIDE 5: 5x5 Sensitivity Matrices & Peer Multiples (Sasi)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    create_header(
        s5, 5, "PART I: VALUATION & SENSITIVITY", "Sasi", "246213618", "45 Seconds",
        "5x5 Sensitivity Matrices & Relative Peer Valuation Multiples",
        "Discount Rate Stress Testing (±100 bps) & Relative Valuation Multiples Across Nifty Blue Chips"
    )

    # Left: Sensitivity Ranges
    add_card(s5, Inches(0.6), Inches(1.35), Inches(5.9), Inches(5.7))
    tbox5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.4))
    tf5 = tbox5.text_frame
    tf5.word_wrap = True

    p = tf5.paragraphs[0]
    p.text = "1. 5x5 Sensitivity Matrix Ranges (Ke/WACC vs. g)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    sens_cards = [
        ("ICICI Bank Ltd (Ke 11.65%–13.65% vs. g 4.25%–6.25%)", [
            "Intrinsic Value Range: ₹1,207.85 (Bear) to ₹2,275.58 (Bull)",
            "Base Case Target: ₹1,595.50 (+14.13% upside)",
            "Stress-Test Robustness: Even at Ke = 13.15% (+50 bps), intrinsic value of ₹1,424.30 preserves positive upside (+1.88%)."
        ]),
        ("Reliance Industries (WACC 11.10%–13.10% vs. g 4.00%–6.00%)", [
            "Intrinsic Value Range: ₹1,082.93 (Bear) to ₹2,015.42 (Bull)",
            "Base Case Target: ₹1,420.14 (+21.91% upside)",
            "Downside Buffer: Current market price (₹1,164.90) sits near the absolute pessimistic boundary (WACC 13.1%, g 4.0%), offering massive margin of safety."
        ]),
        ("TCS (WACC 10.65%–12.65% vs. g 3.50%–5.50%)", [
            "Intrinsic Value Range: ₹2,345.10 (Bear) to ₹3,896.80 (Bull)",
            "Base Case Target: ₹2,905.55 (+16.10% upside)",
            "Asymmetric Payoff: The bull case offers +55.7% upside, whereas the extreme bear case is only -6.3% below CMP."
        ])
    ]
    for s_name, s_pts in sens_cards:
        p_s = tf5.add_paragraph()
        p_s.space_before = Pt(8)
        r_sn = p_s.add_run()
        r_sn.text = s_name
        r_sn.font.bold = True
        r_sn.font.size = Pt(10)
        r_sn.font.color.rgb = TEXT_DARK
        for pt in s_pts:
            p_pt = tf5.add_paragraph()
            p_pt.space_before = Pt(2)
            r_pt = p_pt.add_run()
            r_pt.text = f"  • {pt}"
            r_pt.font.size = Pt(9.5)
            r_pt.font.color.rgb = TEXT_MUTED

    # Right: Relative Peer Multiples Table
    add_card(s5, Inches(6.8), Inches(1.35), Inches(5.9), Inches(5.7))
    tbox5_r = s5.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.5), Inches(5.4))
    tf5_r = tbox5_r.text_frame
    tf5_r.word_wrap = True

    p_r = tf5_r.paragraphs[0]
    p_r.text = "2. Indian Peer Relative Valuation Multiples"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = SLATE_NAVY

    peer_multiples_text = [
        ("Banking Comparables (P/B vs ROE):", [
            "ICICI Bank trades at 3.34x P/B with 17.50% ROE.",
            "HDFC Bank trades at 2.82x P/B with 15.20% ROE.",
            "Kotak Bank trades at 3.12x P/B with 14.10% ROE.",
            "Justification: ICICI commands a warranted quality premium due to industry-leading RoA (2.3%) and Net NPA of 0.45%."
        ]),
        ("Conglomerate & Retail Comparables (EV/EBITDA):", [
            "Reliance Consolidated trades at 9.38x EV/EBITDA.",
            "Bharti Airtel (Telecom Peer) trades at 14.80x EV/EBITDA.",
            "Avenue Supermarts (DMart Retail Peer) trades at 42.00x EV/EBITDA.",
            "Justification: Reliance's consolidated multiple severely discounts its market-leading consumer engines (Jio & Retail)."
        ]),
        ("IT Services Comparables (P/E Multiple):", [
            "TCS trades at 18.40x FY26 P/E with 51.0% ROE.",
            "Infosys trades at 22.10x FY26 P/E with 32.4% ROE.",
            "Wipro trades at 21.40x FY26 P/E with 15.8% ROE.",
            "Justification: TCS offers a superior quality-at-a-reasonable-price opportunity with 51% ROE and 98% cash conversion."
        ])
    ]
    for p_title, p_subpts in peer_multiples_text:
        p_pt = tf5_r.add_paragraph()
        p_pt.space_before = Pt(6)
        r_pt = p_pt.add_run()
        r_pt.text = p_title
        r_pt.font.bold = True
        r_pt.font.size = Pt(10)
        r_pt.font.color.rgb = TEXT_DARK
        for subpt in p_subpts:
            p_sub = tf5_r.add_paragraph()
            p_sub.space_before = Pt(1)
            r_sub = p_sub.add_run()
            r_sub.text = f"  • {subpt}"
            r_sub.font.size = Pt(9)
            r_sub.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s5,
        "To ensure model robustness, we stress-tested all three valuations across 5x5 sensitivity matrices covering plus or minus 100 basis points in cost of capital and terminal growth. Reliance is trading near its extreme bear-case valuation, providing downside protection, while TCS presents an asymmetric payoff where bull upside reaches +55.7%. On a relative basis, Reliance trades at 9.4x EV/EBITDA against retail peers at 42x, and TCS trades at 18.4x P/E despite a 51% ROE. I now hand over to Aditi for our AI and sentiment pipeline.",
        "Smooth transition to Aditi Routray for Part II.",
        "Q: Why does ICICI trade at a higher P/B than HDFC Bank? A: ICICI achieves a superior 17.5% ROE vs HDFC's 15.2% post-merger integration phase."
    )

    # =========================================================================
    # SLIDE 6: AI Pipeline Architecture & Deterministic Verifier (Aditi)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    create_header(
        s6, 6, "PART II: AI NLP PIPELINE & BENCHMARKS", "Aditi Routray", "246213548", "45 Seconds",
        "AI Pipeline Architecture & Deterministic 0%-Hallucination Quote Verifier",
        "Live HuggingFace ProsusAI/finbert Inference Paired with Programmatic difflib Verification"
    )

    # Left: Pipeline Flow Cards
    add_card(s6, Inches(0.6), Inches(1.35), Inches(5.9), Inches(5.7))
    tbox6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.4))
    tf6 = tbox6.text_frame
    tf6.word_wrap = True

    p = tf6.paragraphs[0]
    p.text = "1. AI Pipeline Modular Architecture"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    modules = [
        ("Sub-Module 1: Concall Corpus Ingestion", "24 quarterly earnings call transcripts (FY25–FY26) partitioned into scripted Management Remarks vs. unscripted Analyst Q&A."),
        ("Sub-Module 2: Live FinBERT Scoring", "PyTorch transformer inference using ProsusAI/finbert generating probability distributions across Positive, Negative, and Neutral."),
        ("Sub-Module 3: Deterministic Verifier", "Programmatic verification of annual report qualitative quotes using exact substring matching and difflib.SequenceMatcher."),
        ("Sub-Module 4: 90-Sentence Gold-Standard Benchmark", "Empirical validation against human ground truth evaluating Accuracy, Macro-F1, and Cohen's Kappa."),
        ("Sub-Module 5: 150-Headline Behavioral Framing", "Classification of news headlines into cognitive biases (FOMO, Recency, Loss Aversion) to diagnose market pricing dislocations.")
    ]
    for m_title, m_desc in modules:
        p_m = tf6.add_paragraph()
        p_m.space_before = Pt(6)
        r1 = p_m.add_run()
        r1.text = f"• {m_title}: "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_m.add_run()
        r2.text = m_desc
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    # Right: 0% Hallucination Verification Card
    add_card(s6, Inches(6.8), Inches(1.35), Inches(5.9), Inches(5.7))
    tbox6_r = s6.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.5), Inches(5.4))
    tf6_r = tbox6_r.text_frame
    tf6_r.word_wrap = True

    p_r = tf6_r.paragraphs[0]
    p_r.text = "2. Annual Report Verbatim Verification Results"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = SLATE_NAVY

    p_kpi = tf6_r.add_paragraph()
    p_kpi.space_before = Pt(10)
    r_kpi1 = p_kpi.add_run()
    r_kpi1.text = "12 / 12 Quotes Verified   |   1.0000 Similarity Ratio   |   0.00% Hallucination\n"
    r_kpi1.font.bold = True
    r_kpi1.font.size = Pt(10.5)
    r_kpi1.font.color.rgb = ACCENT_GREEN

    quotes_audit = [
        ("ICICI Bank Guidance", "Deposits: 'Targeting double-digit deposit growth with balanced retail CASA mobilization.' -> Status: VERIFIED (1.0000)"),
        ("ICICI Bank Asset Quality", "NPA: 'Net NPA remains low at 0.45% reflecting disciplined retail risk underwriting.' -> Status: VERIFIED (1.0000)"),
        ("Reliance Jio 5G Capex", "Capex: '5G network roll-out capex peaked in FY25; FY26 capex directed to retail & new energy.' -> Status: VERIFIED (1.0000)"),
        ("Reliance Retail Stores", "Rationalization: 'Rationalized non-performing retail footprint to optimize square-footage EBITDA.' -> Status: VERIFIED (1.0000)"),
        ("TCS GenAI Pipeline", "AI Deals: 'GenAI pipeline doubled to over USD 1.5B with strong cross-industry adoption.' -> Status: VERIFIED (1.0000)"),
        ("TCS Margin Guidance", "Operating Margin: 'Maintaining medium-term EBIT margin aspirational band of 26% to 28%.' -> Status: VERIFIED (1.0000)")
    ]
    for q_lbl, q_txt in quotes_audit:
        p_q = tf6_r.add_paragraph()
        p_q.space_before = Pt(5)
        r_ql = p_q.add_run()
        r_ql.text = f"✓ {q_lbl}: "
        r_ql.font.bold = True
        r_ql.font.size = Pt(9.5)
        r_ql.font.color.rgb = SLATE_NAVY
        r_qt = p_q.add_run()
        r_qt.text = q_txt
        r_qt.font.size = Pt(9)
        r_qt.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s6,
        "Thank you Sasi. To ensure institutional rigor and avoid the hallucination pitfalls of generative LLMs, our AI pipeline combines live PyTorch ProsusAI/finbert transformer inference with deterministic verbatim verification. In Sub-Module 3, we extracted 12 critical qualitative footnote quotes from FY26 Annual Reports across guidance, capex, and contingent liabilities; our program tested each quote against source text using exact substring matching and difflib, achieving a 1.0000 similarity score and a verified 0.00% hallucination rate.",
        "Emphasize the distinction between unconstrained generative LLMs (which hallucinate numbers) and domain-specific FinBERT + deterministic verifiers.",
        "Q: Why use FinBERT instead of GPT-4? A: FinBERT is specifically pre-trained on corporate filings and financial vocabulary, runs locally without latency or API drift, and provides exact class probabilities."
    )

    # =========================================================================
    # SLIDE 7: 8-Quarter Concall Sentiment & Optimism Gap (Aditi)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    create_header(
        s7, 7, "PART II: AI NLP PIPELINE & BENCHMARKS", "Aditi Routray", "246213548", "50 Seconds",
        "8-Quarter Concall Sentiment Trajectory & Management Optimism Gap",
        "Quantifying the Divergence between Scripted Opening Remarks and Unscripted Analyst Q&A"
    )

    # Left: Explanation & Metrics
    add_card(s7, Inches(0.6), Inches(1.35), Inches(5.5), Inches(5.7))
    tbox7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.1), Inches(5.4))
    tf7 = tbox7.text_frame
    tf7.word_wrap = True

    p = tf7.paragraphs[0]
    p.text = "1. The Management Optimism Gap (Δ)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    gap_bullets = [
        ("Formula:", " Optimism Gap Δ = Score(Remarks) - Score(Q&A), where Score = P(Positive) - P(Negative)."),
        ("ICICI Bank (Narrowest Gap = +1.09):", " Scripted Remarks averaged +0.8774 vs. Analyst Q&A of -0.2153. Caution density was 10.95 qualifiers per 100 words, focused on retail deposit competition and unsecured loan calibration."),
        ("Reliance Industries (Wide Gap = +1.48):", " Remarks averaged +0.8909 vs. Q&A of -0.5925. Caution density reached 11.82/100w, as analysts pressed management on O2C refining cracks and retail store closures."),
        ("TCS (Widest Gap = +1.54):", " Remarks averaged +0.7890 vs. Q&A of -0.7482. Caution density was 11.78/100w, dominated by analyst scrutiny over US BFSI tech spending delays and GenAI deal pricing concessions.")
    ]
    for b_title, b_desc in gap_bullets:
        p_b = tf7.add_paragraph()
        p_b.space_before = Pt(8)
        r1 = p_b.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_MUTED

    # Right: Sentiment Trends Image
    add_card(s7, Inches(6.4), Inches(1.35), Inches(6.333), Inches(5.7))
    img_sent = cleaned_dir / "sentiment_trends.png"
    if img_sent.exists():
        s7.shapes.add_picture(str(img_sent), Inches(6.6), Inches(1.5), width=Inches(5.9))

    set_speaker_notes(
        s7,
        "When we scored 24 earnings call transcripts across FY25 and FY26, we discovered a consistent structural phenomenon: the Management Optimism Gap. Management opening remarks consistently score between +0.79 and +0.89. However, during unscripted analyst Q&A, sentiment drops sharply into negative territory with 11 to 12 cautionary hedging words per 100 words. ICICI Bank displays the smallest gap at +1.09, reflecting stable execution, whereas TCS at +1.54 and Reliance at +1.48 faced aggressive analyst probing on tech spending delays and refining margin volatility.",
        "Walk the panel through the 3-panel sentiment trends graph, highlighting the shaded gap areas.",
        "Q: Why did Q&A score negative if all three companies are growing? A: Analysts ask risk-oriented questions, and management answers with prudent qualifiers ('calibrated', 'subject to repricing'), which FinBERT correctly flags as neutral-to-cautious."
    )

    # =========================================================================
    # SLIDE 8: 90-Sentence Human Gold-Standard FinBERT Benchmark (Aditi)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    create_header(
        s8, 8, "PART II: AI NLP PIPELINE & BENCHMARKS", "Aditi Routray", "246213548", "45 Seconds",
        "90-Sentence Human Gold-Standard FinBERT Validation Benchmark",
        "Rigorous Benchmark Evaluating Accuracy, Macro-F1, Cohen's Kappa & Failure Modes"
    )

    # Left: Confusion Matrix Table & Cards
    add_card(s8, Inches(0.6), Inches(1.35), Inches(5.9), Inches(5.7))
    tbox8 = s8.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.4))
    tf8 = tbox8.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    p.text = "1. 3x3 Confusion Matrix & Per-Class Accuracy"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    # Confusion matrix visual
    p_cm = tf8.add_paragraph()
    p_cm.space_before = Pt(8)
    p_cm.text = "Ground Truth vs. FinBERT Predictions (N = 90 Sentences):"
    p_cm.font.bold = True
    p_cm.font.size = Pt(10)

    cm_lines = [
        ("True Positive (30):", "Predicted Positive: 30 | Predicted Neutral: 0 | Predicted Negative: 0 (100% Rec)"),
        ("True Neutral (30):", "Predicted Positive: 0 | Predicted Neutral: 29 | Predicted Negative: 1 (96.7% Rec)"),
        ("True Negative (30):", "Predicted Positive: 3 | Predicted Neutral: 0 | Predicted Negative: 27 (90.0% Rec)")
    ]
    for cl, cd in cm_lines:
        p_cml = tf8.add_paragraph()
        p_cml.space_before = Pt(4)
        r1 = p_cml.add_run()
        r1.text = f"• {cl} "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_cml.add_run()
        r2.text = cd
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    p_per = tf8.add_paragraph()
    p_per.space_before = Pt(12)
    p_per.text = "Per-Company Benchmark Accuracy:"
    p_per.font.bold = True
    p_per.font.size = Pt(10)
    p_per.font.color.rgb = SLATE_NAVY

    co_acc = [
        ("ICICI Bank Ltd:", "28 / 30 Correct (93.33% Accuracy)"),
        ("Reliance Industries:", "29 / 30 Correct (96.67% Accuracy)"),
        ("Tata Consultancy Serv.:", "29 / 30 Correct (96.67% Accuracy)")
    ]
    for c_n, c_a in co_acc:
        p_ca = tf8.add_paragraph()
        p_ca.space_before = Pt(3)
        r_ca = p_ca.add_run()
        r_ca.text = f"  • {c_n} "
        r_ca.font.bold = True
        r_ca.font.size = Pt(9.5)
        r_va = p_ca.add_run()
        r_va.text = c_a
        r_va.font.size = Pt(9)
        r_va.font.color.rgb = ACCENT_GREEN

    # Right: Validation Metrics & Failure-Mode Analysis
    add_card(s8, Inches(6.8), Inches(1.35), Inches(5.9), Inches(5.7))
    tbox8_r = s8.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.5), Inches(5.4))
    tf8_r = tbox8_r.text_frame
    tf8_r.word_wrap = True

    p_r = tf8_r.paragraphs[0]
    p_r.text = "2. Statistical Validation & Failure-Mode Audit"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = SLATE_NAVY

    p_kpis = tf8_r.add_paragraph()
    p_kpis.space_before = Pt(8)
    p_kpis.text = "Overall Benchmark Performance Metrics:\n• Accuracy: 95.56% (86 / 90 Correct)\n• Macro-F1 Score: 0.9555\n• Cohen's Kappa: 0.9333 (Almost Perfect Agreement)"
    p_kpis.font.bold = True
    p_kpis.font.size = Pt(10)
    p_kpis.font.color.rgb = ACCENT_GREEN

    p_fa = tf8_r.add_paragraph()
    p_fa.space_before = Pt(12)
    p_fa.text = "Failure-Mode Analysis (The 4 Misclassifications):"
    p_fa.font.bold = True
    p_fa.font.size = Pt(10.5)
    p_fa.font.color.rgb = SLATE_NAVY

    failures = [
        ("Double-Barreled Corporate Phrasing (3 Misses):", " FinBERT predicted Positive for 3 human-labeled Negative sentences where management used a cautious qualifier alongside a strong financial number (e.g., 'calibrated unsecured lending expansion to preserve asset quality'). FinBERT overweighted 'expansion'."),
        ("Neutral Hedging Ambiguity (1 Miss):", " FinBERT predicted Negative for 1 Neutral sentence on capital allocation timing ('capex phasing remains contingent on spectrum utilization milestones')."),
        ("Remediation in Pipeline:", " This failure mode confirmed why raw sentiment scores must be combined with our Hedging Density Index and DCF fundamentals rather than traded blindly.")
    ]
    for f_t, f_d in failures:
        p_f = tf8_r.add_paragraph()
        p_f.space_before = Pt(6)
        r_ft = p_f.add_run()
        r_ft.text = f"• {f_t} "
        r_ft.font.bold = True
        r_ft.font.size = Pt(9.5)
        r_ft.font.color.rgb = TEXT_DARK
        r_fd = p_f.add_run()
        r_fd.text = f_d
        r_fd.font.size = Pt(9)
        r_fd.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s8,
        "Rather than trusting FinBERT as a black box, we benchmarked it against 90 human gold-standard sentences, balanced evenly with 30 positive, 30 neutral, and 30 negative sentences. FinBERT achieved an outstanding 95.56% accuracy, a Macro-F1 of 0.9555, and a Cohen's Kappa of 0.9333, demonstrating almost perfect agreement with human analysts. Crucially, our confusion matrix identified exactly 4 failure cases where management paired cautious qualifiers with growth metrics, causing FinBERT to overweight the positive noun.",
        "Highlight Cohen's Kappa of 0.9333 proving high statistical reliability.",
        "Q: What is Cohen's Kappa and why does it matter? A: It measures inter-annotator agreement adjusted for the possibility of agreement occurring by chance; anything above 0.81 is considered 'Almost Perfect Agreement'."
    )

    # =========================================================================
    # SLIDE 9: 150-Headline Behavioral Bias Framing vs Dislocation (Aditi)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    create_header(
        s9, 9, "PART II: AI NLP PIPELINE & BENCHMARKS", "Aditi Routray", "246213548", "45 Seconds",
        "150-Headline Behavioral Bias Framing vs. Valuation Dislocation",
        "Diagnosing How Media Narrative Biases Create Fundamental Price-to-Value Disconnects"
    )

    # 3 Cards for the 3 Companies
    add_card(s9, Inches(0.6), Inches(1.35), Inches(3.8), Inches(5.7))
    tbox9_1 = s9.shapes.add_textbox(Inches(0.75), Inches(1.5), Inches(3.5), Inches(5.4))
    tf9_1 = tbox9_1.text_frame
    tf9_1.word_wrap = True

    p = tf9_1.paragraphs[0]
    p.text = "ICICI Bank: Hype & FOMO"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = SLATE_NAVY

    icici_bias_pts = [
        ("Dominant Bias:", " 58% Hype / FOMO Chasing"),
        ("Media Sentiment:", " Highly Positive (+0.2217)"),
        ("Narrative Framing:", " Media heralds ICICI as India's 'unstoppable banking champion' with consensus hiking EPS by +4.8%."),
        ("Fundamental Reality:", " ICICI is compounding exceptionally well, but valuation upside is +14.13% (Target ₹1,595.50 vs CMP ₹1,398.00)."),
        ("Strategic Stance:", " Warranted quality compounder, but warrants disciplined ACCUMULATE on dips, not chasing FOMO spikes.")
    ]
    for b_l, b_t in icici_bias_pts:
        p_pt = tf9_1.add_paragraph()
        p_pt.space_before = Pt(6)
        r1 = p_pt.add_run()
        r1.text = b_l
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_pt.add_run()
        r2.text = b_t
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    add_card(s9, Inches(4.75), Inches(1.35), Inches(3.8), Inches(5.7))
    tbox9_2 = s9.shapes.add_textbox(Inches(4.9), Inches(1.5), Inches(3.5), Inches(5.4))
    tf9_2 = tbox9_2.text_frame
    tf9_2.word_wrap = True

    p = tf9_2.paragraphs[0]
    p.text = "Reliance: Recency Bias"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = SLATE_NAVY

    rel_bias_pts = [
        ("Dominant Bias:", " 34% Recency Extrapolation"),
        ("Media Sentiment:", " Negative (-0.2879)"),
        ("Narrative Framing:", " Market extrapolates two quarters of weak refining margins (GRMs) and retail store footprint closures (-1.4% EPS trim)."),
        ("Fundamental Reality:", " 5G capex has peaked; telecom tariff hikes and retail operating leverage are driving free cash flow surge (+21.91% upside to ₹1,420.14)."),
        ("Strategic Stance:", " Classic contrarian dislocation -> High-Conviction BUY.")
    ]
    for b_l, b_t in rel_bias_pts:
        p_pt = tf9_2.add_paragraph()
        p_pt.space_before = Pt(6)
        r1 = p_pt.add_run()
        r1.text = b_l
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_pt.add_run()
        r2.text = b_t
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    add_card(s9, Inches(8.9), Inches(1.35), Inches(3.8), Inches(5.7))
    tbox9_3 = s9.shapes.add_textbox(Inches(9.05), Inches(1.5), Inches(3.5), Inches(5.4))
    tf9_3 = tbox9_3.text_frame
    tf9_3.word_wrap = True

    p = tf9_3.paragraphs[0]
    p.text = "TCS: Loss Aversion / AI Panic"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = SLATE_NAVY

    tcs_bias_pts = [
        ("Dominant Bias:", " 50% Loss Aversion / Disruption Fear"),
        ("Media Sentiment:", " Highly Negative (-0.3438)"),
        ("Narrative Framing:", " Headlines fixate on existential GenAI billing-headcount destruction and US discretionary spending cuts (-2.1% EPS trim)."),
        ("Fundamental Reality:", " Market-implied growth collapsed to 5.13%, yet order book ($41B+) supports 8.50% CAGR (+16.10% upside to ₹2,905.55)."),
        ("Strategic Stance:", " Unwarranted disruption pessimism -> ACCUMULATE.")
    ]
    for b_l, b_t in tcs_bias_pts:
        p_pt = tf9_3.add_paragraph()
        p_pt.space_before = Pt(6)
        r1 = p_pt.add_run()
        r1.text = b_l
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_pt.add_run()
        r2.text = b_t
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s9,
        "By classifying 150 financial news headlines into behavioral biases, we uncovered why our intrinsic valuations diverge so sharply from current market prices. In Reliance, the market suffers from 34% Recency Bias, extrapolating two quarters of weak refining margins while ignoring the post-5G free cash flow inflections—creating our largest margin of safety at +21.91%. In TCS, the market suffers from 50% Loss Aversion over GenAI staffing fears, pushing implied growth down to 5.13% vs. an 8.50% DCF reality. In ICICI Bank, 58% Hype confirms it is a core compounder, but one to accumulate on disciplined pullbacks.",
        "Contrast the emotional narrative with the underlying discounted cash flows.",
        "Q: How did you classify the headlines into biases? A: Using a dual keyword and semantic embedding classifier categorizing headlines into Hype/FOMO, Recency Extrapolation, Loss Aversion, and Anchoring."
    )

    # =========================================================================
    # SLIDE 10: Technical Momentum & 1,000-Path GBM Monte Carlo (Aditi)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    create_header(
        s10, 10, "PART II: AI NLP PIPELINE & BENCHMARKS", "Aditi Routray", "246213548", "45 Seconds",
        "Technical Momentum Indicators & 1,000-Path GBM Monte Carlo Fan Charts",
        "Reconciling Backward-Looking Stochastic Price Drift with Forward Fundamental Valuation"
    )

    # Left: Technical Table & Analysis
    add_card(s10, Inches(0.6), Inches(1.35), Inches(5.5), Inches(5.7))
    tbox10 = s10.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.1), Inches(5.4))
    tf10 = tbox10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "1. Technical Indicators & Monte Carlo Metrics"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    tech_data = [
        ("ICICI Bank (CMP ₹1,398.00):", [
            "Technical Regime: Strong Uptrend (Price > 50-DMA ₹1,378 > 200-DMA ₹1,347)",
            "Momentum: RSI = 56.97 (Bullish Neutral); MACD Hist = +3.76",
            "1Y GBM Monte Carlo: Median (P50) = ₹1,553.35 (+11.11%), closely converging with our DDM target of ₹1,595.50."
        ]),
        ("Reliance Industries (CMP ₹1,164.90):", [
            "Technical Regime: Consolidation (Price below 50-DMA ₹1,236 and 200-DMA ₹1,326)",
            "Momentum: RSI = 40.27 (Oversold); Bullish MACD Crossover Hist = +0.36",
            "1Y GBM Monte Carlo: Backward median is ₹1,125.15, but our forward DCF target (₹1,420.14) sits at P82 (P75 ₹1,318, P90 ₹1,513), setting up a mean-reverting catalyst."
        ]),
        ("TCS (CMP ₹2,502.60):", [
            "Technical Regime: Rebound Phase (Price above 50-DMA ₹2,255 and 200-DMA ₹2,394)",
            "Momentum: RSI = 67.56; Strong Bullish MACD Hist = +16.22",
            "1Y GBM Monte Carlo: Forward DCF target (₹2,905.55) sits between P75 (₹2,774) and P90 (₹3,134)."
        ])
    ]
    for t_n, t_pts in tech_data:
        p_t = tf10.add_paragraph()
        p_t.space_before = Pt(6)
        r_tn = p_t.add_run()
        r_tn.text = t_n
        r_tn.font.bold = True
        r_tn.font.size = Pt(10)
        r_tn.font.color.rgb = TEXT_DARK
        for pt in t_pts:
            p_pt = tf10.add_paragraph()
            p_pt.space_before = Pt(2)
            r_pt = p_pt.add_run()
            r_pt.text = f"  • {pt}"
            r_pt.font.size = Pt(9)
            r_pt.font.color.rgb = TEXT_MUTED

    # Right: Monte Carlo Fan Charts
    add_card(s10, Inches(6.4), Inches(1.35), Inches(6.333), Inches(5.7))
    img_mc = cleaned_dir / "mc_fan_charts.png"
    if img_mc.exists():
        s10.shapes.add_picture(str(img_mc), Inches(6.6), Inches(1.5), width=Inches(5.9))

    set_speaker_notes(
        s10,
        "Our technical indicators and 1,000-path Geometric Brownian Motion Monte Carlo simulations reveal why backward price extrapolation fails during cyclical turning points. While ICICI Bank exhibits a steady uptrend where the Monte Carlo median of Rs 1,553 converges with our DDM target, Reliance shows oversold RSI levels and an early positive MACD crossover, setting the stage for convergence toward our Rs 1,420 DCF target. I now hand over to our Project Lead, Sankarshana, to present portfolio construction.",
        "Smooth transition to Sankarshana Mulugundam for Part III.",
        "Q: Why did you use GBM instead of jump diffusion? A: For core blue chips with deep liquidity, GBM provides a robust baseline, and our 1,000 paths adequately capture log-normal terminal dispersion."
    )

    # =========================================================================
    # SLIDE 11: Blended Expected Returns & MVO Tangency Portfolio (Sankarshana)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    create_header(
        s11, 11, "PART III: PORTFOLIO OPTIMIZATION", "Sankarshana Mulugundam", "246213080", "50 Seconds",
        "Blended Expected Returns, MVO Tangency Portfolio & Efficient Frontier",
        "Overcoming Historical Drift via 50% CAPM Ke + 50% DCF IRR Blended Return Vector"
    )

    # Left: Blended Returns & Tangency Weights
    add_card(s11, Inches(0.6), Inches(1.35), Inches(5.5), Inches(5.7))
    tbox11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.1), Inches(5.4))
    tf11 = tbox11.text_frame
    tf11.word_wrap = True

    p = tf11.paragraphs[0]
    p.text = "1. Forward Blended Returns & Tangency Portfolio"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    ret_bullets = [
        ("The Historical Drift Trap:", " 5-year historical returns (Reliance +0.27%, TCS -3.77%) reflect past cyclical derating. Extrapolating them would cause optimizer collapse."),
        ("Blended Expected Return Formula:", " E(Ri) = 0.50 * CAPM Ke + 0.50 * DCF/DDM 5Y Implied IRR:"),
        ("  • ICICI Bank:", " 0.5(12.65%) + 0.5(15.33%) = 13.99% (Vol = 19.55%, Beta = 0.9663)"),
        ("  • Reliance Industries:", " 0.5(13.53%) + 0.5(17.57%) = 15.55% (Vol = 22.33%, Beta = 1.1125)"),
        ("  • TCS:", " 0.5(11.76%) + 0.5(14.79%) = 13.28% (Vol = 22.85%, Beta = 0.8184)"),
        ("  • 91D RBI T-Bill:", " Risk-Free Rate = 6.65% (Vol = 0.00%, Beta = 0.0000)"),
        ("Max-Sharpe Tangency Portfolio Weights:", " ICICI Bank = 38.90% | Reliance = 37.91% | TCS = 23.19%"),
        ("Portfolio Efficiency:", " E(Rp) = 14.42%, Vol = 15.74% (diversification eliminates 400–700 bps of standalone volatility!), Sharpe = 0.4935.")
    ]
    for b_title, b_desc in ret_bullets:
        p_b = tf11.add_paragraph()
        p_b.space_before = Pt(5)
        r1 = p_b.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    # Right: Efficient Frontier & CAL Chart
    add_card(s11, Inches(6.4), Inches(1.35), Inches(6.333), Inches(5.7))
    img_ef = cleaned_dir / "efficient_frontier_cal.png"
    if img_ef.exists():
        s11.shapes.add_picture(str(img_ef), Inches(6.6), Inches(1.5), width=Inches(5.9))

    set_speaker_notes(
        s11,
        "Thank you Aditi. Standard Markowitz optimization collapses when fed backward-looking 5-year returns, because past cyclical multiple compression in Reliance and TCS would suggest zero allocation. To solve this, we blended 50% CAPM equilibrium returns with 50% DCF 5-year implied IRRs. Our Max-Sharpe Tangency portfolio allocates 38.90% to ICICI Bank, 37.91% to Reliance, and 23.19% to TCS, delivering an expected return of 14.42% at a volatility of only 15.74%—slashing standalone risk by up to 700 basis points and yielding a Sharpe ratio of 0.4935.",
        "Highlight the Capital Allocation Line originating at Rf = 6.65% (91D T-Bill) and tangent to the equity frontier.",
        "Q: Why blend CAPM and DCF 50/50? A: It balances equilibrium market pricing with fundamental cash flow reality, eliminating single-model forecast bias."
    )

    # =========================================================================
    # SLIDE 12: Utility Allocation & Featured Case A=4.00 (Sankarshana)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    create_header(
        s12, 12, "PART III: PORTFOLIO OPTIMIZATION", "Sankarshana Mulugundam", "246213080", "50 Seconds",
        "Utility Allocation, Prudence Override & Featured Case Study (A = 4.00)",
        "Two-Fund Separation along CAL & Capital Allocations for ₹10 Lakh Lump Sum & ₹25k SIP"
    )

    # Left: Profiler & Prudence Architecture
    add_card(s12, Inches(0.6), Inches(1.35), Inches(5.5), Inches(5.7))
    tbox12 = s12.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.1), Inches(5.4))
    tf12 = tbox12.text_frame
    tf12.word_wrap = True

    p = tf12.paragraphs[0]
    p.text = "1. Risk Profiler & The Prudence Override Rule"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    profiler_pts = [
        ("Two-Dimensional Assessment:", " 10-question framework measuring Financial Ability (Sec A: 5–20) and Psychological Willingness (Sec B: 5–20). Total Score R in [10, 40]."),
        ("The Prudence Override Rule:", " If |Sec A - Sec B| >= 6, we override: Reff = 2 * min(Sec A, Sec B). Prevents emotionally aggressive investors with fragile balance sheets from taking destructive drawdowns."),
        ("Linear Risk Aversion Mapping:", " Risk aversion A = 10 - 0.3 * (Reff - 10). Maps continuously from A = 1.00 (R = 40) down to A = 10.00 (R = 10)."),
        ("Tobin's Separation Formula:", " Risky equity share y* = min(1.0, (E(Rtan) - Rf) / (A * sigma_tan^2)). T-Bill share = 1 - y*.")
    ]
    for b_l, b_d in profiler_pts:
        p_pt = tf12.add_paragraph()
        p_pt.space_before = Pt(6)
        r1 = p_pt.add_run()
        r1.text = b_l
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p_pt.add_run()
        r2.text = b_d
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    p_baskets = tf12.add_paragraph()
    p_baskets.space_before = Pt(8)
    p_baskets.text = "Canonical Investor Baskets:"
    p_baskets.font.bold = True
    p_baskets.font.size = Pt(10)
    p_baskets.font.color.rgb = SLATE_NAVY

    baskets_desc = [
        ("Aggressive (A=2.20, R=36):", " 100% Equity | E(Rc)=14.42%, Vol=15.74%"),
        ("Balanced (A=4.90, R=27):", " 64.0% Equity / 36.0% T-Bill | E(Rc)=11.62%, Vol=10.07%"),
        ("Defensive (A=8.50, R=15):", " 36.9% Equity / 63.1% T-Bill | E(Rc)=9.52%, Vol=5.81%"),
        ("Prudence Override Case:", " Sec A=9, Sec B=18 -> Capped at 41.27% Equity!")
    ]
    for b_n, b_v in baskets_desc:
        p_b = tf12.add_paragraph()
        p_b.space_before = Pt(2)
        r_bn = p_b.add_run()
        r_bn.text = f"• {b_n}"
        r_bn.font.bold = True
        r_bn.font.size = Pt(9)
        r_bv = p_b.add_run()
        r_bv.text = b_v
        r_bv.font.size = Pt(8.5)
        r_bv.font.color.rgb = TEXT_MUTED

    # Right: Featured Case Study A=4.00 Card
    add_card(s12, Inches(6.4), Inches(1.35), Inches(6.333), Inches(5.7), bg_color=CARD_BG, border_color=ACCENT_GREEN)
    tbox12_r = s12.shapes.add_textbox(Inches(6.6), Inches(1.5), Inches(5.9), Inches(5.4))
    tf12_r = tbox12_r.text_frame
    tf12_r.word_wrap = True

    p_r = tf12_r.paragraphs[0]
    p_r.text = "2. Featured Case Study: A = 4.00 (Moderate-Growth)"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = SLATE_NAVY

    p_f_kpis = tf12_r.add_paragraph()
    p_f_kpis.space_before = Pt(4)
    p_f_kpis.text = "Profile: Sec A = 15, Sec B = 15, Reff = 30 -> Risk Aversion A = 4.00\nOptimal Risky Share y* = 78.41%   |   91D T-Bill Share 1-y* = 21.59%\nE(Rc) = 12.74%   |   Vol = 12.34%   |   Beta = 0.7742   |   Sharpe = 0.4935"
    p_f_kpis.font.bold = True
    p_f_kpis.font.size = Pt(9.5)
    p_f_kpis.font.color.rgb = ACCENT_GREEN

    # Rupee Table for A=4.00
    p_tbl = tf12_r.add_paragraph()
    p_tbl.space_before = Pt(8)
    p_tbl.text = "4-Asset Capital Splits (₹10 Lakh Lump Sum & ₹25k Monthly SIP):"
    p_tbl.font.bold = True
    p_tbl.font.size = Pt(10)
    p_tbl.font.color.rgb = SLATE_NAVY

    splits_data = [
        ("ICICI Bank Ltd", "30.50%", "₹3,05,000", "₹7,625 / mo", "Core compounding private banking engine"),
        ("Reliance Industries", "29.72%", "₹2,97,200", "₹7,430 / mo", "Deep value conglomerate & consumer cash flow"),
        ("Tata Consultancy Serv.", "18.18%", "₹1,81,800", "₹4,545 / mo", "Defensive USD cash cow & tech hedge"),
        ("91-Day RBI T-Bill", "21.59%", "₹2,15,900", "₹5,398 / mo", "Risk-free sovereign drawdown buffer"),
        ("Total Complete Portfolio", "100.00%", "₹10,00,000", "₹25,000 / mo", "Optimal Quadratic Utility U = 0.0970")
    ]
    for a_name, a_wt, a_lump, a_sip, a_note in splits_data:
        p_row = tf12_r.add_paragraph()
        p_row.space_before = Pt(4)
        r_an = p_row.add_run()
        r_an.text = f"• {a_name} ({a_wt}): "
        r_an.font.bold = True
        r_an.font.size = Pt(9.5)
        r_an.font.color.rgb = TEXT_DARK if a_name != "Total Complete Portfolio" else SLATE_NAVY
        r_dt = p_row.add_run()
        r_dt.text = f"{a_lump} | SIP: {a_sip}\n   Role: {a_note}"
        r_dt.font.size = Pt(8.5)
        r_dt.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s12,
        "By Tobin's Separation Theorem, all rational investors hold the identical Tangency equity basket, scaling their exposure y-star along the Capital Allocation Line based on their risk aversion A. Our 10-question profiler scores both financial ability and psychological willingness; our Prudence Override rule safeguards against balance sheet fragility. In our featured moderate-growth case study at A = 4.00, the optimal allocation is 78.41% equity and 21.59% T-Bills. For a 10 Lakh Rupee portfolio, this translates directly to Rs 3.05 Lakh in ICICI, Rs 2.97 Lakh in Reliance, Rs 1.82 Lakh in TCS, and Rs 2.16 Lakh in liquid T-Bills.",
        "Highlight the exact rupee allocations for both lump sum and SIP.",
        "Q: Why does the Prudence Rule trigger at a difference of 6? A: A 6-point gap represents an entire risk quadrant difference (e.g. low ability but high risk tolerance), which historically causes panic-selling during market corrections."
    )

    # =========================================================================
    # SLIDE 13: 20-Year Step-Up SIP Lifecycle Glide Path (Sankarshana)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    create_header(
        s13, 13, "PART III: PORTFOLIO OPTIMIZATION", "Sankarshana Mulugundam", "246213080", "45 Seconds",
        "20-Year Step-Up SIP Lifecycle Glide Path (₹25,000/mo, +10% Annual Step-Up)",
        "Dynamic 3-Phase Lifecycle Rebalancing from Early-Career Accumulation to Capital Preservation"
    )

    # Left: Explanation & Milestones
    add_card(s13, Inches(0.6), Inches(1.35), Inches(5.5), Inches(5.7))
    tbox13 = s13.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.1), Inches(5.4))
    tf13 = tbox13.text_frame
    tf13.word_wrap = True

    p = tf13.paragraphs[0]
    p.text = "1. 3-Phase Lifecycle Architecture (Age 25–44)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    sip_phases = [
        ("Phase 1: Accumulation (Years 1–8, Age 25–32):", " 100% Equity / 0% T-Bill (Aggressive Basket, A = 2.20). Maximum compounding power during early career when human capital is highest."),
        ("Phase 2: Consolidation (Years 9–15, Age 33–39):", " 64.0% Equity / 36.0% T-Bill (Balanced Basket, A = 4.90). Introducing sovereign T-Bills to cushion mid-career drawdowns."),
        ("Phase 3: Preservation (Years 16–20, Age 40–44):", " 36.9% Equity / 63.1% T-Bill (Defensive Basket, A = 8.50). Shifts majority into risk-free sovereign paper to eliminate sequence-of-returns risk near retirement."),
        ("Terminal Wealth Accumulation:", [
            "Cumulative Capital Invested: ₹1.7182 Crore (₹1,71,82,500)",
            "Deterministic Expected Corpus: ₹4.3241 Crore (2.52x Wealth Multiple)",
            "1,000-Path Monte Carlo P10 (Bear): ₹3.1765 Crore",
            "1,000-Path Monte Carlo P50 (Median): ₹4.1962 Crore",
            "1,000-Path Monte Carlo P90 (Bull): ₹5.7370 Crore"
        ])
    ]
    for item in sip_phases:
        if isinstance(item[1], str):
            p_sp = tf13.add_paragraph()
            p_sp.space_before = Pt(6)
            r1 = p_sp.add_run()
            r1.text = item[0]
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = TEXT_DARK
            r2 = p_sp.add_run()
            r2.text = item[1]
            r2.font.size = Pt(9)
            r2.font.color.rgb = TEXT_MUTED
        else:
            p_w = tf13.add_paragraph()
            p_w.space_before = Pt(8)
            p_w.text = item[0]
            p_w.font.bold = True
            p_w.font.size = Pt(10)
            p_w.font.color.rgb = SLATE_NAVY
            for sub_w in item[1]:
                p_sw = tf13.add_paragraph()
                p_sw.space_before = Pt(2)
                r_sw = p_sw.add_run()
                r_sw.text = f"  • {sub_w}"
                r_sw.font.size = Pt(8.5)
                r_sw.font.color.rgb = ACCENT_GREEN if "Corpus" in sub_w or "Median" in sub_w else TEXT_MUTED

    # Right: Glide Path Chart
    add_card(s13, Inches(6.4), Inches(1.35), Inches(6.333), Inches(5.7))
    img_sip = cleaned_dir / "sip_glide_path.png"
    if img_sip.exists():
        s13.shapes.add_picture(str(img_sip), Inches(6.6), Inches(1.5), width=Inches(5.9))

    set_speaker_notes(
        s13,
        "We operationalized our allocation model into a 20-year Step-Up SIP lifecycle glide path starting at Rs 25,000 per month with a disciplined 10% annual step-up. The portfolio automatically glides through three distinct phases: 100% equity during early accumulation, shifting to 64% equity in mid-career, and locking in 63.1% in risk-free sovereign T-Bills during the final five years. Over 20 years, an investor deposits Rs 1.72 Crore, compounding to an expected deterministic corpus of Rs 4.32 Crore—with our 1,000-path Monte Carlo confirming a 90% probability of exceeding Rs 3.18 Crore.",
        "Highlight the automatic de-risking into T-Bills in Phase 3 to eliminate sequence-of-returns risk.",
        "Q: Why use a 10% annual step-up? A: It matches typical Indian white-collar corporate salary growth, accelerating wealth accumulation in later years."
    )

    # =========================================================================
    # SLIDE 14: Mandatory 4-Metric Evaluation & 5Y Backtest (Sankarshana)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    create_header(
        s14, 14, "PART III: PORTFOLIO OPTIMIZATION", "Sankarshana Mulugundam", "246213080", "45 Seconds",
        "Mandatory 4-Metric Portfolio Evaluation & 5-Year Historical Backtest",
        "Evaluation Across Sharpe, Treynor, Jensen's Alpha & Information Ratio vs. Nifty 50 Benchmark"
    )

    # Table Card
    add_card(s14, Inches(0.6), Inches(1.35), Inches(6.1), Inches(5.7))
    tbl_shape14 = s14.shapes.add_table(7, 6, Inches(0.8), Inches(1.5), Inches(5.7), Inches(3.2))
    tbl14 = tbl_shape14.table

    headers_tbl14 = ["Portfolio", "Beta", "Sharpe", "Treynor", "Alpha (%)", "Info Ratio"]
    col_w14 = [Inches(1.7), Inches(0.7), Inches(0.8), Inches(0.8), Inches(0.9), Inches(0.8)]
    for i, w in enumerate(col_w14):
        tbl14.columns[i].width = w

    for i, h in enumerate(headers_tbl14):
        c = tbl14.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = DARK_NAVY
        for p in c.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(8.5)
                r.font.color.rgb = TEXT_LIGHT

    rows_eval_data = [
        ("Tangency (A=2.20)", "0.9874", "0.4935", "0.0786", "+1.84%", "+0.2274"),
        ("Featured Case (A=4.00)", "0.7742", "0.4935", "0.0786", "+1.45%", "+0.0144"),
        ("Balanced (A=4.90)", "0.6320", "0.4935", "0.0786", "+1.18%", "+0.1171"),
        ("Defensive (A=8.50)", "0.3643", "0.4940", "0.0786", "+0.68%", "+0.0058"),
        ("Equal-Weight (1/3)", "0.9657", "0.4875", "0.0789", "+1.83%", "+0.2312"),
        ("Nifty 50 Benchmark", "1.0000", "0.4328", "0.0600", "0.00%", "0.0000")
    ]
    for r_idx, r_vals in enumerate(rows_eval_data, start=1):
        for c_idx, val in enumerate(r_vals):
            c = tbl14.cell(r_idx, c_idx)
            c.text = val
            c.fill.solid()
            if "Featured" in r_vals[0]:
                c.fill.fore_color.rgb = RGBColor(220, 252, 231)  # Soft emerald highlight
            else:
                c.fill.fore_color.rgb = CARD_ALT_BG if r_idx % 2 == 0 else CARD_BG
            for p in c.text_frame.paragraphs:
                p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
                for r in p.runs:
                    r.font.size = Pt(8.5)
                    if "Featured" in r_vals[0]:
                        r.font.bold = True

    # Takeaways below table
    tbox14_sub = s14.shapes.add_textbox(Inches(0.8), Inches(4.85), Inches(5.7), Inches(2.1))
    tf14_s = tbox14_sub.text_frame
    tf14_s.word_wrap = True
    p_sub = tf14_s.paragraphs[0]
    p_sub.text = "Mathematical Invariance along the CAL:"
    p_sub.font.bold = True
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = SLATE_NAVY
    invar_pts = [
        "Sharpe Invariance: By Two-Fund Separation, Tangency, Featured, Balanced, and Defensive portfolios all share the identical Sharpe (~0.4935) and Treynor (0.0786) because CAL excess return and volatility scale linearly.",
        "Alpha Superiority: All optimized baskets generate positive Jensen's Alpha (+0.68% to +1.84%) over the Nifty 50 benchmark.",
        "Information Ratio: Captures active return per unit of tracking error (6.84% to 7.76% TE)."
    ]
    for pt in invar_pts:
        p_pt = tf14_s.add_paragraph()
        p_pt.space_before = Pt(2)
        p_pt.text = f"• {pt}"
        p_pt.font.size = Pt(8)
        p_pt.font.color.rgb = TEXT_MUTED

    # Right: 5Y Historical Backtest Chart
    add_card(s14, Inches(6.9), Inches(1.35), Inches(5.833), Inches(5.7))
    img_bt = cleaned_dir / "backtest_performance.png"
    if img_bt.exists():
        s14.shapes.add_picture(str(img_bt), Inches(7.1), Inches(1.5), width=Inches(5.4))

    set_speaker_notes(
        s14,
        "Evaluating our portfolios across the four mandatory course ratios—Sharpe, Treynor, Jensen's Alpha, and Information Ratio—proves the quantitative superiority of our framework over the Nifty 50 benchmark. Notice a profound mathematical result: by Tobin's Separation Theorem, the Sharpe ratio of 0.4935 and Treynor measure of 0.0786 are identical across our Tangency, Featured A = 4.00, Balanced, and Defensive portfolios because both excess return and volatility scale linearly with equity weight y-star. Meanwhile, every basket generates positive Jensen's Alpha, led by +1.84% in the Tangency portfolio.",
        "Explain why Sharpe is constant along the CAL (separation theorem) but Information Ratio changes.",
        "Q: Why does the Information Ratio vary if Sharpe is invariant? A: Information ratio benchmarks against the Nifty 50 (a 100% equity index), whereas Sharpe benchmarks against the risk-free rate."
    )

    # =========================================================================
    # SLIDE 15: Final Synthesis, Actionable Verdict & Dashboard Demo (Sankarshana)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    create_header(
        s15, 15, "SYNTHESIS & CONCLUSION", "Sankarshana Mulugundam", "246213080", "45 Seconds",
        "Final Investment Synthesis, Actionable Verdict & Live Dashboard Demo",
        "Triangulated Asset Allocation Verdicts, Methodological Limitations & Interactive Streamlit App"
    )

    # Left: Triangulated Recommendations
    add_card(s15, Inches(0.6), Inches(1.35), Inches(5.9), Inches(5.7))
    tbox15 = s15.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.4))
    tf15 = tbox15.text_frame
    tf15.word_wrap = True

    p = tf15.paragraphs[0]
    p.text = "1. Final Triangulated Investment Verdicts"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    verdicts = [
        ("Reliance Industries (BUY — 37.91% Tangency / 29.72% in A=4.00):", [
            "DCF Upside: +21.91% (Target ₹1,420.14 vs CMP ₹1,164.90); SOTP cross-check @ ₹1,441.95.",
            "Catalyst: Post-5G capex moderation driving free cash flow surge; contrarian buy against 34% media recency bias.",
            "Role: Highest expected return asset (15.55%) in the portfolio."
        ]),
        ("ICICI Bank Ltd (ACCUMULATE — 38.90% Tangency / 30.50% in A=4.00):", [
            "DDM Upside: +14.13% (Target ₹1,595.50 vs CMP ₹1,398.00).",
            "Catalyst: Best-in-class ROE (17.5%), lowest concall optimism gap (+1.09), pristine 0.45% Net NPA.",
            "Role: Core compounding foundation and largest equity weight."
        ]),
        ("Tata Consultancy Services (ACCUMULATE — 23.19% Tangency / 18.18% in A=4.00):", [
            "DCF Upside: +16.10% (Target ₹2,905.55 vs CMP ₹2,502.60).",
            "Catalyst: Reverse DCF proves market over-discounts AI panic (prices 5.13% vs 8.50% reality).",
            "Role: Essential USD revenue hedge and lowest correlation asset (0.26 with ICICI)."
        ]),
        ("91-Day RBI T-Bill (Core Sovereign Anchor — 21.59% in A=4.00):", [
            "Role: Guaranteed 6.65% sovereign yield eliminating drawdown and sequence risk."
        ])
    ]
    for v_title, v_pts in verdicts:
        p_v = tf15.add_paragraph()
        p_v.space_before = Pt(5)
        r_vt = p_v.add_run()
        r_vt.text = v_title
        r_vt.font.bold = True
        r_vt.font.size = Pt(9.5)
        r_vt.font.color.rgb = ACCENT_GREEN if "BUY" in v_title else (SLATE_NAVY if "ACCUMULATE" in v_title else TEXT_DARK)
        for pt in v_pts:
            p_pt = tf15.add_paragraph()
            p_pt.space_before = Pt(1)
            r_pt = p_pt.add_run()
            r_pt.text = f"  • {pt}"
            r_pt.font.size = Pt(8.5)
            r_pt.font.color.rgb = TEXT_MUTED

    # Right: Dashboard Demo & Limitations
    add_card(s15, Inches(6.8), Inches(1.35), Inches(5.9), Inches(5.7))
    tbox15_r = s15.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.5), Inches(5.4))
    tf15_r = tbox15_r.text_frame
    tf15_r.word_wrap = True

    p_r = tf15_r.paragraphs[0]
    p_r.text = "2. Offline Streamlit Dashboard & Research Limitations"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = SLATE_NAVY

    p_dash = tf15_r.add_paragraph()
    p_dash.space_before = Pt(8)
    p_dash.text = "Interactive 9-Block Streamlit App (05_dashboard/app.py):"
    p_dash.font.bold = True
    p_dash.font.size = Pt(10.5)
    p_dash.font.color.rgb = SLATE_NAVY

    dash_features = [
        "100% Offline-Cached: Zero external API latency or LLM hallucinations.",
        "Interactive Sliders: Live risk aversion A slider, lump sum / SIP rupee adjusters.",
        "Dynamic Plots: Interactive Plotly sensitivity matrices, fan charts, and glide paths.",
        "Execution Command: py -m streamlit run 05_dashboard/app.py"
    ]
    for feat in dash_features:
        p_f = tf15_r.add_paragraph()
        p_f.space_before = Pt(2)
        r_f = p_f.add_run()
        r_f.text = f"  ✓ {feat}"
        r_f.font.size = Pt(9)
        r_f.font.color.rgb = TEXT_MUTED

    p_lim = tf15_r.add_paragraph()
    p_lim.space_before = Pt(10)
    p_lim.text = "Research Limitations & Future Scope:"
    p_lim.font.bold = True
    p_lim.font.size = Pt(10.5)
    p_lim.font.color.rgb = SLATE_NAVY

    lims = [
        ("FinBERT Ambiguity:", " Double-barreled concall sentences require multi-agent LLM consensus for deeper nuance."),
        ("GBM Assumptions:", " Constant drift and volatility in GBM fail to model fat tails and regime switches (future jump-diffusion extension)."),
        ("Static Covariance:", " 5-year sample covariance assumes stationary correlation structures; dynamic DCC-GARCH would enhance real-time rebalancing.")
    ]
    for l_t, l_d in lims:
        p_l = tf15_r.add_paragraph()
        p_l.space_before = Pt(3)
        r_lt = p_l.add_run()
        r_lt.text = f"• {l_t} "
        r_lt.font.bold = True
        r_lt.font.size = Pt(9)
        r_lt.font.color.rgb = TEXT_DARK
        r_ld = p_l.add_run()
        r_ld.text = l_d
        r_ld.font.size = Pt(8.5)
        r_ld.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s15,
        "In conclusion, our study demonstrates that combining fundamental intrinsic valuation with AI-augmented FinBERT sentiment analysis enables institutional investors to look beyond consensus media noise and capitalize on genuine market dislocations. Reliance Industries is our top contrarian BUY with a +21.91% upside; ICICI Bank is our steady private credit compounder at +14.13%; and TCS provides a resilient USD cash cow yielding +16.10% upside. All 9 modules are fully interactive in our offline Streamlit dashboard. Thank you, and we now welcome your questions.",
        "Final strong closing statement and transition to panel Q&A.",
        "Offer to open the Streamlit dashboard for any live scenario testing requested by the faculty."
    )

    # =========================================================================
    # SLIDE 16 (APPENDIX): Viva Voce Defense Cheat Sheet
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    create_header(
        s16, 16, "APPENDIX: FACULTY VIVA DEFENSE", "All Team Members", "Team Roster", "Reference",
        "Appendix: Faculty Viva Voce Defense Guide (6 Toughest Questions)",
        "Rigorous Quantitative Responses to Critical Methodological & Theoretical Inquiries"
    )

    add_card(s16, Inches(0.6), Inches(1.35), Inches(12.133), Inches(5.7))
    tbox16 = s16.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    tf16 = tbox16.text_frame
    tf16.word_wrap = True

    p = tf16.paragraphs[0]
    p.text = "Anticipated Faculty Questions & Defense Cheat Sheet"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE_NAVY

    qna_list = [
        ("Q1 (Sasi - Valuation): Why 2-Stage DDM for ICICI Bank instead of FCFF DCF?", "In commercial banks, customer deposits (₹18.02L Cr) and borrowings are operational inventory, not financing capital. Working capital (ΔNWC) and pre-interest WACC cannot be separated from operating flows. Valuing equity directly via 2-Stage DDM and Excess Equity Return ((ROE - Ke) * BVPS) discounted at CAPM Ke (12.65%) is the only theoretically sound framework."),
        ("Q2 (Sasi - Valuation): TCS 5Y historical return is negative (-3.77%). How justify +16.10% intrinsic upside?", "TCS suffered multiple contraction from ~32x P/E to 18.4x FY26 P/E due to post-COVID tech derating, even as revenue grew to ₹2.58L Cr and PAT hit ₹49,200 Cr with 51% ROE. Our Reverse DCF proves current CMP implies an overly pessimistic 5.13% 5Y CAGR, whereas its $41B+ TCV order book supports 8.50% CAGR (+337 bps unpriced growth)."),
        ("Q3 (Aditi - AI Pipeline): How do you guarantee the AI didn't hallucinate annual report figures?", "All valuation math is in deterministic Python, not LLM prompts. For qualitative notes, we built a verbatim string verifier (difflib.SequenceMatcher) matching extracted quotes against raw source filings. All 12/12 quotes achieved a 1.0000 similarity ratio (0.00% hallucination rate)."),
        ("Q4 (Aditi - AI Benchmark): In your 90-sentence benchmark, what caused FinBERT's 4 misclassifications?", "The 4 misses were double-barreled corporate sentences where management acknowledged risk with soft qualifiers ('calibrated growth', 'repricing headwind') alongside positive metrics. FinBERT overweighted the growth noun. This is why we created our explicit Hedging Density Index (~11-12/100w in Q&A)."),
        ("Q5 (Sankarshana - Portfolio): Why two different risk-free rates (6.85% vs. 6.65%)?", "Duration matching: in DCF/DDM, we discount perpetual corporate cash flows spanning decades, requiring the 10-Year India G-Sec yield (6.85%). In portfolio optimization, the risk-free complete asset (1-y*) must be a zero-duration money-market asset free of mark-to-market risk, matching the 91-Day RBI T-Bill (6.65%)."),
        ("Q6 (Sankarshana - Portfolio): Why are Sharpe and Treynor invariant across utility baskets?", "By Tobin's Two-Fund Separation Theorem, all complete portfolios along the Capital Allocation Line are linear combinations of the Tangency basket and the risk-free T-Bill. Because excess return E(Rc)-Rf = y*(E(Rtan)-Rf) and volatility sigma_c = y*sigma_tan both scale linearly with y*, their ratio (Sharpe = 0.4935, Treynor = 0.0786) is mathematically invariant.")
    ]
    for q_t, q_a in qna_list:
        p_q = tf16.add_paragraph()
        p_q.space_before = Pt(4)
        r_q = p_q.add_run()
        r_q.text = f"• {q_t}\n"
        r_q.font.bold = True
        r_q.font.size = Pt(9.5)
        r_q.font.color.rgb = SLATE_NAVY
        r_a = p_q.add_run()
        r_a.text = f"   Defense: {q_a}"
        r_a.font.size = Pt(8.5)
        r_a.font.color.rgb = TEXT_MUTED

    set_speaker_notes(
        s16,
        "This appendix slide contains our prepared defense for the six most probable theoretical and quantitative questions the faculty may ask during the viva session.",
        "Keep these answers crisp, direct, and grounded in academic corporate finance theory.",
        "Reference specific slides and tables when answering each question."
    )

    pptx_path = root_dir / "06_deliverables" / "Presentation_Deck_15_Slides.pptx"
    prs.save(str(pptx_path))
    shutil.copy2(pptx_path, root_dir / "06_deliverables" / "SA_final_presentation.pptx")
    print(f"Successfully generated {pptx_path}")
    print(f"Copied to SA_final_presentation.pptx")


def build_interactive_html(root_dir: Path):
    html_path = root_dir / "06_deliverables" / "Presentation_Deck_15_Slides.html"
    deliverable_copy = root_dir / "06_deliverables" / "SA_final_presentation.html"

    # HTML code with responsive slide carousel, dark investment banking aesthetic, notes toggle, and embedded image modal
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Deck: Beyond the Consensus</title>
    <style>
        :root {
            --bg-dark: #0a192f;
            --bg-card: #112240;
            --bg-card-alt: #1e293b;
            --accent-blue: #38bdf8;
            --accent-green: #10b981;
            --accent-gold: #f59e0b;
            --text-light: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; }
        body { background: var(--bg-dark); color: var(--text-light); height: 100vh; overflow: hidden; display: flex; flex-direction: column; }
        header { background: #071120; border-bottom: 1px solid var(--border); padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; }
        .logo-area { display: flex; align-items: center; gap: 14px; }
        .project-pill { background: rgba(56, 189, 248, 0.15); color: var(--accent-blue); padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; border: 1px solid rgba(56, 189, 248, 0.3); }
        .project-title { font-size: 15px; font-weight: bold; color: var(--text-light); }
        .controls { display: flex; align-items: center; gap: 12px; }
        .btn { background: #1e293b; color: var(--text-light); border: 1px solid var(--border); padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500; transition: all 0.2s; }
        .btn:hover { background: #334155; border-color: var(--accent-blue); }
        .btn-primary { background: var(--accent-blue); color: #0a192f; font-weight: bold; border: none; }
        .btn-primary:hover { background: #7dd3fc; }
        
        main { flex: 1; position: relative; overflow: hidden; display: flex; }
        .slide-container { flex: 1; padding: 24px 36px; overflow-y: auto; display: none; }
        .slide-container.active { display: block; }
        
        .slide-header { margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 12px; }
        .slide-meta { display: flex; gap: 10px; font-size: 12px; margin-bottom: 6px; font-weight: bold; }
        .badge-num { color: var(--accent-gold); }
        .badge-sec { color: var(--accent-blue); }
        .badge-spk { color: #a7f3d0; }
        .slide-title { font-size: 24px; font-weight: 700; color: #ffffff; margin-bottom: 4px; }
        .slide-subtitle { font-size: 14px; color: var(--text-muted); font-style: italic; }
        
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 16px; }
        .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 16px; }
        .card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2); }
        .card h3 { font-size: 16px; color: var(--accent-blue); margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 6px; }
        .card p, .card li { font-size: 13.5px; line-height: 1.6; color: #cbd5e1; margin-bottom: 8px; }
        .card ul { padding-left: 18px; }
        .card strong { color: #ffffff; }
        .highlight-val { color: var(--accent-green); font-weight: bold; }
        
        .img-card { text-align: center; background: #071120; border: 1px solid var(--border); border-radius: 10px; padding: 12px; overflow: hidden; }
        .img-card img { max-width: 100%; max-height: 440px; border-radius: 6px; cursor: pointer; transition: transform 0.2s; }
        .img-card img:hover { transform: scale(1.02); }
        
        table.data-tbl { width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 12.5px; }
        table.data-tbl th { background: #0f172a; color: var(--accent-blue); padding: 8px 10px; text-align: left; border: 1px solid var(--border); }
        table.data-tbl td { padding: 7px 10px; border: 1px solid var(--border); color: #cbd5e1; }
        table.data-tbl tr:nth-child(even) { background: rgba(255,255,255,0.02); }
        table.data-tbl tr.highlight { background: rgba(16, 185, 129, 0.15); font-weight: bold; }
        
        /* Speaker Notes Drawer */
        .notes-panel { position: fixed; bottom: 0; left: 0; right: 0; background: #030712; border-top: 2px solid var(--accent-gold); padding: 16px 32px; font-size: 13.5px; transform: translateY(100%); transition: transform 0.3s ease; z-index: 50; max-height: 35vh; overflow-y: auto; }
        .notes-panel.open { transform: translateY(0); }
        .notes-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .notes-title { color: var(--accent-gold); font-weight: bold; font-size: 14px; }
        .notes-content { color: #f1f5f9; line-height: 1.6; white-space: pre-line; }

        footer { background: #071120; border-top: 1px solid var(--border); padding: 8px 24px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: var(--text-muted); }
        .progress-bar { width: 220px; height: 6px; background: #1e293b; border-radius: 3px; overflow: hidden; }
        .progress-fill { height: 100%; background: var(--accent-blue); width: 6.66%; transition: width 0.3s ease; }
    </style>
</head>
<body>
    <header>
        <div class="logo-area">
            <span class="project-pill">FINAL ACADEMIC PRESENTATION</span>
            <span class="project-title">Beyond the Consensus: An AI-Augmented Fundamental Valuation</span>
        </div>
        <div class="controls">
            <button class="btn" onclick="prevSlide()">← Prev (Left)</button>
            <span id="slide-indicator" style="font-size: 13px; font-weight: bold; color: var(--accent-blue);">Slide 1 / 16</span>
            <button class="btn" onclick="nextSlide()">Next (Right) →</button>
            <button class="btn btn-primary" onclick="toggleNotes()">Toggle Notes (N)</button>
        </div>
    </header>

    <main id="main-content">
        <!-- Slides will be rendered here dynamically via JS from slideData array -->
    </main>

    <div class="notes-panel" id="notes-panel">
        <div class="notes-header">
            <span class="notes-title">SPEAKER SCRIPT & DEFENSE NOTES</span>
            <button class="btn" onclick="toggleNotes()">Close</button>
        </div>
        <div class="notes-content" id="notes-text">Loading speaker notes...</div>
    </div>

    <footer>
        <div>Roster: Sasi (Valuation) | Aditi Routray (FinBERT) | Sankarshana Mulugundam (Portfolio Lead)</div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <span>Pacing: 10–12 Mins (~45s/slide)</span>
            <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
        </div>
    </footer>

    <script>
        const slideData = [
            {
                num: 1,
                sec: "EXECUTIVE OVERVIEW & SETUP",
                spk: "Sasi (246213618) | 45s",
                title: "Beyond the Consensus: An AI-Augmented Fundamental Valuation",
                sub: "Triangulated Academic Defense across Three Macro Engines: ICICI Bank, Reliance Industries & TCS",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. The Investment Problem & Academic Hypothesis</h3>
                            <ul>
                                <li><strong>The Market Pricing Disconnect:</strong> Short-term market prices are systematically distorted by media narrative biases—FOMO hype in private credit, extrapolating temporary refining cracks in conglomerates, and existential AI panic in IT.</li>
                                <li><strong>Triangulated Architecture:</strong> We combine Multi-Model Intrinsic Valuation (2-Stage DDM, Consolidated DCF, Segmental SOTP, Reverse DCF), Live HuggingFace FinBERT NLP across 24 quarters of concalls, and Utility-Optimal Portfolio Optimization.</li>
                                <li><strong>Three Orthogonal Engines:</strong> Private Financial Intermediation (ICICI Bank), Capex & Consumer Compounder (Reliance), and Dollar-Denominated IP/Tech Consulting (TCS).</li>
                            </ul>
                        </div>
                        <div class="card">
                            <h3>2. Single Source of Truth Constants (config.json)</h3>
                            <table class="data-tbl">
                                <tr><th>Parameter</th><th>Locked Value</th><th>Methodological Role</th></tr>
                                <tr><td>Cutoff Price Date</td><td>2026-10-30</td><td>5-Year Daily Sample (1,236 Days)</td></tr>
                                <tr><td>10Y G-Sec Yield (Rf)</td><td>6.85%</td><td>Duration-Matched DCF/DDM Discounting</td></tr>
                                <tr><td>91D T-Bill Yield (Rf)</td><td>6.65%</td><td>Money-Market Complete Portfolio Anchor</td></tr>
                                <tr><td>India Equity Risk Premium</td><td>6.00%</td><td>Sovereign-Adjusted India ERP</td></tr>
                                <tr><td>Corporate Tax Rate</td><td>25.17%</td><td>Statutory Base Corporate Rate</td></tr>
                            </table>
                            <p style="margin-top: 12px; font-size: 12px; color: var(--text-muted);">Team Allocation: Sasi (Slides 1–5), Aditi Routray (Slides 6–10), Sankarshana Mulugundam (Slides 11–15).</p>
                        </div>
                    </div>
                `,
                notes: `Good morning Professor and panel. We present 'Beyond the Consensus'—an institutional framework combining multi-model fundamental valuation, live FinBERT natural language processing, and utility-based portfolio optimization across three flagship Indian blue chips: ICICI Bank, Reliance Industries, and TCS. I am Sasi, handling Part I on fundamental valuation and forensic accounting; Aditi will present Part II on our AI pipeline; and Sankarshana will present Part III on portfolio construction.`
            },
            {
                num: 2,
                sec: "PART I: UNIVERSE SELECTION & AUDIT",
                spk: "Sasi (246213618) | 45s",
                title: "Three-Pillar Coverage Universe, Rejection Matrix & Correlation Proof",
                sub: "Empirical Diversification across 1,235 Daily Log Returns vs. Intra-Sector Clustered Peers",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. Coverage Rationale & 7 Rejected Alternatives</h3>
                            <ul>
                                <li><strong>Core #1 ICICI Bank:</strong> Best-in-class ROE (~17.5%), clean asset quality (Net NPA 0.45%), ideal for 2-Stage DDM.</li>
                                <li><strong>Core #2 Reliance Industries:</strong> Transitioning from O2C cash cow to high-growth consumer/digital platforms (Jio + Retail); DCF cross-checked via SOTP.</li>
                                <li><strong>Core #3 TCS:</strong> Stellar 51% ROE, negative working capital, low beta (0.82), defensive USD hedge; tested via Reverse DCF.</li>
                                <li><strong>Core #4 91D RBI T-Bill (6.65%):</strong> Zero-default sovereign money-market instrument for two-fund separation along the Capital Allocation Line.</li>
                                <li><strong>7 Explicit Rejections:</strong> ITC (tobacco tax overhang), HUL (52x P/E with 3-4% volume growth), Cummins (diesel genset terminal risk), Coal India (post-FY35 reserve decay), Abbott India (NLEM price cuts), INDHOTEL (>55x cyclical peak), and BSE Ltd (excessive retail options regulatory beta >2.2x).</li>
                            </ul>
                        </div>
                        <div class="img-card">
                            <img src="../01_data/cleaned/correlation_heatmap.png" alt="10-Stock Correlation Heatmap">
                            <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 6px;">Mean pairwise correlation among core triad: 0.3427 (ICICI-TCS: 0.2564, Reliance-TCS: 0.3401)</p>
                        </div>
                    </div>
                `,
                notes: `Rather than picking three stocks from a single sector, we selected three orthogonal pillars of the Indian economy: private credit, consumer conglomerate capex, and global USD enterprise technology. Our 10-stock correlation matrix across 1,235 daily returns proves our core triad has an average correlation of just 0.34 (ICICI-TCS is 0.26, Reliance-TCS is 0.34), far superior to intra-sector pairs like TCS and Infosys at 0.73.`
            },
            {
                num: 3,
                sec: "PART I: UNIVERSE SELECTION & AUDIT",
                spk: "Sasi (246213618) | 45s",
                title: "5-Year Financial Trajectory & Forensic Footnote Audit (FY22–FY26)",
                sub: "Auditing Cash Conversion, Operating Leverage & Ind AS 116 / 24 / 37 Footnote Adjustments",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. 5-Year Trajectory & Operational Quality</h3>
                            <ul>
                                <li><strong>ICICI Bank:</strong> NII compounded at 18.1% CAGR to ₹92,400 Cr; PAT reached ₹49,540 Cr with 17.50% ROE and pristine 0.45% Net NPA.</li>
                                <li><strong>Reliance Industries:</strong> Consolidated Revenue hit ₹10.15 Lakh Cr; EBITDA reached ₹1.82 Lakh Cr with 95.9% CFO/EBITDA cash conversion.</li>
                                <li><strong>TCS:</strong> Revenue ₹2.58 Lakh Cr; EBIT ₹63,200 Cr (24.50% margin) with exceptional 51.0% ROE and 98.2% CFO/PAT conversion.</li>
                            </ul>
                        </div>
                        <div class="card">
                            <h3>2. Forensic Footnote & CARO Checklist</h3>
                            <ul>
                                <li><strong style="color: var(--accent-green);">✓ Ind AS 116 Leases:</strong> Capitalized lease liabilities (Reliance ₹24,600 Cr; TCS ₹8,200 Cr) fully deducted from EV as debt equivalents in DCF bridges.</li>
                                <li><strong style="color: var(--accent-green);">✓ Ind AS 24 RPTs:</strong> Verified all promoter and subsidiary transactions as conducted at arm's-length.</li>
                                <li><strong style="color: var(--accent-green);">✓ Ind AS 37 Contingent Liabilities:</strong> 94% of ICICI's contingent liabilities are customer-hedged FX forward/derivative contracts; legal claims in Reliance and TCS are <1% of net worth.</li>
                                <li><strong style="color: var(--accent-green);">✓ Auditor Opinions:</strong> Unmodified clean opinions across all 3 firms.</li>
                            </ul>
                        </div>
                    </div>
                `,
                notes: `Before projecting cash flows, we conducted a rigorous 5-year financial trajectory and forensic footnote audit across FY22 to FY26. All three firms exhibit superior cash conversion: Reliance converts 96% of EBITDA to operating cash flow, TCS converts 98% of PAT, and ICICI maintains a clean 0.45% Net NPA. On the forensic side, we adjusted for Ind AS 116 lease liabilities in all EV bridges and verified that 94% of ICICI's contingent liabilities are hedged FX swaps.`
            },
            {
                num: 4,
                sec: "PART I: VALUATION & SENSITIVITY",
                spk: "Sasi (246213618) | 50s",
                title: "Intrinsic Valuation Models: 2-Stage DDM, Consolidated DCF, SOTP & Reverse DCF",
                sub: "Master Intrinsic Valuation Output Table & Model Rationales Tailored to Corporate Architecture",
                html: `
                    <div class="card" style="margin-bottom: 16px;">
                        <table class="data-tbl">
                            <tr><th>Company</th><th>Model Used</th><th>Cost of Capital</th><th>Intrinsic Target</th><th>Market Price</th><th>Margin / Upside</th><th>5Y IRR</th><th>Verdict</th></tr>
                            <tr><td><strong>ICICI Bank</strong></td><td>2-Stage DDM & Excess Return</td><td>Ke = 12.65%</td><td>₹1,595.50</td><td>₹1,398.00</td><td class="highlight-val">+14.13%</td><td>15.33%</td><td><span style="color: #38bdf8; font-weight: bold;">ACCUMULATE</span></td></tr>
                            <tr class="highlight"><td><strong>Reliance Industries</strong></td><td>Consol. FCFF DCF & SOTP</td><td>WACC = 12.10%</td><td>₹1,420.14</td><td>₹1,164.90</td><td class="highlight-val">+21.91%</td><td>17.57%</td><td><span style="color: #10b981; font-weight: bold;">BUY</span></td></tr>
                            <tr><td><strong>TCS</strong></td><td>2-Stage FCFF & Reverse DCF</td><td>WACC = 11.65%</td><td>₹2,905.55</td><td>₹2,502.60</td><td class="highlight-val">+16.10%</td><td>14.79%</td><td><span style="color: #38bdf8; font-weight: bold;">ACCUMULATE</span></td></tr>
                        </table>
                    </div>
                    <div class="grid-3">
                        <div class="card">
                            <h3>ICICI Bank: DDM Rationale</h3>
                            <p>FCFF is invalid for banks as deposits are operational inventory. 2-Stage DDM using Ke = 12.65%, Stage 1 ROE = 17.20%, and terminal g = 5.25% yields ₹1,595.50 (+14.13% upside).</p>
                        </div>
                        <div class="card">
                            <h3>Reliance: DCF & SOTP Cross-Check</h3>
                            <p>Consolidated DCF target of ₹1,420.14 (+21.91% upside) is cross-verified by Segmental SOTP at ₹1,441.95 (O2C 7.5x, Jio 14.5x, Retail 24x). Deepest value dislocation -> BUY.</p>
                        </div>
                        <div class="card">
                            <h3>TCS: DCF & Reverse DCF Proof</h3>
                            <p>DCF yields ₹2,905.55 (+16.10% upside). Reverse DCF proves market prices in only 5.13% 5Y CAGR, whereas $41B+ TCV order book supports 8.50% CAGR (+337 bps unpriced growth).</p>
                        </div>
                    </div>
                `,
                notes: `Here we present our master valuation outputs, which we specifically tailored to each company's capital architecture. For ICICI Bank, standard FCFF is invalid because deposits are operational raw material; our 2-Stage DDM derives an intrinsic value of Rs 1,595.50 (+14.13% upside). For Reliance, our consolidated FCFF DCF target of Rs 1,420.14 (+21.91% upside) is cross-verified by our segmental SOTP at Rs 1,441.95. For TCS, our DCF target is Rs 2,905.55 (+16.10% upside); our Reverse DCF reveals that the market is pricing in an overly pessimistic 5.13% growth rate against an 8.50% reality.`
            },
            {
                num: 5,
                sec: "PART I: VALUATION & SENSITIVITY",
                spk: "Sasi (246213618) | 45s",
                title: "5x5 Sensitivity Matrices & Relative Peer Valuation Multiples",
                sub: "Discount Rate Stress Testing (±100 bps) & Relative Valuation Multiples Across Nifty Blue Chips",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. 5x5 Sensitivity Matrix Ranges</h3>
                            <ul>
                                <li><strong>ICICI Bank (Ke 11.65%–13.65% vs g 4.25%–6.25%):</strong> Ranges from ₹1,207.85 to ₹2,275.58. Base case is ₹1,595.50. At +50 bps Ke stress (13.15%), target of ₹1,424.30 preserves positive margin of safety.</li>
                                <li><strong>Reliance (WACC 11.10%–13.10% vs g 4.00%–6.00%):</strong> Ranges from ₹1,082.93 to ₹2,015.42. Current market price (₹1,164.90) sits near the absolute pessimistic boundary (WACC 13.1%, g 4.0%), offering massive downside cushion.</li>
                                <li><strong>TCS (WACC 10.65%–12.65% vs g 3.50%–5.50%):</strong> Ranges from ₹2,345.10 to ₹3,896.80. Base case is ₹2,905.55; bull case offers +55.7% upside vs -6.3% downside in worst-case bear.</li>
                            </ul>
                        </div>
                        <div class="card">
                            <h3>2. Relative Peer Valuation Comparables</h3>
                            <ul>
                                <li><strong>ICICI Bank vs Peers:</strong> Trades at 3.34x P/B with 17.50% ROE. Justified quality premium over HDFC Bank (2.82x P/B, 15.2% ROE) due to superior 2.3% RoA and pristine 0.45% Net NPA.</li>
                                <li><strong>Reliance vs Peers:</strong> Consolidated 9.38x EV/EBITDA is a steep discount to telecom peer Bharti Airtel (14.8x) and retail peer DMart (42.0x).</li>
                                <li><strong>TCS vs Peers:</strong> Trades at 18.40x FY26 P/E with 51.0% ROE vs Infosys (22.1x) and Wipro (21.4x), offering superior quality-at-a-reasonable-price.</li>
                            </ul>
                        </div>
                    </div>
                `,
                notes: `To ensure model robustness, we stress-tested all three valuations across 5x5 sensitivity matrices covering plus or minus 100 basis points in cost of capital and terminal growth. Reliance is trading near its extreme bear-case valuation, providing downside protection, while TCS presents an asymmetric payoff where bull upside reaches +55.7%. On a relative basis, Reliance trades at 9.4x EV/EBITDA against retail peers at 42x, and TCS trades at 18.4x P/E despite a 51% ROE. I now hand over to Aditi for our AI and sentiment pipeline.`
            },
            {
                num: 6,
                sec: "PART II: AI NLP PIPELINE & BENCHMARKS",
                spk: "Aditi Routray (246213548) | 45s",
                title: "AI Pipeline Architecture & Deterministic 0%-Hallucination Quote Verifier",
                sub: "Live HuggingFace ProsusAI/finbert Inference Paired with Programmatic difflib Verification",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. AI Pipeline Modular Architecture</h3>
                            <ul>
                                <li><strong>Sub-Module 1 (Corpus Ingestion):</strong> 24 quarterly earnings call transcripts partitioned into scripted Remarks vs unscripted Q&A.</li>
                                <li><strong>Sub-Module 2 (Live FinBERT Inference):</strong> Local PyTorch inference using ProsusAI/finbert generating probability distributions.</li>
                                <li><strong>Sub-Module 3 (Deterministic Verifier):</strong> Programmatic string verifier ensuring 0% hallucination on annual report qualitative quotes.</li>
                                <li><strong>Sub-Module 4 (90-Sentence Gold-Standard):</strong> Human validation benchmark for accuracy, Macro-F1, and Cohen's Kappa.</li>
                                <li><strong>Sub-Module 5 (150-Headline Framing):</strong> Diagnostic framing into cognitive biases (FOMO, Recency, Loss Aversion).</li>
                            </ul>
                        </div>
                        <div class="card">
                            <h3>2. Annual Report Verbatim Verification (0% Hallucination)</h3>
                            <p style="color: var(--accent-green); font-weight: bold; font-size: 14px; margin-bottom: 10px;">12 / 12 Quotes Verified | 1.0000 Similarity Ratio | 0.00% Hallucination</p>
                            <ul>
                                <li><strong>ICICI Deposit Guidance:</strong> "Targeting double-digit deposit growth with balanced retail CASA mobilization." (VERIFIED)</li>
                                <li><strong>Reliance 5G Capex:</strong> "5G network roll-out capex peaked in FY25; FY26 capex directed to retail & new energy." (VERIFIED)</li>
                                <li><strong>TCS GenAI Pipeline:</strong> "GenAI pipeline doubled to over USD 1.5B with strong cross-industry adoption." (VERIFIED)</li>
                            </ul>
                        </div>
                    </div>
                `,
                notes: `Thank you Sasi. To ensure institutional rigor and avoid the hallucination pitfalls of generative LLMs, our AI pipeline combines live PyTorch ProsusAI/finbert transformer inference with deterministic verbatim verification. In Sub-Module 3, we extracted 12 critical qualitative footnote quotes from FY26 Annual Reports across guidance, capex, and contingent liabilities; our program tested each quote against source text using exact substring matching and difflib, achieving a 1.0000 similarity score and a verified 0.00% hallucination rate.`
            },
            {
                num: 7,
                sec: "PART II: AI NLP PIPELINE & BENCHMARKS",
                spk: "Aditi Routray (246213548) | 50s",
                title: "8-Quarter Concall Sentiment Trajectory & Management Optimism Gap",
                sub: "Quantifying the Divergence between Scripted Opening Remarks and Unscripted Analyst Q&A",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. The Management Optimism Gap (Δ)</h3>
                            <ul>
                                <li><strong>Formula:</strong> Optimism Gap Δ = Score(Remarks) - Score(Q&A), where Score = P(Positive) - P(Negative).</li>
                                <li><strong>ICICI Bank (Narrowest Gap = +1.09):</strong> Remarks +0.8774 vs Q&A -0.2153. Caution density: 10.95/100w (focused on deposit competition and retail loan calibration).</li>
                                <li><strong>Reliance Industries (Wide Gap = +1.48):</strong> Remarks +0.8909 vs Q&A -0.5925. Caution density: 11.82/100w (analysts pressing on O2C crack volatility and retail store closures).</li>
                                <li><strong>TCS (Widest Gap = +1.54):</strong> Remarks +0.7890 vs Q&A -0.7482. Caution density: 11.78/100w (dominated by US BFSI tech spending delays and GenAI deal pricing concessions).</li>
                            </ul>
                        </div>
                        <div class="img-card">
                            <img src="../01_data/cleaned/sentiment_trends.png" alt="Sentiment Trends & Optimism Gap">
                            <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 6px;">8-Quarter Sentiment Trajectory across 24 Calls (Q1 FY25 to Q4 FY26)</p>
                        </div>
                    </div>
                `,
                notes: `When we scored 24 earnings call transcripts across FY25 and FY26, we discovered a consistent structural phenomenon: the Management Optimism Gap. Management opening remarks consistently score between +0.79 and +0.89. However, during unscripted analyst Q&A, sentiment drops sharply into negative territory with 11 to 12 cautionary hedging words per 100 words. ICICI Bank displays the smallest gap at +1.09, reflecting stable execution, whereas TCS at +1.54 and Reliance at +1.48 faced aggressive analyst probing on tech spending delays and refining margin volatility.`
            },
            {
                num: 8,
                sec: "PART II: AI NLP PIPELINE & BENCHMARKS",
                spk: "Aditi Routray (246213548) | 45s",
                title: "90-Sentence Human Gold-Standard FinBERT Validation Benchmark",
                sub: "Rigorous Benchmark Evaluating Accuracy, Macro-F1, Cohen's Kappa & Failure Modes",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. 3x3 Confusion Matrix (N = 90 Sentences)</h3>
                            <table class="data-tbl">
                                <tr><th>Human Ground Truth</th><th>Pred. Positive</th><th>Pred. Neutral</th><th>Pred. Negative</th><th>Recall</th></tr>
                                <tr><td><strong>Positive (30)</strong></td><td>30</td><td>0</td><td>0</td><td>100.0%</td></tr>
                                <tr><td><strong>Neutral (30)</strong></td><td>0</td><td>29</td><td>1</td><td>96.7%</td></tr>
                                <tr><td><strong>Negative (30)</strong></td><td>3</td><td>0</td><td>27</td><td>90.0%</td></tr>
                            </table>
                            <p style="margin-top: 12px;"><strong>Per-Company Accuracy:</strong> ICICI Bank: 93.33% (28/30) | Reliance: 96.67% (29/30) | TCS: 96.67% (29/30).</p>
                        </div>
                        <div class="card">
                            <h3>2. Statistical Validation & Failure-Mode Audit</h3>
                            <p style="color: var(--accent-green); font-weight: bold; font-size: 13px; margin-bottom: 8px;">Accuracy: 95.56% | Macro-F1: 0.9555 | Cohen's Kappa: 0.9333 (Almost Perfect)</p>
                            <ul>
                                <li><strong>Double-Barreled Corporate Phrasing (3 Misses):</strong> FinBERT predicted Positive for 3 human Negative sentences where management used cautious qualifiers alongside growth metrics (e.g. 'calibrated unsecured lending expansion'). FinBERT overweighted 'expansion'.</li>
                                <li><strong>Neutral Hedging Ambiguity (1 Miss):</strong> FinBERT predicted Negative for 1 Neutral sentence on capex milestones.</li>
                                <li><strong>Pipeline Takeaway:</strong> Confirms why raw sentiment must be combined with our Hedging Density Index and DCF fundamentals rather than traded blindly.</li>
                            </ul>
                        </div>
                    </div>
                `,
                notes: `Rather than trusting FinBERT as a black box, we benchmarked it against 90 human gold-standard sentences, balanced evenly with 30 positive, 30 neutral, and 30 negative sentences. FinBERT achieved an outstanding 95.56% accuracy, a Macro-F1 of 0.9555, and a Cohen's Kappa of 0.9333, demonstrating almost perfect agreement with human analysts. Crucially, our confusion matrix identified exactly 4 failure cases where management paired cautious qualifiers with growth metrics, causing FinBERT to overweight the positive noun.`
            },
            {
                num: 9,
                sec: "PART II: AI NLP PIPELINE & BENCHMARKS",
                spk: "Aditi Routray (246213548) | 45s",
                title: "150-Headline Behavioral Bias Framing vs. Valuation Dislocation",
                sub: "Diagnosing How Media Narrative Biases Create Fundamental Price-to-Value Disconnects",
                html: `
                    <div class="grid-3">
                        <div class="card">
                            <h3>ICICI: Hype & FOMO</h3>
                            <ul>
                                <li><strong>Dominant Bias:</strong> 58% Hype / FOMO Chasing</li>
                                <li><strong>Media Sentiment:</strong> Positive (+0.2217)</li>
                                <li><strong>Narrative:</strong> Media crowns ICICI 'unstoppable champion' (+4.8% EPS revisions).</li>
                                <li><strong>Reality:</strong> Compounding strongly, but upside is +14.13%. Warranted compounder, but accumulate on dips, not FOMO chasing.</li>
                            </ul>
                        </div>
                        <div class="card" style="border-color: var(--accent-green);">
                            <h3>Reliance: Recency Bias</h3>
                            <ul>
                                <li><strong>Dominant Bias:</strong> 34% Recency Extrapolation</li>
                                <li><strong>Media Sentiment:</strong> Negative (-0.2879)</li>
                                <li><strong>Narrative:</strong> Traders extrapolate 2 quarters of weak refining margins & retail closures (-1.4% EPS trim).</li>
                                <li><strong>Reality:</strong> 5G capex has peaked; tariff hikes drive FCF surge (+21.91% upside). Contrarian BUY.</li>
                            </ul>
                        </div>
                        <div class="card">
                            <h3>TCS: Loss Aversion</h3>
                            <ul>
                                <li><strong>Dominant Bias:</strong> 50% Loss Aversion / AI Panic</li>
                                <li><strong>Media Sentiment:</strong> Negative (-0.3438)</li>
                                <li><strong>Narrative:</strong> Headlines fixate on GenAI headcount destruction & US spending cuts (-2.1% EPS trim).</li>
                                <li><strong>Reality:</strong> Reverse DCF proves market prices 5.13% vs 8.50% order-backed reality (+16.10% upside). ACCUMULATE.</li>
                            </ul>
                        </div>
                    </div>
                `,
                notes: `By classifying 150 financial news headlines into behavioral biases, we uncovered why our intrinsic valuations diverge so sharply from current market prices. In Reliance, the market suffers from 34% Recency Bias, extrapolating two quarters of weak refining margins while ignoring the post-5G free cash flow inflections—creating our largest margin of safety at +21.91%. In TCS, the market suffers from 50% Loss Aversion over GenAI staffing fears, pushing implied growth down to 5.13% vs. an 8.50% DCF reality. In ICICI Bank, 58% Hype confirms it is a core compounder, but one to accumulate on disciplined pullbacks.`
            },
            {
                num: 10,
                sec: "PART II: AI NLP PIPELINE & BENCHMARKS",
                spk: "Aditi Routray (246213548) | 45s",
                title: "Technical Momentum Indicators & 1,000-Path GBM Monte Carlo Fan Charts",
                sub: "Reconciling Backward-Looking Stochastic Price Drift with Forward Fundamental Valuation",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. Technical Indicators & Monte Carlo Metrics</h3>
                            <ul>
                                <li><strong>ICICI Bank (CMP ₹1,398.00):</strong> Strong Uptrend (Price > 50-DMA > 200-DMA), RSI = 56.97, MACD Hist = +3.76. 1Y MC Median (P50) = ₹1,553.35 (+11.11%), converging with DDM target ₹1,595.50.</li>
                                <li><strong>Reliance Industries (CMP ₹1,164.90):</strong> Consolidation below moving averages; RSI = 40.27 (Oversold); Bullish MACD crossover Hist = +0.36. Backward MC median is ₹1,125.15, but DCF target (₹1,420.14) sits at P82, setting up mean-reversion catalyst.</li>
                                <li><strong>TCS (CMP ₹2,502.60):</strong> Rebounding above moving averages; RSI = 67.56; MACD Hist = +16.22. DCF target (₹2,905.55) sits between P75 (₹2,774) and P90 (₹3,134).</li>
                            </ul>
                        </div>
                        <div class="img-card">
                            <img src="../01_data/cleaned/mc_fan_charts.png" alt="Monte Carlo Fan Charts">
                            <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 6px;">1,000-Path GBM Monte Carlo Fan Charts (1 Year Forward, Seed = 42)</p>
                        </div>
                    </div>
                `,
                notes: `Our technical indicators and 1,000-path Geometric Brownian Motion Monte Carlo simulations reveal why backward price extrapolation fails during cyclical turning points. While ICICI Bank exhibits a steady uptrend where the Monte Carlo median of Rs 1,553 converges with our DDM target, Reliance shows oversold RSI levels and an early positive MACD crossover, setting the stage for convergence toward our Rs 1,420 DCF target. I now hand over to our Project Lead, Sankarshana, to present portfolio construction.`
            },
            {
                num: 11,
                sec: "PART III: PORTFOLIO OPTIMIZATION",
                spk: "Sankarshana Mulugundam (246213080) | 50s",
                title: "Blended Expected Returns, MVO Tangency Portfolio & Efficient Frontier",
                sub: "Overcoming Historical Drift via 50% CAPM Ke + 50% DCF IRR Blended Return Vector",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. Blended Expected Returns & Tangency Portfolio</h3>
                            <ul>
                                <li><strong>The Historical Drift Trap:</strong> 5Y historical returns (Reliance +0.27%, TCS -3.77%) reflect past derating. Extrapolating them would cause optimizer collapse.</li>
                                <li><strong>Blended E(Ri) = 0.50 * CAPM Ke + 0.50 * DCF 5Y IRR:</strong>
                                    <ul>
                                        <li>ICICI Bank: 0.5(12.65%) + 0.5(15.33%) = <strong>13.99%</strong> (Vol = 19.55%, Beta = 0.9663)</li>
                                        <li>Reliance: 0.5(13.53%) + 0.5(17.57%) = <strong>15.55%</strong> (Vol = 22.33%, Beta = 1.1125)</li>
                                        <li>TCS: 0.5(11.76%) + 0.5(14.79%) = <strong>13.28%</strong> (Vol = 22.85%, Beta = 0.8184)</li>
                                        <li>91D RBI T-Bill: <strong>6.65%</strong> (Vol = 0.00%, Beta = 0.0000)</li>
                                    </ul>
                                </li>
                                <li><strong>Max-Sharpe Tangency Weights:</strong> ICICI Bank = 38.90% | Reliance = 37.91% | TCS = 23.19%</li>
                                <li><strong>Portfolio Metrics:</strong> E(Rp) = 14.42%, Vol = 15.74% (cuts 400–700 bps of standalone volatility!), Sharpe = 0.4935.</li>
                            </ul>
                        </div>
                        <div class="img-card">
                            <img src="../01_data/cleaned/efficient_frontier_cal.png" alt="Efficient Frontier & CAL">
                            <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 6px;">Markowitz Efficient Frontier & Capital Allocation Line (Rf = 6.65%)</p>
                        </div>
                    </div>
                `,
                notes: `Thank you Aditi. Standard Markowitz optimization collapses when fed backward-looking 5-year returns, because past cyclical multiple compression in Reliance and TCS would suggest zero allocation. To solve this, we blended 50% CAPM equilibrium returns with 50% DCF 5-year implied IRRs. Our Max-Sharpe Tangency portfolio allocates 38.90% to ICICI Bank, 37.91% to Reliance, and 23.19% to TCS, delivering an expected return of 14.42% at a volatility of only 15.74%—slashing standalone risk by up to 700 basis points and yielding a Sharpe ratio of 0.4935.`
            },
            {
                num: 12,
                sec: "PART III: PORTFOLIO OPTIMIZATION",
                spk: "Sankarshana Mulugundam (246213080) | 50s",
                title: "Utility Allocation, Prudence Override & Featured Case Study (A = 4.00)",
                sub: "Two-Fund Separation along CAL & Capital Allocations for ₹10 Lakh Lump Sum & ₹25k SIP",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. Risk Profiler & Prudence Override Rule</h3>
                            <ul>
                                <li><strong>Two-Dimensional Scoring:</strong> Ability (Sec A: 5–20) + Willingness (Sec B: 5–20). Total R in [10, 40].</li>
                                <li><strong>Prudence Override:</strong> If |Sec A - Sec B| >= 6 -> Reff = 2 * min(Sec A, Sec B). Prevents emotionally aggressive investors with fragile balance sheets from catastrophic drawdowns.</li>
                                <li><strong>Risk Aversion A:</strong> A = 10 - 0.3 * (Reff - 10). Maps continuously from A = 1.00 down to A = 10.00.</li>
                                <li><strong>Separation Theorem:</strong> y* = min(1.0, (E(Rtan) - Rf) / (A * sigma_tan^2)). T-Bill = 1 - y*.</li>
                            </ul>
                        </div>
                        <div class="card" style="border-color: var(--accent-green);">
                            <h3>2. Featured Case Study: A = 4.00 (R = 30)</h3>
                            <p style="color: var(--accent-green); font-weight: bold; margin-bottom: 8px;">Sec A = 15, Sec B = 15 -> Equity y* = 78.41% | T-Bill 1-y* = 21.59%<br>E(Rc) = 12.74% | Vol = 12.34% | Beta = 0.7742 | Sharpe = 0.4935</p>
                            <table class="data-tbl">
                                <tr><th>Asset</th><th>Weight</th><th>₹10 Lakh Lump Sum</th><th>₹25k Monthly SIP</th></tr>
                                <tr><td>ICICI Bank</td><td>30.50%</td><td>₹3,05,000</td><td>₹7,625 / mo</td></tr>
                                <tr><td>Reliance Ind.</td><td>29.72%</td><td>₹2,97,200</td><td>₹7,430 / mo</td></tr>
                                <tr><td>TCS</td><td>18.18%</td><td>₹1,81,800</td><td>₹4,545 / mo</td></tr>
                                <tr><td>91D T-Bill</td><td>21.59%</td><td>₹2,15,900</td><td>₹5,398 / mo</td></tr>
                                <tr class="highlight"><td>Total Complete</td><td>100.00%</td><td>₹10,00,000</td><td>₹25,000 / mo</td></tr>
                            </table>
                        </div>
                    </div>
                `,
                notes: `By Tobin's Separation Theorem, all rational investors hold the identical Tangency equity basket, scaling their exposure y-star along the Capital Allocation Line based on their risk aversion A. Our 10-question profiler scores both financial ability and psychological willingness; our Prudence Override rule safeguards against balance sheet fragility. In our featured moderate-growth case study at A = 4.00, the optimal allocation is 78.41% equity and 21.59% T-Bills. For a 10 Lakh Rupee portfolio, this translates directly to Rs 3.05 Lakh in ICICI, Rs 2.97 Lakh in Reliance, Rs 1.82 Lakh in TCS, and Rs 2.16 Lakh in liquid T-Bills.`
            },
            {
                num: 13,
                sec: "PART III: PORTFOLIO OPTIMIZATION",
                spk: "Sankarshana Mulugundam (246213080) | 45s",
                title: "20-Year Step-Up SIP Lifecycle Glide Path (₹25,000/mo, +10% Annual Step-Up)",
                sub: "Dynamic 3-Phase Lifecycle Rebalancing from Early-Career Accumulation to Capital Preservation",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. 3-Phase Lifecycle Architecture</h3>
                            <ul>
                                <li><strong>Phase 1 (Years 1–8, Age 25–32):</strong> 100% Equity (Aggressive, A = 2.20). Maximum compounding when human capital is highest.</li>
                                <li><strong>Phase 2 (Years 9–15, Age 33–39):</strong> 64.0% Equity / 36.0% T-Bill (Balanced, A = 4.90). Mid-career drawdown dampening.</li>
                                <li><strong>Phase 3 (Years 16–20, Age 40–44):</strong> 36.9% Equity / 63.1% T-Bill (Defensive, A = 8.50). Pre-retirement preservation eliminating sequence risk.</li>
                                <li><strong>Wealth Outcomes:</strong>
                                    <ul>
                                        <li>Total Capital Invested: <strong>₹1.7182 Crore</strong></li>
                                        <li>Deterministic Corpus: <strong style="color: var(--accent-green);">₹4.3241 Crore (2.52x Multiple)</strong></li>
                                        <li>Monte Carlo Median P50: <strong>₹4.1962 Crore</strong> (P10 ₹3.18 Cr, P90 ₹5.74 Cr)</li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="img-card">
                            <img src="../01_data/cleaned/sip_glide_path.png" alt="20-Year SIP Glide Path">
                            <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 6px;">20-Year Wealth Accumulation & Asset Allocation Glide Path</p>
                        </div>
                    </div>
                `,
                notes: `We operationalized our allocation model into a 20-year Step-Up SIP lifecycle glide path starting at Rs 25,000 per month with a disciplined 10% annual step-up. The portfolio automatically glides through three distinct phases: 100% equity during early accumulation, shifting to 64% equity in mid-career, and locking in 63.1% in risk-free sovereign T-Bills during the final five years. Over 20 years, an investor deposits Rs 1.72 Crore, compounding to an expected deterministic corpus of Rs 4.32 Crore—with our 1,000-path Monte Carlo confirming a 90% probability of exceeding Rs 3.18 Crore.`
            },
            {
                num: 14,
                sec: "PART III: PORTFOLIO OPTIMIZATION",
                spk: "Sankarshana Mulugundam (246213080) | 45s",
                title: "Mandatory 4-Metric Portfolio Evaluation & 5-Year Historical Backtest",
                sub: "Evaluation Across Sharpe, Treynor, Jensen's Alpha & Information Ratio vs. Nifty 50 Benchmark",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. 4-Ratio Performance Evaluation</h3>
                            <table class="data-tbl">
                                <tr><th>Strategy</th><th>Beta</th><th>Sharpe</th><th>Treynor</th><th>Alpha</th><th>Info Ratio</th></tr>
                                <tr><td>Tangency (A=2.20)</td><td>0.9874</td><td>0.4935</td><td>0.0786</td><td>+1.84%</td><td>+0.2274</td></tr>
                                <tr class="highlight"><td>Featured (A=4.00)</td><td>0.7742</td><td>0.4935</td><td>0.0786</td><td>+1.45%</td><td>+0.0144</td></tr>
                                <tr><td>Balanced (A=4.90)</td><td>0.6320</td><td>0.4935</td><td>0.0786</td><td>+1.18%</td><td>+0.1171</td></tr>
                                <tr><td>Defensive (A=8.50)</td><td>0.3643</td><td>0.4940</td><td>0.0786</td><td>+0.68%</td><td>+0.0058</td></tr>
                                <tr><td>Nifty 50 Index</td><td>1.0000</td><td>0.4328</td><td>0.0600</td><td>0.00%</td><td>0.0000</td></tr>
                            </table>
                            <p style="margin-top: 10px; font-size: 12px; color: var(--text-muted);">
                                <strong>Sharpe Invariance:</strong> By Two-Fund Separation, all portfolios along the CAL achieve identical Sharpe (~0.4935) and Treynor (0.0786) because excess return and vol scale linearly with y*.
                            </p>
                        </div>
                        <div class="img-card">
                            <img src="../01_data/cleaned/backtest_performance.png" alt="5-Year Historical Backtest">
                            <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 6px;">5-Year Realized Wealth Accumulation (₹100 Base)</p>
                        </div>
                    </div>
                `,
                notes: `Evaluating our portfolios across the four mandatory course ratios—Sharpe, Treynor, Jensen's Alpha, and Information Ratio—proves the quantitative superiority of our framework over the Nifty 50 benchmark. Notice a profound mathematical result: by Tobin's Separation Theorem, the Sharpe ratio of 0.4935 and Treynor measure of 0.0786 are identical across our Tangency, Featured A = 4.00, Balanced, and Defensive portfolios because both excess return and volatility scale linearly with equity weight y-star. Meanwhile, every basket generates positive Jensen's Alpha, led by +1.84% in the Tangency portfolio.`
            },
            {
                num: 15,
                sec: "SYNTHESIS & CONCLUSION",
                spk: "Sankarshana Mulugundam (246213080) | 45s",
                title: "Final Investment Synthesis, Actionable Verdict & Live Dashboard Demo",
                sub: "Triangulated Asset Allocation Verdicts, Methodological Limitations & Interactive Streamlit App",
                html: `
                    <div class="grid-2">
                        <div class="card">
                            <h3>1. Final Triangulated Investment Verdicts</h3>
                            <ul>
                                <li><strong style="color: var(--accent-green);">Reliance Industries (BUY — 37.91% Tangency / 29.72% in A=4.00):</strong> +21.91% DCF upside (₹1,420.14) & SOTP cross-check (₹1,441.95). Free cash flow surge post-5G capex. Contrarian BUY against 34% media recency bias.</li>
                                <li><strong style="color: #38bdf8;">ICICI Bank (ACCUMULATE — 38.90% Tangency / 30.50% in A=4.00):</strong> +14.13% DDM upside (₹1,595.50). 17.5% ROE, lowest concall optimism gap (+1.09), pristine 0.45% Net NPA. Core compounding foundation.</li>
                                <li><strong style="color: #38bdf8;">TCS (ACCUMULATE — 23.19% Tangency / 18.18% in A=4.00):</strong> +16.10% DCF upside (₹2,905.55). Reverse DCF proves market over-discounts AI panic (prices 5.13% vs 8.50% reality). Defensive USD tech hedge.</li>
                                <li><strong style="color: var(--accent-gold);">91-Day RBI T-Bill (Core Sovereign Anchor — 21.59% in A=4.00):</strong> Guaranteed 6.65% sovereign yield eliminating sequence risk.</li>
                            </ul>
                        </div>
                        <div class="card">
                            <h3>2. Dashboard Demo & Research Limitations</h3>
                            <ul>
                                <li><strong>Offline Streamlit App (05_dashboard/app.py):</strong> 9 interactive blocks, live slider recalculations, zero external API latency or hallucinations.</li>
                                <li><strong>Research Limitations:</strong>
                                    <ul>
                                        <li>Double-barreled concall sentences in FinBERT require multi-agent LLM consensus.</li>
                                        <li>GBM constant drift/vol fails to capture fat tails (future jump-diffusion extension).</li>
                                        <li>Static 5-year covariance assumes stationary correlations (DCC-GARCH would enhance dynamic rebalancing).</li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                    </div>
                `,
                notes: `In conclusion, our study demonstrates that combining fundamental intrinsic valuation with AI-augmented FinBERT sentiment analysis enables institutional investors to look beyond consensus media noise and capitalize on genuine market dislocations. Reliance Industries is our top contrarian BUY with a +21.91% upside; ICICI Bank is our steady private credit compounder at +14.13%; and TCS provides a resilient USD cash cow yielding +16.10% upside. All 9 modules are fully interactive in our offline Streamlit dashboard. Thank you, and we now welcome your questions.`
            },
            {
                num: 16,
                sec: "APPENDIX: FACULTY VIVA DEFENSE",
                spk: "All Team Members | Viva Guide",
                title: "Appendix: Faculty Viva Voce Defense Guide (6 Toughest Questions)",
                sub: "Rigorous Quantitative Responses to Critical Methodological & Theoretical Inquiries",
                html: `
                    <div class="card">
                        <table class="data-tbl">
                            <tr><th>Question</th><th>Crisp Quantitative Defense Answer</th></tr>
                            <tr><td><strong>Q1: Why 2-Stage DDM for ICICI Bank instead of FCFF DCF?</strong></td><td>In commercial banks, deposits (₹18.02L Cr) and debt are operational inventory used to produce NII, not financing capital. Working capital and WACC cannot be separated from operating flows. Valuing equity directly via 2-Stage DDM and Excess Equity Return ((ROE - Ke) * BVPS) discounted at CAPM Ke (12.65%) is the only sound framework.</td></tr>
                            <tr><td><strong>Q2: TCS 5Y return is -3.77%. How justify +16.10% DCF upside?</strong></td><td>TCS derated from ~32x to 18.4x FY26 P/E due to post-COVID multiple compression, even while revenue grew to ₹2.58L Cr and PAT hit ₹49,200 Cr with 51% ROE. Our Reverse DCF proves CMP implies an overly pessimistic 5.13% 5Y CAGR, whereas its $41B+ TCV order book supports 8.50% CAGR (+337 bps unpriced growth).</td></tr>
                            <tr><td><strong>Q3: How guarantee AI didn't hallucinate annual report data?</strong></td><td>All valuation math is in deterministic Python, not LLM prompts. For qualitative notes, we built a verbatim string verifier (difflib.SequenceMatcher) matching extracted quotes against raw source filings. All 12/12 quotes achieved a 1.0000 similarity ratio (0.00% hallucination rate).</td></tr>
                            <tr><td><strong>Q4: What caused FinBERT's 4 benchmark misclassifications?</strong></td><td>Double-barreled corporate phrasing where management paired cautious qualifiers ('calibrated growth', 'repricing headwind') with growth metrics. FinBERT overweighted the growth noun. This is why we created our explicit Hedging Density Index (~11-12/100w in Q&A).</td></tr>
                            <tr><td><strong>Q5: Why two different risk-free rates (6.85% vs 6.65%)?</strong></td><td>Duration matching: in DCF/DDM, we discount perpetual cash flows spanning decades, requiring the 10-Year India G-Sec yield (6.85%). In portfolio optimization, the risk-free asset (1-y*) must be a zero-duration money-market asset free of mark-to-market risk, matching the 91-Day RBI T-Bill (6.65%).</td></tr>
                            <tr><td><strong>Q6: Why are Sharpe and Treynor invariant across utility baskets?</strong></td><td>By Tobin's Separation Theorem, all complete portfolios along the CAL are linear combinations of the Tangency basket and the risk-free T-Bill. Because excess return E(Rc)-Rf = y*(E(Rtan)-Rf) and volatility sigma_c = y*sigma_tan both scale linearly with y*, their ratio (Sharpe = 0.4935, Treynor = 0.0786) is mathematically invariant.</td></tr>
                        </table>
                    </div>
                `,
                notes: `This appendix slide contains our prepared defense for the six most probable theoretical and quantitative questions the faculty may ask during the viva session.`
            }
        ];

        let currentSlide = 0;

        function renderSlide(index) {
            const main = document.getElementById('main-content');
            const data = slideData[index];
            
            main.innerHTML = `
                <div class="slide-container active">
                    <div class="slide-header">
                        <div class="slide-meta">
                            <span class="badge-num">SLIDE ${data.num < 10 ? '0' + data.num : data.num} / 16</span>
                            <span>|</span>
                            <span class="badge-sec">${data.sec}</span>
                            <span>|</span>
                            <span class="badge-spk">${data.spk}</span>
                        </div>
                        <div class="slide-title">${data.title}</div>
                        <div class="slide-subtitle">${data.sub}</div>
                    </div>
                    ${data.html}
                </div>
            `;
            
            document.getElementById('slide-indicator').textContent = `Slide ${data.num} / ${slideData.length}`;
            document.getElementById('progress-fill').style.width = `${(data.num / slideData.length) * 100}%`;
            document.getElementById('notes-text').textContent = data.notes;
        }

        function nextSlide() {
            if (currentSlide < slideData.length - 1) {
                currentSlide++;
                renderSlide(currentSlide);
            }
        }

        function prevSlide() {
            if (currentSlide > 0) {
                currentSlide--;
                renderSlide(currentSlide);
            }
        }

        function toggleNotes() {
            const panel = document.getElementById('notes-panel');
            panel.classList.toggle('open');
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') {
                nextSlide();
            } else if (e.key === 'ArrowLeft') {
                prevSlide();
            } else if (e.key === 'n' || e.key === 'N') {
                toggleNotes();
            }
        });

        // Initial render
        renderSlide(0);
    </script>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    shutil.copy2(html_path, deliverable_copy)
    print(f"Successfully generated {html_path}")
    print(f"Copied to SA_final_presentation.html")


def main():
    root_dir = Path(__file__).resolve().parent.parent
    print("Building institutional PowerPoint deck (16:9 Widescreen)...")
    build_powerpoint(root_dir)

    print("\nBuilding interactive standalone HTML presentation...")
    build_interactive_html(root_dir)

    print("\nPresentation creation complete!")


if __name__ == "__main__":
    main()
