from reportlab.graphics.shapes import ArcPath, SolidShape
from reportlab.graphics.widgetbase import Widget
from reportlab.lib.attrmap import AttrMap, AttrMapValue
from reportlab.lib.validators import isNumber, isColorOrNone, isBoolean, isListOfNumbersOrNone
from reportlab.lib import colors

class VThermometerBar(Widget):
    _attrMap = AttrMap(BASE=SolidShape,
        x = AttrMapValue(isNumber),
        y = AttrMapValue(isNumber),
        width = AttrMapValue(isNumber,desc="width of the object in points"),
        height = AttrMapValue(isNumber,desc="height of the objects in points"),
        fillColor = AttrMapValue(isColorOrNone),
        strokeColor = AttrMapValue(isColorOrNone),
        strokeWidth = AttrMapValue(isNumber),
        strokeDashArray = AttrMapValue(isListOfNumbersOrNone, desc='Dash array of a line.'),
        degreedelta = AttrMapValue(isNumber,desc="degrees to use for the arc interval"),
        )

    def __init__(self, x=0, y=0, width=0, height=0,
            fillColor = colors.red, strokeColor=colors.black, strokeWidth=0.1, strokeDashArray=None,
            degreedelta=5,
            ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fillColor = fillColor
        self.strokeColor =strokeColor 
        self.strokeWidth = strokeWidth
        self.strokeDashArray = strokeDashArray
        self.degreedelta = degreedelta

    def draw(self):
        P = ArcPath()
        P.strokeWidth = self.strokeWidth
        P.strokeColor = self.strokeColor
        P.fillColor = self.fillColor
        P.strokeDashArray = self.strokeDashArray
        x = self.x
        y = self.y
        width = self.width
        height = self.height
        width = abs(width)
        height = abs(height)
        y1 = y + height
        x1 = x + width
        P.moveTo(x,y1)
        rx = width*0.5
        ry = min(height,rx)
        cx = x + rx
        cy = y + ry
        if ry>=height:
            P.addArc(cx,cy,rx,180,0, yradius=ry,reverse=0, degreedelta=self.degreedelta)
        else:
            P.lineTo(x,cy)
            P.addArc(cx,cy,rx,180,0, yradius=ry,reverse=0, degreedelta=self.degreedelta)
        P.lineTo(x1,y1)
        P.closePath()
        return P
