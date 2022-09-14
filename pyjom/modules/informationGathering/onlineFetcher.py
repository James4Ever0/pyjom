from pyjom.commons import *
from type

@decorator
def OnlineFetcher(infoList, source='giphy'):
    # how do you chain this shit up?
    for info in infoList: # generator most likely
        if source=='giphy'