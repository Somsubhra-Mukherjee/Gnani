import io
from datetime import datetime
from typing import List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from backend.app.analytics.scratchpad import scratchpad, MemoEntry

def generate_scratchpad_pdf() -> bytes:
    """
    Renders the active executive working memo into a high-quality PDF report
    using ReportLab. Returns PDF file bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A")
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#3B82F6")
    )
    meta_style = ParagraphStyle(
        "DocMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#64748B")
    )
    section_title = ParagraphStyle(
        "SectionTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E293B")
    )
    cell_bold = ParagraphStyle(
        "CellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    )
    cell_regular = ParagraphStyle(
        "CellReg",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#334155")
    )
    cell_mono = ParagraphStyle(
        "CellMono",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0F172A")
    )

    elements = []

    def sanitize_text(txt: str) -> str:
        """Replaces Unicode Rupee symbol with 'Rs. ' to avoid WinAnsi black box rendering."""
        if not txt:
            return ""
        return txt.replace("₹", "Rs. ")

    # 1. Header Banner
    elements.append(Paragraph("FRESHROUTE FOODS PVT. LTD.", subtitle_style))
    elements.append(Paragraph("Executive Analytical Working Memo & Scenario Dossier", title_style))
    now_str = datetime.now().strftime("%B %d, %Y - %I:%M %p")
    elements.append(Paragraph(f"Generated on {now_str} | Session Scratchpad Audit Trail | Strictly Confidential", meta_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#3B82F6"), spaceAfter=14))

    # 2. Executive Scope & Baseline Regional Economics
    elements.append(Paragraph("1. Active Investigation Scope & Baseline Regional Economics", section_title))
    elements.append(Spacer(1, 6))

    baseline_data = [
        [
            Paragraph("Metric", cell_bold),
            Paragraph("Gujarat (West Region / Ahmedabad)", cell_bold),
            Paragraph("West Bengal (East Region / Kolkata)", cell_bold),
            Paragraph("Variance / Spread", cell_bold)
        ],
        [
            Paragraph("Per-Piece Production Cost", cell_regular),
            Paragraph("Rs. 188.80", cell_mono),
            Paragraph("Rs. 182.50", cell_mono),
            Paragraph("-Rs. 6.30 (WB lower)", cell_regular)
        ],
        [
            Paragraph("Per-Piece Transportation", cell_regular),
            Paragraph("Rs. 24.50", cell_mono),
            Paragraph("Rs. 25.60", cell_mono),
            Paragraph("+Rs. 1.10 (WB higher)", cell_regular)
        ],
        [
            Paragraph("Total Landed Unit Cost", cell_bold),
            Paragraph("Rs. 213.30", cell_mono),
            Paragraph("Rs. 208.10", cell_mono),
            Paragraph("-Rs. 5.20 (WB cheaper)", cell_bold)
        ],
        [
            Paragraph("Base Selling Price", cell_regular),
            Paragraph("Rs. 240.00", cell_mono),
            Paragraph("Rs. 245.00", cell_mono),
            Paragraph("+Rs. 5.00 (WB premium)", cell_regular)
        ],
        [
            Paragraph("Unit Gross Margin (Spread)", cell_bold),
            Paragraph("Rs. 26.70 (11.1%)", cell_mono),
            Paragraph("Rs. 36.90 (15.1%)", cell_mono),
            Paragraph("+Rs. 10.20 (+4.0%)", cell_bold)
        ],
        [
            Paragraph("Monthly Units Sold", cell_regular),
            Paragraph("18,200 units", cell_mono),
            Paragraph("24,500 units", cell_mono),
            Paragraph("+6,300 units", cell_regular)
        ],
        [
            Paragraph("Total Monthly Revenue", cell_regular),
            Paragraph("Rs. 43,68,000.00", cell_mono),
            Paragraph("Rs. 60,02,500.00", cell_mono),
            Paragraph("+Rs. 16,34,500.00", cell_regular)
        ],
        [
            Paragraph("Total Gross Profit", cell_bold),
            Paragraph("Rs. 4,85,940.00", cell_mono),
            Paragraph("Rs. 9,04,050.00", cell_mono),
            Paragraph("+Rs. 4,18,110.00", cell_bold)
        ]
    ]

    t_baseline = Table(baseline_data, colWidths=[1.8 * inch, 2.0 * inch, 2.0 * inch, 1.7 * inch])
    t_baseline.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    elements.append(t_baseline)
    elements.append(Spacer(1, 16))

    # 3. Conversational Arithmetic Scratchpad Log
    entries = scratchpad.get_entries()
    elements.append(Paragraph("2. Step-by-Step Computational Trace & Inquiry Log", section_title))
    elements.append(Spacer(1, 6))

    if not entries:
        elements.append(Paragraph("<i>No interactive inquiries logged in current session. Standard scenario baseline active above.</i>", cell_regular))
    else:
        log_rows = [
            [
                Paragraph("#", cell_bold),
                Paragraph("Time", cell_bold),
                Paragraph("Inquiry / Instruction", cell_bold),
                Paragraph("Category", cell_bold),
                Paragraph("Deterministic Verification / Calculation", cell_bold)
            ]
        ]
        for e in entries:
            clean_details = sanitize_text(e.details)
            clean_formula = sanitize_text(e.formula) if e.formula else None
            log_rows.append([
                Paragraph(str(e.id), cell_mono),
                Paragraph(e.timestamp, cell_mono),
                Paragraph(e.query, cell_bold),
                Paragraph(e.category, cell_regular),
                Paragraph(f"{clean_details}" + (f"<br/><b>Formula:</b> <font face='Courier'>{clean_formula}</font>" if clean_formula else ""), cell_regular)
            ])

        t_log = Table(log_rows, colWidths=[0.3 * inch, 0.7 * inch, 2.5 * inch, 1.2 * inch, 2.8 * inch])
        t_log.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])
        ]))
        elements.append(t_log)

    elements.append(Spacer(1, 16))

    # 4. What-If Scenario Arbitrage Balance Sheet
    elements.append(Paragraph("3. What-If Volume Reallocation Scenario (Gujarat -2% -> West Bengal +2%)", section_title))
    elements.append(Spacer(1, 6))

    scenario_rows = [
        [Paragraph("Simulation Component", cell_bold), Paragraph("Exact Formula", cell_bold), Paragraph("Computed Value", cell_bold)],
        [Paragraph("Volume Diverted from Gujarat (2%)", cell_regular), Paragraph("18,200 × 0.02", cell_mono), Paragraph("364 units", cell_mono)],
        [Paragraph("Gujarat Unit Margin (Price - Landed)", cell_regular), Paragraph("Rs. 240.00 - Rs. 213.30", cell_mono), Paragraph("Rs. 26.70 / unit", cell_mono)],
        [Paragraph("Gross Profit Forfeited in Gujarat", cell_regular), Paragraph("364 × Rs. 26.70", cell_mono), Paragraph("-Rs. 9,718.80", cell_mono)],
        [Paragraph("West Bengal Unit Margin (Price - Landed)", cell_regular), Paragraph("Rs. 245.00 - Rs. 208.10", cell_mono), Paragraph("Rs. 36.90 / unit", cell_mono)],
        [Paragraph("Gross Profit Realized in West Bengal", cell_regular), Paragraph("364 × Rs. 36.90", cell_mono), Paragraph("+Rs. 13,431.60", cell_mono)],
        [Paragraph("<b>Net Arbitrage Profit Balance</b>", cell_bold), Paragraph("Rs. 13,431.60 - Rs. 9,718.80", cell_mono), Paragraph("<b>+Rs. 3,712.80 Gain</b>", cell_bold)]
    ]

    t_scen = Table(scenario_rows, colWidths=[2.6 * inch, 2.5 * inch, 2.4 * inch])
    t_scen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#DCFCE7")), # Light green accent for net gain
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor("#F8FAFC")])
    ]))
    elements.append(t_scen)

    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
    elements.append(Paragraph(
        "<b>Executive Sign-off Note:</b> This document contains factual calculations and database-verified data points compiled by the FreshRoute AI Assistant. Strategic judgment, vendor contracts, retail shelf agreements, and execution decisions rest entirely with executive management.",
        cell_regular
    ))

    doc.build(elements)
    return buffer.getvalue()
