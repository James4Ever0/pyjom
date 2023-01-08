from test_commons import *

from pyjom.modules.contentCensoring.core import censorInterface

mcounter = 20
mtags0 = ["superLongtag{}".format(x) for x in range(mcounter)]  # must be differet.
mtags1 = ["tag{}".format(x) for x in range(mcounter)]

mtags = mtags0 + mtags1
import random

random.shuffle(mtags)

result = censorInterface(
    "title", ["mytopic", "another topic"], "mycontent", mtags=mtags
)

print(result)
