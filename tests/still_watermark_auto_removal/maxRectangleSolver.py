import sympy
import json

data = json.loads(open("test_special.json", "r").read())
canvas = data["canvas"]
rectangles = data["rectangles"]

canvaswidth, canvasheight = canvas

xValid = [0, canvaswidth]
yValid = [0, canvasheight]

mRects = []


def checkContains(rect, point):
    xPoints = [p[0] for p in rect]
    yPoints = [p[1] for p in rect]
    maxX, minX = max(xPoints), min(xPoints)
    maxY, minY = max(yPoints), min(yPoints)
    x, y = point
    return x > minX and x < maxX and y > minY and y < maxY


def checkOverlapAsymmetric(rect0, rect1):
    for point in rect0:
        if checkContains(rect1, point):
            return True
    return False


def checkOverlap(rect0, rect1):
    if checkOverlapAsymmetric(rect0, rect1):
        return True
    if checkOverlapAsymmetric(rect1, rect0):
        return True
    return False


for x, y, mWidth, mHeight in rectangles:
    xValid.append(x)
    xValid.append(x + mWidth)
    yValid.append(y)
    yValid.append(y + mHeight)
    p0, p1, p2, p3 = (
        (x, y),
        (x + mWidth, y),
        (x + mWidth, y + mHeight),
        (x, y + mHeight),
    )
    # mRectangle = sympy.Polygon(p0,p1,p2,p3)
    mRectangle = [p0, p1, p2, p3]
    mRects.append(mRectangle)


def purify(xValid):
    xValid = list(set(xValid))
    xValid.sort()
    return xValid


def checkOverlapAgainstRectList(rect, rectList):
    for testRect in rectList:
        if checkOverlap(rect, testRect):
            return True
    return False


xValid = purify(xValid)
yValid = purify(yValid)
totalCandidates = []


def getRectArea(rect):
    xPoints = [p[0] for p in rect]
    yPoints = [p[1] for p in rect]
    maxX, minX = max(xPoints), min(xPoints)
    maxY, minY = max(yPoints), min(yPoints)
    return (maxX - minX) * (maxY - minY)


bestCandidate = None
bestArea = 0
for ix0 in range(0, len(xValid)):
    for ix1 in range(ix0, len(xValid)):
        for iy0 in range(0, len(yValid)):
            for iy1 in range(iy0, len(yValid)):
                x0, x1, y0, y1 = xValid[ix0], xValid[ix1], yValid[iy0], yValid[iy1]
                x, y = x0, y0
                mWidth, mHeight = x1 - x, y1 - y
                p0, p1, p2, p3 = (
                    (x, y),
                    (x + mWidth, y),
                    (x + mWidth, y + mHeight),
                    (x, y + mHeight),
                )
                rectCandidate = [p0, p1, p2, p3]
                area = getRectArea(rectCandidate)
                if area <= bestArea:
                    continue
                if checkOverlapAgainstRectList(rectCandidate, mRects):
                    break
                bestCandidate = rectCandidate.copy()
                bestArea = area
                # print("UPDATING:",bestCandidate)
                # print('AREA:', bestArea)
                # totalCandidates.append(rectCandidate.copy())

print("final candidate:", bestCandidate)
# plot this?
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, ax = plt.subplots()

# add rectangle to plot
def plotRect(ax, x, y, width, height, facecolor):
    ax.add_patch(Rectangle((x, y), width, height, facecolor=facecolor, fill=True))


def rectToXYWH(rect):
    xPoints = [p[0] for p in rect]
    yPoints = [p[1] for p in rect]
    maxX, minX = max(xPoints), min(xPoints)
    maxY, minY = max(yPoints), min(yPoints)
    x, y = minX, minY
    width, height = (maxX - minX), (maxY - minY)
    return x, y, width, height


# display plot
plt.show()
# totalCandidates.sort(key = lambda rect: -getRectArea(rect))
# for rect in totalCandidates[:5]:
#     print(rect)
