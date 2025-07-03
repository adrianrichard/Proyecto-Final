from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def transformations():
    # Setting transformations apply to canvas and effects all added after, so use saveState and restoreState.
    c = canvas.Canvas("translate_rotate_scale.pdf", pagesize=A4)  # 595 x 842 is the page dimensions for A4 at 72DPI
    logo = 'reportlab.png'
    c.setFont("Helvetica", 20, leading=None)

    # Translate
    c.saveState()
    c.drawString(x=30, y=780, text="Translate")
    c.drawInlineImage(image=logo, x=100, y=700, width=50, height=50)
    c.translate(dx=55, dy=0)  # Adding transformation so you can see the underlying image
    c.drawInlineImage(image=logo, x=100, y=700, width=50, height=50)
    c.restoreState()

    # Rotate
    c.drawString(x=30, y=580, text="Rotate")
    c.drawInlineImage(image=logo, x=100, y=500, width=50, height=50)
    c.saveState()
    c.translate(dx=100, dy=500)
    c.rotate(-90)  # Rotates whole canvas, so translate to make dx, dy the new 0,0
    c.translate(dx=-100, dy=-500)
    c.drawInlineImage(image=logo, x=100, y=500, width=50, height=50)
    c.restoreState()

    # Scale
    c.saveState()
    c.drawString(x=30, y=380, text="Scale")
    c.drawInlineImage(image=logo, x=100, y=180, width=50, height=50)
    c.scale(1.5, 1.5)
    c.drawInlineImage(image=logo, x=100, y=180, width=50, height=50)
    c.restoreState()

    c.showPage()
    c.save()


transformations()
