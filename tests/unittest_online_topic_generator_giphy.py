from test_commons import *
from pyjom.modules.topicGenerator import OnlineTopicGenerator
from pyjom.modules.informationGathering import OnlineFetcher
from lazero.utils import sprint
from lazero.network import download
from lazero.filesystem import tmpdir

elems, function_label = OnlineTopicGenerator()
sprint("FUNCTION LABEL:", function_label)
# # 'pyjom.commons.OnlineTopicGenerator'
# breakpoint()
tmpPath = "/dev/shm/medialang/online_test"
import os

flag = "topic_with_fetcher"

with tmpdir(path=tmpPath) as testDir:
    print("TESTDIR:", testDir)
    if flag == "only_topic_generator":
        # print("HERE??",1)
        for asset_id, meta in elems:
            print("X", asset_id, meta)
            url = meta["url"]
            extension = url.split("?")[0].split(".")[-1]
            basename = ".".join([asset_id, extension])
            download_path = os.path.join(tmpPath, basename)
            try:
                download(
                    url,
                    download_path,
                    threads=-0.3,
                    size_filter={"min": 0.4, "max": 50},
                )
            except:
                print("Error when download file")
            # X ('sr8jYZVVsCmxddga8w', {'height': 480, 'width': 474, 'url': 'https://media0.giphy.com/media/sr8jYZVVsCmxddga8w/giphy.gif'})
            # breakpoint()
            # seems good. now we check the cat/dog.
    elif flag == "topic_with_fetcher":
        sprint("checking online fetcher")
        # print("HERE??",2)
        newElems, label = OnlineFetcher(elems, tempdir=tmpPath) # infinite video generators.
        for elem in newElems:
            sprint(elem)
            (item_id, local_video_location) = elem
            # what is the freaking response?
            from caer.video.frames_and_fps import get_duration, get_fps_float

            # duration = get_duration(local_video_location)
            from pyjom.commons import checkMinMaxDict

            duration_filter = {"min": 0.6, "max": 9}
            fps_filter = {"min": 7, "max": 60}
            # fps_float = get_fps_float(local_video_location)
            # duration_valid = checkMinMaxDict(duration,duration_filter)
            # fps_valid = checkMinMaxDict(fps_float,fps_filter)
            from pyjom.videotoolbox import (
                getVideoColorCentrality,
                checkVideoColorCentrality,
                getEffectiveFPS,
                NSFWVideoFilter,
                yolov5_bezier_paddlehub_resnet50_dog_cat_video_filter,
                dummyFilterFunction,  # just for dog and cat, no other animals.
            )

            video_color_filter = {
                "centrality": {"max": 0.30},
                "max_nearby_center_percentage": {"max": 0.20},
            }
            video_effective_fps_filter = {"min": 7}
            valid = True
            mList = [
                [get_duration, duration_filter, checkMinMaxDict, "duration"],
                [get_fps_float, fps_filter, checkMinMaxDict, "fps"],
                [
                    getVideoColorCentrality,
                    video_color_filter,
                    checkVideoColorCentrality,
                    "video_color_centrality",
                ],
                [
                    getEffectiveFPS,
                    video_effective_fps_filter,
                    checkMinMaxDict,
                    "EffectiveFPS",
                ],  # also, the dog/cat detector! fuck.
                [NSFWVideoFilter, None, dummyFilterFunction, "NSFW"],
                [
                    yolov5_bezier_paddlehub_resnet50_dog_cat_video_filter,
                    None,
                    dummyFilterFunction,
                    "DogCat",
                ],
            ]
            for function, mFilter, filterFunction, flag in mList:
                mValue = function(local_video_location)
                valid = filterFunction(mValue, mFilter)
                if not valid:
                    print("skipping due to invalid %s: %s" % (flag, mValue))
                    print("%s filter:" % flag, mFilter)
                    break
            if not valid:
                print("abandon video:", item_id)
                # if you abandon that, better delete it!
            # do time duration check, effective fps check, color centrality check, then the dog/cat check
            breakpoint()
    # print("HERE??",3)
    # print('flag', flag)
