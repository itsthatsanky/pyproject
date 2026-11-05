"""Visual, low-text presentation deck (dashboard-inspired). Data: Excel/JSON/graphs only."""
import shutil
import sys
from pathlib import Path

import pptx
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "01_data" / "cleaned"


def rgb(h):
    return RGBColor.from_string(h.lstrip("#").upper())


NAVY, BLUE, TEAL, GREY = "0F2B46", "1F4E78", "008080", "95A5A6"
MID, ORANGE, GREEN, RED, GOLD = "2E75B6", "D35400", "27AE60", "C0392B", "F39C12"
BG, CARD, INK, MUTED, WHITE = "F4F7FB", "FFFFFF", "0F172A", "64748B", "FFFFFF"
CO = {"ICICI": BLUE, "REL": MID, "TCS": TEAL, "TB": GREY}

prs = pptx.Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def rect(s, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
    sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb(fill)
    if line:
        sh.line.color.rgb = rgb(line)
        sh.line.width = Pt(1)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def text(s, x, y, w, h, t, size=14, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    lines = t if isinstance(t, list) else [t]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = ln
        r.font.size, r.font.bold, r.font.italic = Pt(size), bold, italic
        r.font.color.rgb = rgb(color)
        r.font.name = "Calibri"
    return tb


def slide(n, title, sub, speaker):
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, 13.333, 7.5, BG)
    rect(s, 0, 0, 13.333, 1.05, NAVY)
    rect(s, 0, 1.05, 13.333, 0.06, GOLD)
    text(s, 0.5, 0.12, 10.6, 0.55, title, 26, True, WHITE)
    text(s, 0.5, 0.64, 10.6, 0.35, sub, 13, False, "BFD3EA", italic=True)
    text(s, 10.6, 0.14, 2.3, 0.35, f"{n:02d} / 15", 14, True, "F7C873", PP_ALIGN.RIGHT)
    text(s, 10.0, 0.52, 2.9, 0.35, speaker, 11, False, "BFD3EA", PP_ALIGN.RIGHT)
    return s


def card(s, x, y, w, h, accent=None):
    rect(s, x, y, w, h, CARD, "E2E8F0", MSO_SHAPE.ROUNDED_RECTANGLE).adjustments[0] = 0.05
    if accent:
        rect(s, x, y + 0.12, 0.08, h - 0.24, accent)


def kpi(s, x, y, w, h, value, label, color=BLUE, vsize=30):
    card(s, x, y, w, h, color)
    text(s, x + 0.2, y + 0.08, w - 0.3, h * 0.6, value, vsize, True, color, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 0.2, y + h * 0.62, w - 0.3, h * 0.36, label, 11, False, MUTED)


def chip(s, x, y, w, label, fill, color=WHITE, size=11, h=0.34):
    sh = rect(s, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    sh.adjustments[0] = 0.5
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = Inches(0.04)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.size, r.font.bold = Pt(size), True
    r.font.color.rgb = rgb(color)
    r.font.name = "Calibri"


def picture(s, path, x, y, maxw, maxh):
    if not Path(path).exists():
        return
    pic = s.shapes.add_picture(str(path), Inches(x), Inches(y), width=Inches(maxw))
    if pic.height > Inches(maxh):
        ratio = Inches(maxh) / pic.height
        pic.height = Inches(maxh)
        pic.width = int(pic.width * ratio)
    pic.left = Inches(x) + int((Inches(maxw) - pic.width) / 2)


def notes(s, script):
    s.notes_slide.notes_text_frame.text = script


def style_chart(ch, legend=True, size=11):
    ch.font.size = Pt(size)
    ch.font.name = "Calibri"
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout = False


def bar_chart(s, x, y, w, h, cats, series, colors, fmt='#,##0', title=None, horizontal=False):
    cd = CategoryChartData()
    cd.categories = cats
    for name, vals in series:
        cd.add_series(name, vals)
    kind = XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
    gf = s.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    style_chart(ch, legend=len(series) > 1)
    if title:
        ch.has_title = True
        ch.chart_title.text_frame.text = title
        ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(13)
        ch.chart_title.text_frame.paragraphs[0].runs[0].font.bold = True
    else:
        ch.has_title = False
    ch.value_axis.has_major_gridlines = False
    ch.value_axis.visible = False
    plot = ch.plots[0]
    plot.gap_width = 60
    plot.has_data_labels = True
    plot.data_labels.number_format = fmt
    plot.data_labels.number_format_is_linked = False
    plot.data_labels.font.size = Pt(11)
    plot.data_labels.font.bold = True
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    for i, c in enumerate(colors):
        if i < len(plot.series):
            plot.series[i].format.fill.solid()
            plot.series[i].format.fill.fore_color.rgb = rgb(c)
    return ch


def donut(s, x, y, w, h, cats, vals, colors, title=None):
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("Weight", vals)
    gf = s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    style_chart(ch, legend=True, size=11)
    ch.has_title = bool(title)
    if title:
        ch.chart_title.text_frame.text = title
        ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(13)
        ch.chart_title.text_frame.paragraphs[0].runs[0].font.bold = True
    plot = ch.plots[0]
    plot.has_data_labels = True
    plot.data_labels.number_format = '0.0%'
    plot.data_labels.number_format_is_linked = False
    plot.data_labels.font.size = Pt(12)
    plot.data_labels.font.bold = True
    plot.data_labels.font.color.rgb = rgb(WHITE)
    for i, c in enumerate(colors):
        pt = plot.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = rgb(c)
    return ch


def table(s, x, y, w, h, rows, widths, hl_row=None, font=12):
    shp = s.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(h))
    t = shp.table
    for i, cw in enumerate(widths):
        t.columns[i].width = Inches(cw)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.text = str(val)
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = rgb(BLUE)
            elif hl_row is not None and r == hl_row:
                cell.fill.fore_color.rgb = rgb("DDF3E4")
            else:
                cell.fill.fore_color.rgb = rgb(CARD if r % 2 else "EEF3F9")
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
                for run in p.runs:
                    run.font.size = Pt(font)
                    run.font.name = "Calibri"
                    run.font.bold = (r == 0) or (hl_row is not None and r == hl_row)
                    run.font.color.rgb = rgb(WHITE if r == 0 else INK)
    return t


SASI, ADITI, SANK = "Sasi", "Aditi Routray", "Sankarshana M."

# ---------------------------------------------------------------- 1 Title
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0, 0, 13.333, 7.5, BLUE).fill.fore_color.rgb = rgb(NAVY)
rect(s, 8.2, 0, 5.133, 7.5, BLUE)
rect(s, 0.6, 1.0, 0.9, 0.08, GOLD)
text(s, 0.6, 1.2, 7.4, 2.4, "Beyond the Consensus", 48, True, WHITE)
text(s, 0.6, 2.35, 7.4, 1.6, "AI-Augmented Fundamental Valuation of Core Indian Blue Chips with Risk-Calibrated Portfolio Construction", 18, False, "BFD3EA")
for i, (nm, rl, col) in enumerate([("ICICI Bank", "DDM", CO["ICICI"]), ("Reliance", "DCF + SOTP", CO["REL"]), ("TCS", "DCF + Reverse DCF", CO["TCS"]), ("91D T-Bill", "Risk-free anchor", CO["TB"])]):
    x = 0.6 + i * 1.85
    rect(s, x, 4.35, 1.75, 1.0, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x, 4.45, 1.75, 0.45, nm, 16, True, WHITE, PP_ALIGN.CENTER)
    text(s, x, 4.9, 1.75, 0.4, rl, 11, False, WHITE, PP_ALIGN.CENTER)
