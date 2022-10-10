import sys
import os

os.chdir("../../")
sys.path.append(".")
# ignore the global proxy now, we are not going to use that.
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2
from pyjom.platforms.bilibili.postMetadata import getBilibiliPostMetadataForDogCat
# metatopic = {
#     "optional": [
#         [
#             "狗狗",
#             "狗",
#             "汪汪",
#             "修勾",
#             "汪",
#             "狗子",
#         ],
#         ["喵喵", "猫", "猫咪", "喵"],
#     ],
#     "dynamic": [["可爱", "萌", "萌宠", "行为", "燃"]],
# }

# maybe this is not task specific. just maybe.


if __name__ == "__main__":
    for (
        mCover,
        mTagSeries,
        mTitle,
        mBgm,
        mDescription,
        dog_or_cat,
    ) in getBilibiliPostMetadataForDogCat():
        print("FETCHED VIDEO METADATA FOR PRODUCTION:")
        videoMetadata = mCover, mTagSeries, mTitle, mBgm, mDescription, dog_or_cat
        print(videoMetadata)
        mCover2 = cv2.resize(mCover, (int(1920 / 2), int(1080 / 2)))
        cv2.imshow("COVER", mCover2)
        cv2.waitKey(0)
        breakpoint()
