from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.flowables import DocPara, DocAssign, DocExec, DocIf, DocWhile

styles = getSampleStyleSheet()


def programmable_flowables():
    doc = SimpleDocTemplate("programmable_flowables.pdf")
    instructions = [
        DocAssign('i',3),
        DocExec('i-=1'),
        DocPara('i', format='The value of i is %(__expr__)d', style=styles['Normal']),
        DocIf(
            cond='i<2',
            thenBlock=Paragraph('The value of i is greater than 2'),
            elseBlock=Paragraph('The value of i is less than or equal to 2'),
        ),
        DocWhile(
            cond='i',
            whileBlock=[
                DocPara(expr='i', format='The value of i is %(__expr__)d'),
                DocExec(stmt='i-=1'),
            ],
        )
    ]
    Story = [Spacer(1, 72)]
    for instruction in instructions:
        Story.append(instruction)
    doc.build(Story)


programmable_flowables()