text(s, 0.6, 5.9, 7.4, 0.4, "Sankarshana Mulugundam 246213080  •  Aditi Routray 246213548  •  Sasi 246213618", 13, False, "BFD3EA")
text(s, 8.6, 0.9, 4.4, 0.4, "SINGLE SOURCE OF TRUTH", 13, True, "F7C873")
for i, (v, l) in enumerate([("2026-10-30", "Price cutoff"), ("6.85%", "10Y G-Sec (DCF / DDM)"), ("6.65%", "91D T-Bill (portfolio Rf)"), ("6.00%", "India ERP"), ("25.17%", "Corporate tax")]):
    y = 1.5 + i * 1.05
    text(s, 8.6, y, 4.3, 0.55, v, 30, True, WHITE)
    text(s, 8.6, y + 0.5, 4.3, 0.35, l, 12, False, "BFD3EA")
notes(s, "Good morning Professor and panel. We present Beyond the Consensus: multi-model valuation of ICICI Bank, Reliance and TCS, live FinBERT NLP, and utility-based portfolio construction anchored on the 91-day RBI T-Bill. I am Sasi; Aditi covers the AI pipeline; Sankarshana covers portfolio construction.")

# ---------------------------------------------------------------- 2 Universe
s = slide(2, "Universe: 3 Stocks + 1 Sovereign Anchor", "Low correlation proves real diversification", SASI)
card(s, 0.4, 1.35, 6.4, 5.7)
picture(s, IMG / "correlation_heatmap.png", 0.5, 1.45, 6.2, 5.5)
tiles = [("ICICI Bank", "Private credit", CO["ICICI"]), ("Reliance", "Energy • Jio • Retail", CO["REL"]), ("TCS", "Global IT • USD hedge", CO["TCS"]), ("91D T-Bill 6.65%", "Core #4 • Risk-free anchor", CO["TB"])]
for i, (a, b, c) in enumerate(tiles):
    x, y = 7.05 + (i % 2) * 3.0, 1.35 + (i // 2) * 1.35
    rect(s, x, y, 2.85, 1.2, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x + 0.1, y + 0.12, 2.65, 0.5, a, 17, True, WHITE)
    text(s, x + 0.1, y + 0.65, 2.65, 0.4, b, 12, False, WHITE)
kpi(s, 7.05, 4.1, 2.85, 1.15, "0.34", "Avg pairwise correlation", GREEN)
kpi(s, 10.05, 4.1, 2.85, 1.15, "0.73", "TCS vs Infosys (same sector)", RED)
text(s, 7.05, 5.45, 5.8, 0.35, "REJECTED", 12, True, MUTED)
for i, r in enumerate(["ITC", "HUL", "Cummins", "Coal India", "Abbott", "IHCL", "BSE"]):
    chip(s, 7.05 + (i % 4) * 1.5, 5.85 + (i // 4) * 0.45, 1.4, r, "94A3B8")
notes(s, "We picked three orthogonal engines of the Indian economy plus the 91-day T-Bill as risk-free anchor. Average pairwise correlation is 0.34 versus 0.73 for TCS-Infosys. We explicitly rejected ITC, HUL, Cummins, Coal India, Abbott India, IHCL and BSE Ltd.")

# ---------------------------------------------------------------- 3 Financials
s = slide(3, "5-Year Financial Health & Forensic Audit", "FY22 – FY26 • cash conversion above 95% everywhere", SASI)
cos = [("ICICI Bank", CO["ICICI"], [("17.5%", "ROE"), ("0.45%", "Net NPA"), ("₹92,400 Cr", "NII (18% CAGR)")]),
       ("Reliance", CO["REL"], [("₹1.82 L Cr", "EBITDA"), ("95.9%", "CFO / EBITDA"), ("₹10.15 L Cr", "Revenue")]),
       ("TCS", CO["TCS"], [("51.0%", "ROE"), ("98.2%", "CFO / PAT"), ("24.5%", "EBIT margin")])]
for i, (nm, col, ks) in enumerate(cos):
    x = 0.4 + i * 4.2
    rect(s, x, 1.4, 4.0, 0.6, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x, 1.42, 4.0, 0.55, nm, 20, True, WHITE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    for j, (v, l) in enumerate(ks):
        kpi(s, x, 2.15 + j * 1.3, 4.0, 1.2, v, l, col, 28)
text(s, 0.4, 6.1, 4, 0.35, "FORENSIC CHECKS", 12, True, MUTED)
for i, b in enumerate(["Ind AS 116 leases deducted from EV", "Ind AS 24 RPTs arm's-length", "Ind AS 37 94% ICICI hedged FX", "Clean auditor opinions"]):
    chip(s, 0.4 + i * 3.15, 6.5, 3.05, "✓ " + b, GREEN, size=11, h=0.42)
notes(s, "Before projecting cash flows we audited five years of financials. All three convert more than 95 percent of earnings to cash. Lease liabilities under Ind AS 116 are deducted in every EV bridge, related-party transactions are arm's length and 94 percent of ICICI's contingent liabilities are hedged FX contracts.")

# ---------------------------------------------------------------- 4 Valuation
s = slide(4, "Intrinsic Value vs Market Price", "Each model tailored to the business structure", SASI)
card(s, 0.4, 1.35, 7.4, 5.7)
bar_chart(s, 0.5, 1.45, 7.2, 5.5, ["ICICI Bank", "Reliance", "TCS"], [("Market price (₹)", (1398.00, 1164.90, 2502.60)), ("Intrinsic value (₹)", (1595.50, 1420.14, 2905.55))], [GREY, GREEN], '#,##0')
vals = [("ICICI Bank", "+14.13%", "ACCUMULATE", "2-Stage DDM • Ke 12.65%", CO["ICICI"]),
        ("Reliance", "+21.91%", "BUY", "FCFF DCF + SOTP ₹1,441.95 • WACC 12.10%", CO["REL"]),
        ("TCS", "+16.10%", "ACCUMULATE", "DCF + Reverse DCF • WACC 11.65%", CO["TCS"])]
for i, (nm, up, rec, mdl, col) in enumerate(vals):
    y = 1.35 + i * 1.92
    card(s, 8.05, y, 4.9, 1.78, col)
    text(s, 8.3, y + 0.08, 2.5, 0.4, nm, 17, True, col)
    text(s, 8.3, y + 0.5, 2.6, 0.7, up, 34, True, GREEN)
    chip(s, 10.95, y + 0.2, 1.85, rec, GREEN if rec == "BUY" else MID, size=12, h=0.4)
    text(s, 8.3, y + 1.28, 4.5, 0.4, mdl, 11, False, MUTED)
notes(s, "Banks cannot be valued with FCFF because deposits are operating inventory, so ICICI uses a 2-stage DDM: 1,595.50, plus 14.13 percent. Reliance uses a consolidated DCF of 1,420.14, plus 21.91 percent, cross-checked by SOTP at 1,441.95. TCS DCF gives 2,905.55, plus 16.10 percent, and the reverse DCF shows the market only prices 5.13 percent growth versus 8.5 percent.")

# ---------------------------------------------------------------- 5 Sensitivity
s = slide(5, "Stress Test: Bear – Base – Bull", "5x5 sensitivity grids (±100 bps discount rate and growth)", SASI)
card(s, 0.4, 1.35, 8.0, 5.7)
bar_chart(s, 0.5, 1.45, 7.8, 5.5, ["ICICI Bank", "Reliance", "TCS"],
          [("Bear", (1207.85, 1082.93, 2345.10)), ("Base", (1595.50, 1420.14, 2905.55)), ("Bull", (2275.58, 2015.42, 3896.80)), ("Market", (1398.00, 1164.90, 2502.60))],
          [RED, BLUE, GREEN, GREY], '#,##0')
kpi(s, 8.7, 1.35, 4.25, 1.6, "₹1,165", "Reliance CMP sits near its bear case (₹1,083)", CO["REL"], 32)
kpi(s, 8.7, 3.1, 4.25, 1.6, "+55.7%", "TCS bull-case upside vs -6.3% worst-case", CO["TCS"], 32)
kpi(s, 8.7, 4.85, 4.25, 1.6, "9.4x vs 42x", "Reliance EV/EBITDA vs DMart peer", CO["ICICI"], 30)
text(s, 8.7, 6.55, 4.3, 0.5, "TCS 18.4x P/E vs Infosys 22.1x • ICICI 3.34x P/B", 11, False, MUTED)
notes(s, "Across the five by five grids every company keeps upside near the base case. Reliance trades near its bear-case value, TCS has an asymmetric payoff of plus 55.7 percent versus minus 6.3 percent. On relative multiples Reliance trades at 9.4 times EV/EBITDA versus 42 times for DMart. Now Aditi will take over.")

# ---------------------------------------------------------------- 6 AI pipeline
s = slide(6, "AI Pipeline: Zero Hallucination", "Live FinBERT + deterministic verification", ADITI)
steps = [("1", "24 concall\ntranscripts", BLUE), ("2", "Live FinBERT\ninference", MID), ("3", "Verbatim quote\nverifier", TEAL), ("4", "90-sentence\nhuman benchmark", ORANGE), ("5", "150-headline\nbias framing", GOLD)]
for i, (n, lbl, col) in enumerate(steps):
    x = 0.4 + i * 2.55
    sh = rect(s, x, 1.55, 2.45, 1.5, col, shape=MSO_SHAPE.PENTAGON)
    text(s, x + 0.1, 1.62, 0.6, 0.5, n, 26, True, WHITE)
    text(s, x + 0.35, 2.05, 1.9, 0.9, lbl.split("\n"), 14, True, WHITE)
kpi(s, 0.4, 3.5, 4.1, 2.0, "12 / 12", "annual-report quotes verified", GREEN, 44)
kpi(s, 4.65, 3.5, 4.1, 2.0, "1.0000", "SequenceMatcher similarity", BLUE, 44)
kpi(s, 8.9, 3.5, 4.05, 2.0, "0.00%", "hallucination rate", GREEN, 44)
text(s, 0.4, 5.85, 12.5, 0.8, "Valuation math is deterministic Python. AI only extracts and scores text, and every extraction is checked against the source.", 16, False, MUTED, PP_ALIGN.CENTER)
notes(s, "To avoid LLM hallucination we paired live FinBERT with a deterministic verifier. All 12 extracted annual report quotes matched the source with similarity 1.0000, a 0.00 percent hallucination rate.")

# ---------------------------------------------------------------- 7 Sentiment
s = slide(7, "Management Optimism Gap", "Scripted remarks vs unscripted analyst Q&A (24 concalls)", ADITI)
card(s, 0.4, 1.35, 8.2, 5.7)
picture(s, IMG / "sentiment_trends.png", 0.5, 1.45, 8.0, 5.5)
for i, (nm, g, d, col) in enumerate([("ICICI Bank", "+1.09", "Remarks +0.88 • Q&A -0.22", CO["ICICI"]), ("Reliance", "+1.48", "Remarks +0.89 • Q&A -0.59", CO["REL"]), ("TCS", "+1.54", "Remarks +0.79 • Q&A -0.75", CO["TCS"])]):
    y = 1.35 + i * 1.92
    card(s, 8.85, y, 4.1, 1.78, col)
    text(s, 9.1, y + 0.08, 3.5, 0.4, nm + " gap", 15, True, col)
    text(s, 9.1, y + 0.45, 3.5, 0.8, g, 38, True, col)
    text(s, 9.1, y + 1.28, 3.7, 0.4, d, 11, False, MUTED)
notes(s, "Opening remarks score between plus 0.79 and plus 0.89, but unscripted Q&A turns negative with 11 to 12 hedging words per 100. ICICI has the narrowest gap at 1.09; Reliance is 1.48 and TCS 1.54.")

# ---------------------------------------------------------------- 8 Benchmark
s = slide(8, "FinBERT vs Human Gold Standard", "90 hand-labelled sentences (30 per company)", ADITI)
kpi(s, 0.4, 1.4, 4.0, 1.7, "95.56%", "Accuracy (86 / 90)", GREEN, 40)
kpi(s, 4.65, 1.4, 4.0, 1.7, "0.9555", "Macro-F1", BLUE, 40)
kpi(s, 8.9, 1.4, 4.05, 1.7, "0.9333", "Cohen's Kappa • almost perfect", TEAL, 40)
card(s, 0.4, 3.4, 7.0, 3.65)
text(s, 0.6, 3.5, 6.5, 0.4, "Confusion matrix (rows = human, cols = FinBERT)", 13, True, BLUE)
table(s, 0.6, 3.95, 6.6, 2.4, [["", "Positive", "Neutral", "Negative"], ["Positive", "30", "0", "0"], ["Neutral", "0", "29", "1"], ["Negative", "3", "0", "27"]], [1.8, 1.6, 1.6, 1.6], font=15)
card(s, 7.65, 3.4, 5.3, 3.65)
text(s, 7.85, 3.5, 5, 0.4, "Accuracy by company", 13, True, BLUE)
bar_chart(s, 7.75, 3.85, 5.1, 3.1, ["ICICI", "Reliance", "TCS"], [("Accuracy", (93.33, 96.67, 96.67))], [BLUE], '0.0"%"')
notes(s, "We benchmarked FinBERT against 90 human labelled sentences: accuracy 95.56 percent, macro F1 0.9555 and Cohen's kappa 0.9333. The four misses were double-barrelled sentences where a cautious qualifier sat next to a positive number.")

# ---------------------------------------------------------------- 9 Bias
s = slide(9, "Why the Market Misprices Them", "150 headlines classified by behavioural bias", ADITI)
card(s, 0.4, 1.35, 5.6, 5.7)
bar_chart(s, 0.5, 1.45, 5.4, 5.5, ["ICICI\nHype/FOMO", "Reliance\nRecency", "TCS\nLoss aversion"], [("Dominant bias share (%)", (58, 34, 50))], [ORANGE], '0"%"', title="Dominant bias share")
for i, (nm, bias, up, act, col) in enumerate([("ICICI Bank", "Hype / FOMO", "+14.13%", "ACCUMULATE", CO["ICICI"]), ("Reliance", "Recency bias", "+21.91%", "BUY", CO["REL"]), ("TCS", "Loss aversion", "+16.10%", "ACCUMULATE", CO["TCS"])]):
    y = 1.35 + i * 1.92
    card(s, 6.25, y, 6.7, 1.78, col)
    text(s, 6.5, y + 0.1, 3.0, 0.4, nm, 18, True, col)
    text(s, 6.5, y + 0.55, 3.2, 0.4, bias, 14, False, MUTED)
    text(s, 9.5, y + 0.25, 2.0, 0.9, up, 34, True, GREEN)
    chip(s, 11.1, y + 0.4, 1.7, act, GREEN if act == "BUY" else MID, size=11)
notes(s, "Headline framing explains the dislocation: ICICI suffers hype and FOMO, so we accumulate on dips; Reliance suffers recency bias over two weak refining quarters, creating our largest upside of 21.91 percent; TCS suffers loss aversion over AI fears, giving 16.10 percent upside.")

# ---------------------------------------------------------------- 10 Technicals + MC
s = slide(10, "Momentum & Monte Carlo View", "1,000-path GBM, 1-year horizon", ADITI)
card(s, 0.4, 1.35, 8.2, 5.7)
picture(s, IMG / "mc_fan_charts.png", 0.5, 1.45, 8.0, 5.5)
for i, (nm, rsi, mc, col) in enumerate([("ICICI Bank", "RSI 56.97", "MC median ₹1,553 ≈ DDM ₹1,596", CO["ICICI"]), ("Reliance", "RSI 40.27 oversold", "DCF ₹1,420 at 82nd percentile", CO["REL"]), ("TCS", "RSI 67.56", "DCF ₹2,906 between P75 and P90", CO["TCS"])]):
    y = 1.35 + i * 1.92
    card(s, 8.85, y, 4.1, 1.78, col)
    text(s, 9.1, y + 0.08, 3.6, 0.4, nm, 17, True, col)
    text(s, 9.1, y + 0.55, 3.6, 0.5, rsi, 20, True, INK)
    text(s, 9.1, y + 1.2, 3.7, 0.5, mc, 11, False, MUTED)
notes(s, "The Monte Carlo median for ICICI converges to our DDM. Reliance is oversold with a positive MACD crossover and our DCF sits at the 82nd percentile, a mean-reversion setup. TCS's target sits between P75 and P90. I now hand over to Sankarshana.")

# ---------------------------------------------------------------- 11 Returns & tangency
s = slide(11, "Expected Returns & Tangency Portfolio", "Return = 50% CAPM Ke + 50% DCF/DDM implied IRR", SANK)
card(s, 0.4, 1.35, 6.3, 5.7)
bar_chart(s, 0.5, 1.45, 6.1, 5.5, ["ICICI", "Reliance", "TCS", "91D T-Bill"], [("Expected return (%)", (13.99, 15.55, 13.28, 6.65))], [BLUE], '0.00"%"', title="Blended expected return")
ch = s.shapes[-1].chart
for i, c in enumerate([CO["ICICI"], CO["REL"], CO["TCS"], CO["TB"]]):
    pt = ch.plots[0].series[0].points[i]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = rgb(c)
card(s, 6.9, 1.35, 6.05, 3.6)
donut(s, 7.0, 1.4, 5.85, 3.5, ["ICICI", "Reliance", "TCS"], (0.3890, 0.3791, 0.2319), [CO["ICICI"], CO["REL"], CO["TCS"]], title="Max-Sharpe equity mix")
kpi(s, 6.9, 5.15, 1.95, 1.9, "14.42%", "Return", BLUE, 24)
kpi(s, 8.95, 5.15, 1.95, 1.9, "15.74%", "Volatility", ORANGE, 24)
kpi(s, 11.0, 5.15, 1.95, 1.9, "0.4935", "Sharpe (Rf 6.65%)", GREEN, 24)
notes(s, "History punishes Reliance and TCS for cyclical derating, so we blend CAPM cost of equity with DCF implied IRR: 13.99, 15.55 and 13.28 percent, against 6.65 percent for the 91-day T-Bill. The max-Sharpe equity mix is 38.9, 37.9 and 23.2 percent, with 14.42 percent return, 15.74 percent volatility and Sharpe 0.4935.")

# ---------------------------------------------------------------- 12 A=4 case
s = slide(12, "Featured Investor: A = 4.00", "Risk score 30 • Ability 15 • Willingness 15", SANK)
card(s, 0.4, 1.35, 5.4, 4.3)
donut(s, 0.5, 1.4, 5.2, 4.2, ["ICICI", "Reliance", "TCS", "91D T-Bill"], (0.3050, 0.2972, 0.1818, 0.2159), [CO["ICICI"], CO["REL"], CO["TCS"], CO["TB"]], title="Look-through allocation")
kpi(s, 0.4, 5.85, 1.3, 1.2, "78.41%", "Equity y*", BLUE, 17)
kpi(s, 1.75, 5.85, 1.3, 1.2, "21.59%", "T-Bill", GREY, 17)
kpi(s, 3.1, 5.85, 1.3, 1.2, "12.74%", "E(Rc)", GREEN, 17)
kpi(s, 4.45, 5.85, 1.35, 1.2, "12.34%", "Vol σ", ORANGE, 17)
card(s, 6.05, 1.35, 6.9, 3.6)
text(s, 6.25, 1.42, 6.5, 0.4, "Where the money goes", 14, True, BLUE)
table(s, 6.25, 1.85, 6.5, 2.95, [["Asset", "Weight", "₹10 L lump sum", "₹25k SIP / mo"], ["ICICI Bank", "30.50%", "₹3,05,000", "₹7,625"], ["Reliance", "29.72%", "₹2,97,200", "₹7,430"], ["TCS", "18.18%", "₹1,81,800", "₹4,545"], ["91D T-Bill", "21.59%", "₹2,15,900", "₹5,398"]], [1.7, 1.3, 1.9, 1.6], font=13)
text(s, 6.05, 5.15, 6.9, 0.35, "Prudence rule: if |Sec A − Sec B| ≥ 6, use 2 × the lower score", 13, True, ORANGE)
for i, (v, l) in enumerate([("0.4935", "Sharpe"), ("0.0786", "Treynor"), ("+1.45%", "Jensen α"), ("0.0970", "Utility")]):
    kpi(s, 6.05 + i * 1.74, 5.6, 1.64, 1.45, v, l, GREEN if i < 3 else BLUE, 20)
notes(s, "At A equals 4 the optimal split is 78.41 percent equity and 21.59 percent in the T-Bill. That is 30.5 percent ICICI, 29.72 Reliance, 18.18 TCS. For ten lakh rupees: 3.05 lakh, 2.97 lakh, 1.82 lakh and 2.16 lakh in T-Bills; for a 25,000 monthly SIP: 7,625, 7,430, 4,545 and 5,398. Expected return 12.74 percent at 12.34 percent volatility. The prudence rule overrides when ability and willingness differ by six points or more.")

# ---------------------------------------------------------------- 13 SIP
s = slide(13, "20-Year Step-Up SIP Glide Path", "₹25,000 / month • +10% annual step-up", SANK)
card(s, 0.4, 1.35, 8.2, 4.3)
picture(s, IMG / "sip_glide_path.png", 0.5, 1.45, 8.0, 4.1)
for i, (ph, yrs, mix, col) in enumerate([("Accumulate", "Years 1–8", "100% equity", BLUE), ("Consolidate", "Years 9–15", "64% equity • 36% T-Bill", MID), ("Preserve", "Years 16–20", "37% equity • 63% T-Bill", GREY)]):
    x = 0.4 + i * 2.75
    rect(s, x, 5.8, 2.65, 1.25, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x + 0.1, 5.85, 2.45, 0.4, ph, 16, True, WHITE)
    text(s, x + 0.1, 6.25, 2.45, 0.35, yrs, 12, False, WHITE)
    text(s, x + 0.1, 6.57, 2.45, 0.4, mix, 12, True, WHITE)
kpi(s, 8.85, 1.35, 4.1, 1.35, "₹1.72 Cr", "Total invested", GREY, 30)
kpi(s, 8.85, 2.85, 4.1, 1.35, "₹4.32 Cr", "Expected corpus (2.52x)", GREEN, 30)
kpi(s, 8.85, 4.35, 4.1, 1.35, "₹4.20 Cr", "Monte Carlo median", BLUE, 30)
kpi(s, 8.85, 5.85, 4.1, 1.2, "₹3.18 – 5.74 Cr", "P10 to P90 range", TEAL, 24)
notes(s, "A 25,000 rupee monthly SIP with a 10 percent annual step-up invests 1.72 crore over 20 years and compounds to 4.32 crore. The glide path moves from 100 percent equity to 63 percent in T-Bills in the last five years to lock in gains. The Monte Carlo median is 4.20 crore with a 3.18 to 5.74 crore range.")

# ---------------------------------------------------------------- 14 Evaluation
s = slide(14, "4-Metric Evaluation vs Nifty 50", "Sharpe • Treynor • Jensen's alpha • Information ratio", SANK)
card(s, 0.4, 1.35, 7.0, 3.3)
table(s, 0.55, 1.45, 6.7, 3.1, [["Portfolio", "Sharpe", "Treynor", "Alpha", "IR"], ["Tangency", "0.4935", "0.0786", "+1.84%", "+0.227"], ["A = 4.00", "0.4935", "0.0786", "+1.45%", "+0.014"], ["Balanced", "0.4935", "0.0786", "+1.18%", "+0.117"], ["Defensive", "0.4940", "0.0786", "+0.68%", "+0.006"], ["Nifty 50", "0.4328", "0.0600", "—", "—"]], [1.7, 1.2, 1.2, 1.3, 1.3], hl_row=2, font=13)
card(s, 7.6, 1.35, 5.35, 5.7)
picture(s, IMG / "backtest_performance.png", 7.65, 1.45, 5.25, 5.5)
kpi(s, 0.4, 4.85, 3.4, 2.2, "Same Sharpe", "Every mix lies on the Capital Allocation Line (Tobin separation)", BLUE, 24)
kpi(s, 4.0, 4.85, 3.4, 2.2, "T-Bills cut risk", "Defensive mix: ₹131.88 on ₹100 with a 63% T-Bill cushion", GREY, 24)
notes(s, "All four mandatory ratios beat the Nifty 50. Sharpe and Treynor are the same along the capital allocation line because excess return and volatility both scale with y star, whereas the information ratio differs because it benchmarks against a fully invested index. T-Bill heavy baskets cushioned the Reliance and TCS derating in the five-year backtest.")

# ---------------------------------------------------------------- 15 Verdict
s = slide(15, "Final Verdict", "Triangulated: valuation + AI sentiment + portfolio", SANK)
cards = [("Reliance", "BUY", "+21.91%", "29.72%", CO["REL"], GREEN), ("ICICI Bank", "ACCUMULATE", "+14.13%", "30.50%", CO["ICICI"], MID),
         ("TCS", "ACCUMULATE", "+16.10%", "18.18%", CO["TCS"], MID), ("91D T-Bill", "ANCHOR", "6.65%", "21.59%", CO["TB"], GREY)]
for i, (nm, rec, up, w, col, rc) in enumerate(cards):
    x = 0.4 + i * 3.15
    rect(s, x, 1.4, 3.0, 3.5, CARD, "E2E8F0", MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s, x, 1.4, 3.0, 0.15, col)
    text(s, x, 1.65, 3.0, 0.5, nm, 20, True, col, PP_ALIGN.CENTER)
    chip(s, x + 0.45, 2.25, 2.1, rec, rc, size=13, h=0.45)
    text(s, x, 2.85, 3.0, 0.9, up, 38, True, GREEN if "+" in up else INK, PP_ALIGN.CENTER)
    text(s, x, 3.6, 3.0, 0.35, "upside" if "+" in up else "risk-free yield", 12, False, MUTED, PP_ALIGN.CENTER)
    text(s, x, 4.1, 3.0, 0.6, f"{w} of A=4.00 portfolio", 13, True, INK, PP_ALIGN.CENTER)
card(s, 0.4, 5.15, 6.2, 1.9)
text(s, 0.6, 5.22, 5.8, 0.4, "Live offline dashboard • 9 blocks", 15, True, BLUE)
text(s, 0.6, 5.65, 5.8, 1.3, ["py -m streamlit run 05_dashboard/app.py", "Risk-aversion slider • ₹ lump sum & SIP"], 13, False, MUTED)
card(s, 6.8, 5.15, 6.15, 1.9)
text(s, 7.0, 5.22, 5.8, 0.4, "Limitations", 15, True, ORANGE)
text(s, 7.0, 5.65, 5.8, 1.3, ["Double-barrelled sentences fool FinBERT (4 / 90)", "GBM has constant volatility", "5-year betas & covariance are static"], 13, False, MUTED)
notes(s, "To conclude: Reliance is our contrarian BUY, ICICI and TCS are ACCUMULATE, and the 91-day T-Bill anchors the portfolio, 21.59 percent at A equals 4. Limitations are FinBERT on double-barrelled sentences, constant-volatility GBM and static betas. All nine modules run live in our offline dashboard. Thank you; we welcome your questions.")

# ---------------------------------------------------------------- 16 Viva appendix
s = slide(16, "Appendix: Viva Quick Answers", "Six likely questions • one line each", "All")
qa = [("Why DDM for ICICI?", "Deposits are operating inventory, so FCFF/WACC is meaningless for a bank."),
      ("TCS return is negative, upside +16%?", "P/E fell ~32x → 18.4x while profit grew; reverse DCF prices only 5.13% growth."),
      ("How is AI hallucination ruled out?", "Verbatim verifier: 12/12 quotes at similarity 1.0000."),
      ("Why 4 FinBERT misses?", "Cautious qualifier next to a positive number (double-barrelled)."),
      ("6.85% vs 6.65% risk-free?", "10Y G-Sec matches long DCF duration; 91D T-Bill is the zero-duration portfolio asset."),
      ("Why identical Sharpe across baskets?", "All lie on the CAL; return and volatility scale together with y*.")]
for i, (q, a) in enumerate(qa):
    x, y = 0.4 + (i % 2) * 6.35, 1.4 + (i // 2) * 1.85
    card(s, x, y, 6.2, 1.7, [BLUE, TEAL, MID][i // 2])
    text(s, x + 0.25, y + 0.1, 5.8, 0.45, q, 16, True, INK)
    text(s, x + 0.25, y + 0.6, 5.8, 1.0, a, 13, False, MUTED)
notes(s, "Reference slide for viva questions.")

out = ROOT / "06_deliverables" / "Presentation_Deck_15_Slides.pptx"
prs.save(str(out))
shutil.copy2(out, ROOT / "06_deliverables" / "SA_final_presentation.pptx")
print("Saved", out, "slides:", len(prs.slides))
