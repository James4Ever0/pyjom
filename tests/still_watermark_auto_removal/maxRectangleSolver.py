import sympy
import json

data = json.loads(open("test_special.json",'r').read())
canvas = data['canvas']
rectangles = data['rectangles']

width, height = canvas

xValid = [0, width]
yValid = [0, height]

mRects = []

def checkContains(rect, point):
    xPoints = []

def checkOverlapAsymmetric(rect0, rect1):
    for point in rect0:
        if checkContains(rect1, point):
            return True
    return False

def checkOverlap(rect0, rect1):
    if checkOverlapAsymmetric(rect0, rect1): return True
    if checkOverlapAsymmetric(rect1, rect0): return True
    return False


for x,y, mWidth, mHeight in rectangles:
    xValid.append(x)
    xValid.append(x+mWidth)
    yValid.append(y)
    yValid.append(y+mHeight)
    p0, p1, p2, p3 = (x,y), (x+mWidth,y),(x+mWidth, y+mHeight), (x, y+mHeight)
    # mRectangle = sympy.Polygon(p0,p1,p2,p3)
    mRectangle = [p0,p1,p2,p3]
    mRects.append(mRectangle)