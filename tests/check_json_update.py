from test_commons import *
from pyjom.commons import jsonUpdate

mdict = {"a": [1, 2, 3, {"b": [4, 5]}]}
print("ORIGINAL:", mdict)
jsonUpdate(mdict, ["a", 3, "b", 0], 2)
print("RESULT:", mdict)
