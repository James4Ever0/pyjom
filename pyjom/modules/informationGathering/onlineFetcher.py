from pyjom.commons import *
from typing import Literal

@decorator
def OnlineFetcher(infoList, source:Literal['giphy']='giphy', frame_size_filter:dict={'width':{'min':200,'max':1000}, 'height':{'min':200,'max':1000}}):
    # how do you chain this shit up?
    for info in infoList: # generator most likely
        if source=='giphy':
            (id, {width, height, url})