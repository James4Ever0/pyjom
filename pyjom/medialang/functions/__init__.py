from pyjom.medialang.functions.detectors import *

medialangFunctions = {"detector": medialangDetectors}


def getMedialangFunction(function):
    for key in medialangFunctions:
        mgroup = medialangFunctions[key]
        for key2 in mgroup:
            if key2 == function:
                function = mgroup[key2]
                print("function type:", key)
                print("function name:", key2)
                return function
    return None
