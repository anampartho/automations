def generate_invoice():
    print("generating invoice...")

    # Import reportlab
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.units import cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from reportlab.lib import colors

    file_path = 'invoice.pdf'

    doc = SimpleDocTemplate(
        file_path,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm
    )

    story = []

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Right',
        alignment=TA_RIGHT
    ))
    styles.add(ParagraphStyle(
        name='Sub_Total',
        alignment=TA_RIGHT, spaceBefore=20
    ))
    styles.add(ParagraphStyle(
        name='Page_Title',
        font='Helvetica-Bold',
        fontSize=20,
        alignment=TA_RIGHT,
        spaceBefore=20,
        spaceAfter=20
    ))

    story.append(Paragraph("NAME"))
    story.append(Paragraph("personal address"))
    story.append(Paragraph("INVOICE", styles["Page_Title"]))

    table = Table(
        [
            [
                Paragraph("<strong>Bill To:</strong><br /> Company Details"),
                Paragraph(
                    "Invoice #INV-NUMBER<br /> Invoice Date May 16, 2024<br /> Due Date May 31, 2024"
                )
            ]
        ],
        colWidths=(9 * cm)
    )

    table2 = Table(
        [
            [
                Paragraph("Description"),
                Paragraph("Days"),
                Paragraph("Monthly Salary"),
                Paragraph("Subtotal")
            ],
            [
                Paragraph(
                    "No. of working days for Software Engineering Services"),
                Paragraph("N"),
                Paragraph("X"),
                Paragraph("X USD")
            ]
        ],
        colWidths=(4.5 * cm),
        spaceBefore=20
    )

    table2.setStyle(TableStyle(
        [
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]
    ))

    story.append(table)
    story.append(table2)
    story.append(Paragraph("Total Amount: X USD",  styles["Sub_Total"]))

    doc.build(story)

    print("Invoice generated...")
