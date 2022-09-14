from pyjom.commons import *
from typing import Literal

@decorator
def OnlineFetcher(infoList, source:Literal['giphy']='giphy', frame_size_filter:dict={'width':200, 'height':200}):
    # how do you chain this shit up?
    min_width = frame_size_filter.get('width')
    min_height = frame_size_filter.get('height')
    for info in infoList: # generator most likely
        if source=='giphy':
            # (id, {width, height, url})