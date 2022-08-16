from pyjom.medialang.functions import *
from pyjom.medialang.commons import *

def dotVideoProcessor(item, previous,format="mp4"):
    print("DOTVIDEO ARGS:", item, previous, format)
    # this item is the video output config, medialang item.
    itemArgs = item.args
    backend = itemArgs["backend"]
    fast = itemArgs["fast"]
    bgm = itemArgs["bgm"]
    print(backend, fast,bgm)

    # the "previous" is the clips, now fucked.
    # this is initially decided to output mp4, however you might want to decorate it.
    print("_________INSIDE DOT VIDEO PROCESSOR_________")
    print("ITEM:", item)
    print("PREVIOUS:", previous)
    print("_________INSIDE DOT VIDEO PROCESSOR_________")
