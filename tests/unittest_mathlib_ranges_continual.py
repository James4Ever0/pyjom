from test_commons import *
from pyjom.mathlib import *

inputList = [[(0, 1), (1, 1.1), (2, 3)], [(0.5, 1.5), (1.6, 2.5)]]

mRangesDict = {"sample_%s" % num: inputList[num] for num in range(len(inputList))}

result_0 = getContinualNonSympyMergeResult(inputList)