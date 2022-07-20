from test_commons import *
from pyjom.medialang.core import *
import os

testpaths = [
    "processor_demo.mdl",
    "processor_multi.mdl",
    "recipe.mdl",
    "audiolang.mdl",
    "videolang.mdl",
]

# testcontent = open(testpath,"r").read()

for path in testpaths:
    testpath = os.path.join("/root/Desktop/works/pyjom/test/", path)
    mdl = Medialang(script_path=testpath)  # will be parsed.
    mdl.prettify(inplace=True)
