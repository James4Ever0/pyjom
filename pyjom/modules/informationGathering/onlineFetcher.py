from pyjom.commons import *
from typing import Literal

@decorator
def OnlineFetcher(infoList, source:Literal['giphy']='giphy'):
    # how do you chain this shit up?
    for info in infoList: # generator most likely
        if source=='giphy':
            