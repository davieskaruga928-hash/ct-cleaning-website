import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT

# Brand colors, matching the website design system.
INK = colors.HexColor("#12203A")
TEAL = colors.HexColor("#1D8A7A")
GREY = colors.HexColor("#6B7583")
LIGHT_BG = colors.HexColor("#EEF1F4")

# Placeholder company details — update these once real business details are available.
COMPANY_NAME = "CT Cleaning Service"
COMPANY_ADDRESS = "[Address placeholder], Nairobi, Kenya"
COMPANY_PHONE = "[Phone placeholder]"
COMPANY_EMAIL = "[Email placeholder]"

# Placeholder payment details — update once real account details are available.
BANK_NAME = "[Bank name placeholder]"
BANK_ACCOUNT_NAME = "[Account name placeholder]"
BANK_ACCOUNT_NUMBER = "[Account number placeholder]"
BANK_BRANCH = "[Branch placeholder]"
MPESA_PAYBILL = "[Paybill number placeholder]"
MPESA_ACCOUNT = "[Account/Till reference placeholder]"


def generate_quotation_pdf(quotation) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CompanyName", fontSize=18, leading=22, textColor=INK, fontName="Helvetica-Bold", spaceAfter=2))
    styles.add(ParagraphStyle(name="SmallGrey", fontSize=9, textColor=GREY, leading=13))
    styles.add(ParagraphStyle(name="QuoteTitle", fontSize=14, textColor=TEAL, fontName="Helvetica-Bold", alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name="RightSmall", fontSize=9, textColor=GREY, alignment=TA_RIGHT, leading=13))
    styles.add(ParagraphStyle(name="SectionLabel", fontSize=9, textColor=GREY, fontName="Helvetica-Bold", spaceAfter=4))
    styles.add(ParagraphStyle(name="Body", fontSize=10, textColor=INK, leading=14))
    styles.add(ParagraphStyle(name="NotesBody", fontSize=9, textColor=GREY, leading=13))
    styles.add(ParagraphStyle(name="PayLabel", fontSize=9, textColor=TEAL, fontName="Helvetica-Bold", leading=14))
    styles.add(ParagraphStyle(name="PayValue", fontSize=9.5, textColor=INK, leading=14))

    elements = []

    # Header: company info left, quotation title/number right
    header_data = [[
        Paragraph(f'<b>{COMPANY_NAME}</b>', styles["CompanyName"]),
        Paragraph("QUOTATION", styles["QuoteTitle"]),
    ], [
        Paragraph(f'{COMPANY_ADDRESS}<br/>{COMPANY_PHONE} &nbsp;|&nbsp; {COMPANY_EMAIL}', styles["SmallGrey"]),
        Paragraph(
            f'No: <b>{quotation.quotation_number}</b><br/>Date: {quotation.date_issued.strftime("%d %b %Y")}'
            + (f'<br/>Valid until: {quotation.valid_until.strftime("%d %b %Y")}' if quotation.valid_until else ""),
            styles["RightSmall"],
        ),
    ]]
    header_table = Table(header_data, colWidths=[100 * mm, 70 * mm])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 2),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 4))
    elements.append(Table([[""]], colWidths=[170 * mm], style=TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 1.2, TEAL),
    ])))
    elements.append(Spacer(1, 14))

    # Client info block
    client_lines = f"<b>{quotation.client_name}</b><br/>"
    if quotation.client_org:
        client_lines += f"{quotation.client_org}<br/>"
    client_lines += f"{quotation.client_location}<br/>{quotation.client_phone}"
    if quotation.client_email:
        client_lines += f"<br/>{quotation.client_email}"

    elements.append(Paragraph("QUOTE FOR", styles["SectionLabel"]))
    elements.append(Paragraph(client_lines, styles["Body"]))
    elements.append(Spacer(1, 18))

    # Line items table
    table_data = [["Description", "Qty", "Unit Price (KES)", "Subtotal (KES)"]]
    total = 0.0
    for item in quotation.items:
        subtotal = item.quantity * item.unit_price
        total += subtotal
        table_data.append([
            item.description,
            f"{item.quantity:g}",
            f"{item.unit_price:,.2f}",
            f"{subtotal:,.2f}",
        ])
    table_data.append(["", "", "Total", f"{total:,.2f}"])

    items_table = Table(table_data, colWidths=[85 * mm, 20 * mm, 35 * mm, 35 * mm])
    items_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, LIGHT_BG]),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, INK),
        ("LINEABOVE", (0, -1), (-1, -1), 1, INK),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 20))

    if quotation.notes:
        elements.append(Paragraph("NOTES", styles["SectionLabel"]))
        elements.append(Paragraph(quotation.notes.replace("\n", "<br/>"), styles["NotesBody"]))
        elements.append(Spacer(1, 14))

    # Payment details: bank and M-Pesa, side by side in a bordered block
    elements.append(Paragraph("PAYMENT DETAILS", styles["SectionLabel"]))

    def field(label, value):
        return f'<font color="#1D8A7A"><b>{label}:</b></font> {value}'

    bank_block = Paragraph(
        "<b>Bank Transfer</b><br/>"
        + field("Bank", BANK_NAME) + "<br/>"
        + field("Account name", BANK_ACCOUNT_NAME) + "<br/>"
        + field("Account no.", BANK_ACCOUNT_NUMBER) + "<br/>"
        + field("Branch", BANK_BRANCH),
        styles["PayValue"],
    )
    mpesa_block = Paragraph(
        "<b>M-Pesa</b><br/>"
        + field("Paybill", MPESA_PAYBILL) + "<br/>"
        + field("Account/Reference", MPESA_ACCOUNT),
        styles["PayValue"],
    )

    payment_table = Table([[bank_block, mpesa_block]], colWidths=[85 * mm, 85 * mm])
    payment_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#DCE1E6")),
        ("INNERGRID", (0, 0), (-1, -1), 0.75, colors.HexColor("#DCE1E6")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    elements.append(payment_table)
    elements.append(Spacer(1, 18))

    elements.append(Paragraph(
        "Thank you for considering CT Cleaning Service. This quotation is an estimate; "
        "final pricing may be confirmed after an on-site assessment where applicable.",
        styles["NotesBody"],
    ))

    doc.build(elements)
    return buffer.getvalue()
