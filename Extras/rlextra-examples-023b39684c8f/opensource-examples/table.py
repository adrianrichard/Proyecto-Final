from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus.tables import TableStyle, Table

TABLE_DATA = [
    ['00', '01', '02', '03', '04'],
    ['10', '11', '12', '13', '14'],
    ['20', '21', '22', '23', '24'],
    ['30', '31', '32', '33', '34']]


def table(canvas):
    """Create a demo table"""
    # The line's use a thickness specified in their respective styles.
    # (0,0) represents the top left cell. (-1,-1) represents the last cell
    LIST_STYLE = TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.green),
        ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 2, colors.green),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT')])

    LIST_STYLE1 = TableStyle(LIST_STYLE.getCommands())
    LIST_STYLE1.add('BOX', (0, 0), (1, -1), 2, colors.red)  # Add style after styles have already been declared
    t1 = Table(TABLE_DATA, style=LIST_STYLE1)
    t1.wrapOn(canvas, 100, 100)
    t1.drawOn(canvas, x=50, y=700)

    LIST_STYLE2 = TableStyle(LIST_STYLE.getCommands())
    LIST_STYLE2.add('BACKGROUND', (0, 0), (-1, 0), colors.Color(0, 0.7, 0.7))  # Blue background, colour manually declared
    t2 = Table(TABLE_DATA, style=LIST_STYLE2)
    t2.wrapOn(canvas, 100, 100)
    t2.drawOn(canvas, x=50, y=500)

    LIST_STYLE3 = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (1, 1), colors.palegreen),
        ('BACKGROUND', (-2, -2), (-1, -1), colors.pink),
        ('SPAN', (0, 0), (1, 1)),
        ('SPAN', (-2, -2), (-1, -1))])
    t3 = Table(TABLE_DATA, style=LIST_STYLE3)
    t3.wrapOn(canvas, 100, 100)
    t3.drawOn(canvas, x=50, y=300)


def go():
    c = canvas.Canvas("table.pdf", pagesize=A4) # 595 x 842 is the page dimensions for A4 at 72DPI
    table(canvas=c)
    c.showPage()
    c.save()


go()
