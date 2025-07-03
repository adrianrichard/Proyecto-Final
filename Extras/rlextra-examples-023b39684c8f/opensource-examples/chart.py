from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Drawing
from reportlab.platypus.doctemplate import SimpleDocTemplate


def chart():
    """Create a chart"""
    doc = SimpleDocTemplate('chart.pdf')
    elements = []

    d1 = Drawing(400, 200)
    pc = Pie()
    pc.x, pc.y = 20, 20
    pc.data = [10, 20, 30, 40, 50, 60]
    pc.labels = ['a', 'b', 'c', 'd', 'e', 'f']
    d1.add(pc, 'PieChart')
    elements.append(d1)

    d2 = Drawing(400, 200)
    lp = LinePlot()
    lp.x, lp.y = 20, 20
    d2.add(lp, 'linePlot')
    elements.append(d2)

    d3 = Drawing(400, 200)
    vbc = VerticalBarChart()
    vbc.x, vbc.y = 20, 20
    vbc.categoryAxis.categoryNames = ['Jan', 'Feb', 'Mar', 'Apr']
    d3.add(vbc, 'VerticalBarChart')
    elements.append(d3)

    doc.build(elements)


chart()
