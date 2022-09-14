from pyjom.commons import *
from typing import Literal

@decorator
def OnlineFetcher(infoList, source:Literal['giphy']='giphy', frame_size_filter:dict={'width':{'min':200,'max':1000}, 'height':{'min':200,'max':1000}}):
    # how do you chain this shit up?
    for info in infoList: # generator most likely
        if source=='giphy':
            (source_id, mDict) = info
            width, height = mDict['width'], mDict['height']
            if not (checkMinMaxDict(width, frame_size_filter['width']) and checkMinMaxDict(height, frame_size_filter['height'])):
                print("Filter out invalid video with shape of {}x{}".format(width,height))
                print('Valid Width and Height are {}-{}x{}-{}'.format(width,height)