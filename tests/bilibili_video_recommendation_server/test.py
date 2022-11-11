import sys

sys.path.append("/root/Desktop/works/pyjom/")
from pyjom.platforms.bilibili.database import (
    bilibiliRecommendationServer,
    bootstrap,
    textPreprocessing,
    searchUserVideos,
    registerUserVideo,
    searchAndRegisterVideos,
)

# you should recommend by label instead of by name. but whatever.
if __name__ == "__main__":
    # objective = 'test'
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--objective", type=str, default="server")
    parsed_args = parser.parse_args()
    objective = parsed_args.objective
    # can't specify port here.
    # python3 -m uvicorn --port 7341 test:app
    if objective == "server":
        bilibiliRecommendationServer()
    elif objective == "test":
        bootstrap()
        test = "searchVideos"
        # test = "searchUserVideos"
        # test = "textPreprocessing"
        # test = 'registerMyVideo'
        if test == "textPreprocessing":
            text = "猫  咪  钢  琴  家 searchUserVideos have a nice day 新闻联播,动物圈,汪星人,喵星人"
            result = textPreprocessing(
                text
            )  # shall you do the same to your search query.
            print("RESULT:", result)
        elif test == "searchUserVideos":
            query = "猫"
            # for v in searchUserVideos(query):
            for v in searchUserVideos(query, method="bm25"):
                # print("fetched value:", v)
                breakpoint()
        elif test == "registerMyVideo":
            bvid = "BV1fR4y1w7BL"  # that's surely yours.
            dedeuserid = "397424026"
            registerUserVideo(bvid, dedeuserid)
        elif test == "searchVideos":
            query = "cod19"  # recent hot videos.
            for v in searchAndRegisterVideos(query):
                print(v)  # warning: title containing markup language.
                breakpoint()
            # you want to select video after search?
            # no keywords? are you kidding?
            # results = getMyVideos()
            # print(results)
            # video_bvid_invisible = "BV1pd4y1y7cu"  # too fucking fast. i can't see shit.
            # # some hard rule on this? like being invisible for how long we will disable video source for good?
            # video_bvid_abnormal = "BV1x84y1B7Nb"
            # video_bvid_visible = "BV1Fs411k7e9"  # 老戴的视频
            # # 啊叻？视频不见了？
            # checkPublishedVideo(video_bvid_invisible)
            # checkPublishedVideo(video_bvid_visible)
            # checkPublishedVideo(video_bvid_abnormal)
            # 视频撞车了 需要原创视频哦
