import sympy
import json

data = json.loads(open("test_special.json",'r').read())
canvas = data['canvas']
rectangles = data['rectangles']



width, height = canvas

xValid = [0, width]
yValid = [0, height]

for x,y, mWidth, mHeight in rectangles:
    xValid.append(x)
    xValid.append(x+mWidth)
    yValid.append(y)
    yValid.append(y+mHeight)
