from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


def first_page():
	c = canvas.Canvas("hello-world.pdf", pagesize=A4)
	width, height = A4
	c.saveState()
	c.setFont('Times-Bold',16)
	c.drawCentredString(width/2.0, height-108, "Hello world Heading")
	c.setFont('Times-Roman',12)
	c.drawString(100, 700, "Hello World Text")
	c.restoreState()
	c.showPage()
	c.save()


first_page()
