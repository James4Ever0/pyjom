# to get a proper cover, let's simply crop.

# to find a proper title for this video, extract keywords, generate title and find the best cover by embeddings.

# first, get picture aspect.

import cv2


def getWidthHeight(impath):
    d = cv2.imread(impath)
    # print(d.shape)
    height, width, channels = d.shape
    return width, height


im0 = "long_and_funny_image_about_ai_painting.jpg"
im1 = "intermediate.png"
# very high, low width.
# calculate actual output?
mheight, mwidth = 1080, 1920
width, height = getWidthHeight(im0)
import ffmpeg

ffmpeg.input(im0).filter("scale", w=mwidth, h=-1).output(im1).run(overwrite_output=True)
width0, height0 = getWidthHeight(im1)
pad_total =( mheight-(height0 % mheight)) % mheight
# print("PAD TOTAL?", pad_total)
# breakpoint()
if pad_total != 0:
    im2 = "intermediate_0.png"
    pad_above = pad_total // 2
    pad_below = pad_total - pad_above
    # then you must rewrite this shit.
    ffmpeg.input(im1).filter(
        "pad", w="iw", h="ih+{}".format(pad_total), x=0, y=pad_above, color="white"
    ).output(im2).run(overwrite_output=True)
else:
    im2 = im1

# then chop it up.
import os
import shutil

mdir = "output"
fout = "output%d.png"

if os.path.exists(mdir):
    shutil.rmtree(mdir)
os.mkdir(mdir)
mfout = os.path.join(mdir, fout)
import math

mh = math.ceil(height0 / mheight)
mlayout = "1x{}".format(mh)
ffmpeg.input(im2).filter("untile", layout=mlayout).output(mfout).run(
    overwrite_output=True
)

mfiles = os.listdir(mdir)
import re

output_path = "./output.mp4"

mfiles.sort(key=lambda x: int(re.findall(r"[0-9]+", x)[0]))
editly_script = {
    "width": mwidth,
    "height": mheight,
    "fps": 60,
    "outPath": output_path,
    "defaults": {
        "transition": {
            "duration": 0.5,
            "name": "random",
            "audioOutCurve": "tri",
            "audioInCurve": "tri",
        },
        "duration": 3,
    },
    "clips": [
        {"layers": [{"type": "image", "path": os.path.join(mdir, mfile)}]}
        for mfile in mfiles
    ],
    "audioFilePath": "the_happy_troll.mp3",
}

import json5

editly_spec_file = "spec_file.json5"
with open(editly_spec_file, "w+") as fp:
    json5.dump(editly_script, fp)

# now execute
import os

os.system("rm -rf editly-tmp*")
os.system("xvfb-run editly {}".format(editly_spec_file))
