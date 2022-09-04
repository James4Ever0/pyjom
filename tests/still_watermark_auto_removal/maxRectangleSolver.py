import sympy
import json

data = json.loads(open("test_special.json",'r').read())
canvas = data['canvas']
rectangles = data['rectangles']

width, height = canvas

