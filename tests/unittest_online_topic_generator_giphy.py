from test_commons import *
from pyjom.modules.topicGenerator import OnlineTopicGenerator
from pyjom.modules.informationGathering import OnlineFetcher
from lazero.utils import sprint
from lazero.network import download
from lazero.filesystem import tmpdir

elems, label = OnlineTopicGenerator()
sprint("LABEL:", label)
# # 'pyjom.commons.OnlineTopicGenerator'
# breakpoint()
tmpPath = "/dev/shm/medialang/online_test"
import os
flag = 'topic_with_fetcher'

with tmpdir(path=tmpPath) as testDir:
    print("TESTDIR:", testDir)
    if flag == 'only_topic_generator':
        # print("HERE??",1)
        for asset_id, meta in elems:
            print("X", asset_id, meta)
            url = meta["url"]
            extension = url.split("?")[0].split(".")[-1]
            basename = ".".join([asset_id, extension])
            download_path = os.path.join(tmpPath, basename)
            try:
                download(url, download_path, threads=-0.3, size_filter={"min":0.4, "max":50})
            except:
                print("Error when download file")
            # X ('sr8jYZVVsCmxddga8w', {'height': 480, 'width': 474, 'url': 'https://media0.giphy.com/media/sr8jYZVVsCmxddga8w/giphy.gif'})
            # breakpoint()
            # seems good. now we check the cat/dog.
    elif flag == 'topic_with_fetcher':
        sprint("checking online fetcher")
        # print("HERE??",2)
        newElems, label = OnlineFetcher(elems, tempdir=tmpPath)
        for elem in newElems:
            sprint(elem)
            (item_id, local_video_location) = elem
            # what is the freaking response?
            from caer.video.frames_and_fps import get_duration
            duration = get_duration(local_video_location)
            from pyjom.commons import checkMinMaxDict
            duration_valid = checkMinMaxDict(
            # do time duration check, effective fps check, color centrality check, then the dog/cat check
            breakpoint()
    # print("HERE??",3)
    # print('flag', flag)
    