def makePDF(stringList):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 11)
    for string in stringList:
        pdf.cell(40, 10, string + '.')
    pdf.output('law--less.pdf', 'F')
