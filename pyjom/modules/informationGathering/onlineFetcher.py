from pyjom.commons import *


@decorator
def OnlineFetcher(infoList):
    # how do you chain this shit up?
    for info in infoList: # generator most likely
        if 