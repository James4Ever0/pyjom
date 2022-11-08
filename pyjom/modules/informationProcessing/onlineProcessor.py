from reloading import reloading
import pyjom.videotoolbox as vtb
from pyjom.commons import decorator, keywordDecorator
import os
from lazero.utils import sprint
from lazero.network import waitForServerUp
from lazero.filesystem import tmpdir

# # flag = "topic_with_fetcher"
# # should't we have our judgement here?

#     collection = getMilvusVideoDeduplicationCollection(get_existing = get_existing)
@decorator
@reloading
def OnlineProcessor(
    newElems,  # a generator.
    source="giphy",
    use_proxy=False,  # use some proxy.
    clash_refresher_port=8677,
    proxy_url="http://127.0.0.1:8381",
    tmpPath="/dev/shm/medialang/onlineProcessor",
    debug=False,
    # dog_or_cat?
    dog_or_cat="dog",
    yolov5_default_filter_dict={
        "dog": {"min": 0.5},
        "cat": {"min": 0.5},
    },
):
    if use_proxy:
        clash_refresher_url = "http://127.0.0.1:{}".format(clash_refresher_port)
        waitForServerUp(clash_refresher_port, "clash update controller")

    def set_proxy():
        os.environ["http_proxy"] = proxy_url
        os.environ["https_proxy"] = proxy_url

    with tmpdir(path=tmpPath) as testDir:
        # elif flag == "topic_with_fetcher":
        # sprint("checking online fetcher")
        # print("HERE??",2)
        if use_proxy:
            set_proxy()
        if source == "giphy":
            for elem in newElems:
                if use_proxy:
                    waitForServerUp(clash_refresher_port, "clash update controller")
                if debug:
                    sprint(elem)
                (item_id, local_video_location) = elem
                # what is the freaking response?
                from caer.video.frames_and_fps import (
                    get_duration,
                    get_fps_float,
                    get_res,
                )

                # duration = get_duration(local_video_location)
                from pyjom.commons import checkMinMaxDict

                duration_filter = {"min": 0.6, "max": 12}
                fps_filter = {"min": 7, "max": 60}
                # fps_float = get_fps_float(local_video_location)
                # duration_valid = checkMinMaxDict(duration,duration_filter)
                # fps_valid = checkMinMaxDict(fps_float,fps_filter)
                from pyjom.videotoolbox import (
                    corruptVideoFilter,
                    getVideoColorCentrality,
                    checkVideoColorCentrality,
                    getEffectiveFPS,
                    NSFWVideoFilter,
                    yolov5_bezier_paddlehub_resnet50_dog_cat_video_filter,
                    dummyFilterFunction,  # just for dog and cat, no other animals.
                    getVideoTextAreaRatio,
                )

                video_color_filter = {
                    "centrality": {"max": 0.18},  # stricter limit?
                    "max_nearby_center_percentage": {"max": 0.13},
                }
                video_effective_fps_filter = {"min": 7}
                videoTextAreaRatioFilter = {"max": 0.3}
                valid = True
                mList = [
                    [
                        corruptVideoFilter,
                        None,
                        dummyFilterFunction,
                        "video corruption filter",
                    ],
                    [get_duration, duration_filter, checkMinMaxDict, "duration"],
                    [get_fps_float, fps_filter, checkMinMaxDict, "fps"],
                    [
                        getVideoTextAreaRatio,
                        videoTextAreaRatioFilter,
                        checkMinMaxDict,
                        "videoTextAreaRatioFilter",
                    ],
                    [
                        # yolov5_bezier_paddlehub_resnet50_dog_cat_video_filter,
                        keywordDecorator(
                            yolov5_bezier_paddlehub_resnet50_dog_cat_video_filter,
                            filter_dict={
                                key: value
                                for key, value in yolov5_default_filter_dict.items()
                                if key == dog_or_cat
                            },
                        ),
                        None,
                        dummyFilterFunction,
                        "DogCat",
                    ],
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
                        vtb.duplicatedVideoFilter,
                        None,
                        dummyFilterFunction,
                        "video duplication filter",
                    ],
                ]
                for function, mFilter, filterFunction, flag in mList:
                    try:
                        mValue = function(local_video_location)
                        valid = filterFunction(mValue, mFilter)
                        if not valid:
                            print("skipping due to invalid %s: %s" % (flag, mValue))
                            print("%s filter:" % flag, mFilter)
                            break
                    except:
                        import traceback

                        traceback.print_exc()
                        print("skipping due to exception during filtering")
                        valid = False
                        break
                if not valid:
                    print("abandon video:", item_id)
                # breakpoint()
                if not valid:
                    if os.path.exists(local_video_location):
                        print("removing abandoned video:", local_video_location)
                        os.remove(local_video_location)
                else:
                    video_width, video_height = get_res(local_video_location)
                    yield {
                        "location": local_video_location,
                        "item_id": item_id,
                        "meta": {
                            "duration": get_duration(local_video_location),
                            "width": video_width,
                            "height": video_height,
                        },
                    }
                    # if you abandon that, better delete it!
                # do time duration check, effective fps check, color centrality check, then the dog/cat check
                # what's next? find some audio files? or just use one audio?
                # print("HERE??",3)
                # print('flag', flag)
