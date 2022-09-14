from pyjom.commons import *
from typing import Literal

@decorator
def OnlineFetcher(infoList, source:Literal['giphy']='giphy', frame_size_filter:dict={'width':{'min':200,'max':1000}, 'height':{'min':200,'max':1000}}, tempdir='/dev/shm/medialang/online'):
    # how do you chain this shit up?
    assert os.path.isabs(tempdir)
    assert os.path.isdir(tempdir)
    assert os.path.exists(tempdir)
    for info in infoList: # generator most likely
        if source=='giphy':
            (source_id, frameMeta) = info
            flag = frameSizeFilter(frameMeta, frame_size_filter)
            if flag:
                # this time it is selected.
                downloadPath = os.path.join(tempdir,filename)
                url = frameMeta["url"]
                extension = url.split("?")[0].split(".")[-1]
                basename = ".".join([asset_id, extension])
                download_path = os.path.join(path, basename)
                download(url, download_path, threads=-0.3, size_filter={"min":0.4, "max":50})
                yield source_id, downloadPath