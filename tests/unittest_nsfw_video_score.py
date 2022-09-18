# we take max for the concerned ones, and take mean for the unconcerned ones.

from test_commons import *
import requests
from lazero.network.checker import waitForServerUp
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS
from typing import Literal

gateway = "http://localhost:8511/"

from pyjom.mathlib import superMean, superMax

from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2

# suggest you not to use this shit.
import math

from pyjom.imagetoolbox import resizeImageWithPadding, scale

from lazero.filesystem import tmpdir, tmpfile

tmpdirPath = "/dev/shm/medialang/nsfw"

import uuid

waitForServerUp(8511, "nsfw nodejs server")
import os

test_flag = "nsfw_video"
# test_flag = "nsfw_image"
# test_flag = "scanning"
# test_flag = "paddinging"

source = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif"
import numpy as np


def processNSFWServerImageReply(reply):
    mDict = {}
    for elem in reply:
        className, probability = elem["className"], elem["probability"]
        mDict.update({className: probability})
    return mDict


def processNSFWReportArray(
    NSFWReportArray,
    average_classes=["Neutral"],
    get_max_classes=["Drawing", "Porn", "Sexy", "Hentai"],
):
    assert set(average_classes).intersection(set(get_max_classes)) == set()
    NSFWReport = {}
    for element in NSFWReportArray:
        for key in element.keys():
            NSFWReport[key] = NSFWReport.get(key, []) + [element[key]]
    for average_class in average_classes:
        NSFWReport[average_class] = superMean(NSFWReport.get(average_class, [0]))
    for get_max_class in get_max_classes:
        NSFWReport[get_max_class] = superMax(NSFWReport.get(get_max_class, [0]))
    return NSFWReport


from pyjom.commons import checkMinMaxDict

# you can reuse this, really.
def NSFWFilter(
    NSFWReport,
    filter_dict={
        "Neutral": {"min": 0.5},
        "Sexy": {"max": 0.5},
        "Porn": {"max": 0.5},
        "Hentai": {"max": 0.5},
        "Drawing": {"max": 0.5},
    },
):
    for key in filter_dict:
        value = NSFWReport.get(key, 0)
        key_filter = filter_dict[key]
        result = checkMinMaxDict(value, key_filter)
        if not result:
            print("not passing NSFW filter: %s" % key)
            print("value: %s" % value)
            print("filter: %s" % str(key_filter))
            return False
    return True


if test_flag == "padding":
    for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
        image = resizeImageWithPadding(frame, 1280, 720, border_type="replicate")
        # i'd like to view this.
        cv2.imshow("PADDED", image)
        cv2.waitKey(0)
elif test_flag == "scanning":
    for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
        scanned_array = scanImageWithWindowSizeAutoResize(
            frame, 1280, 720, threshold=0.3
        )
        for index, image in enumerate(scanned_array):
            cv2.imshow("SCANNED %d" % index, image)
            cv2.waitKey(0)
elif test_flag == "nsfw_video":
    # use another source?
    with tmpdir(path=tmpdirPath) as T:
        responses = []
        for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
            padded_resized_frame = resizeImageWithPadding(
                frame, 224, 224, border_type="replicate"
            )
            # i'd like to view this.
            basename = "{}.jpg".format(uuid.uuid4())
            jpg_path = os.path.join(tmpdirPath, basename)
            with tmpfile(path=jpg_path) as TF:
                cv2.imwrite(jpg_path, padded_resized_frame)
                files = {"image": (basename, open(jpg_path, "rb"), "image/jpeg")}
                r = requests.post(
                    gateway + "nsfw", files=files
                )  # post gif? or just jpg?
                try:
                    response_json = r.json()
                    response_json = processNSFWServerImageReply(response_json)
                    # breakpoint()
                    # print("RESPONSE:", response_json)
                    responses.append(
                        response_json  # it contain 'messages'
                    )  # there must be at least one response, i suppose?
                except:
                    import traceback
                    traceback.print_exc()
                    print("error when processing NSFW server response")
        NSFWReport = processNSFWReportArray(responses)
        # print(NSFWReport)
        # breakpoint()
        result = NSFWFilter(NSFWReport)
        if result:
            print("NSFW test passed.")
            print("source %s" % source)
# we don't want drawing dogs.

# [{'className': 'Neutral', 'probability': 0.9995943903923035}, {'className': 'Drawing', 'probability': 0.00019544694805517793}, {'className': 'Porn', 'probability': 0.00013213469355832785}, {'className': 'Sexy', 'probability': 6.839347042841837e-05}, {'className': 'Hentai', 'probability': 9.632151886762585e-06}]
elif test_flag == "nsfw_image":
    source = "/root/Desktop/works/pyjom/samples/image/kitty_flash.bmp"
    # RESPONSE: [{'className': 'Neutral', 'probability': 0.9997681975364685}, {'className': 'Drawing', 'probability': 0.0002115015813615173}, {'className': 'Porn', 'probability': 1.3146535820851568e-05}, {'className': 'Hentai', 'probability': 4.075543984072283e-06}, {'className': 'Sexy', 'probability': 3.15313491228153e-06}]
    # source = '/root/Desktop/works/pyjom/samples/image/pig_really.bmp'
    # RESPONSE: [{'className': 'Neutral', 'probability': 0.9634107351303101}, {'className': 'Porn', 'probability': 0.0244674663990736}, {'className': 'Drawing', 'probability': 0.006115634460002184}, {'className': 'Hentai', 'probability': 0.003590137232095003}, {'className': 'Sexy', 'probability': 0.002416097791865468}]
    # source = "/root/Desktop/works/pyjom/samples/image/dog_with_text.bmp"
    # source = '/root/Desktop/works/pyjom/samples/image/dick2.jpeg'
    # [{'className': 'Porn', 'probability': 0.7400921583175659}, {'className': 'Hentai', 'probability': 0.2109236866235733}, {'className': 'Sexy', 'probability': 0.04403943940997124}, {'className': 'Neutral', 'probability': 0.0034419416915625334}, {'className': 'Drawing', 'probability': 0.0015027812914922833}]
    # source = '/root/Desktop/works/pyjom/samples/image/dick4.jpeg'
    # RESPONSE: [{'className': 'Porn', 'probability': 0.8319052457809448}, {'className': 'Hentai', 'probability': 0.16578854620456696}, {'className': 'Sexy', 'probability': 0.002254955470561981}, {'className': 'Neutral', 'probability': 3.2827374525368214e-05}, {'className': 'Drawing', 'probability': 1.8473130694474094e-05}]
    # source = '/root/Desktop/works/pyjom/samples/image/porn_shemale.jpeg'
    # no good for this one. this is definitely some unacceptable shit, with just cloth wearing.
    # RESPONSE: [{'className': 'Neutral', 'probability': 0.6256022453308105}, {'className': 'Hentai', 'probability': 0.1276213526725769}, {'className': 'Porn', 'probability': 0.09777139872312546}, {'className': 'Sexy', 'probability': 0.09318379312753677}, {'className': 'Drawing', 'probability': 0.05582122132182121}]
    # source ='/root/Desktop/works/pyjom/samples/image/dick3.jpeg'
    # [{'className': 'Porn', 'probability': 0.978420078754425}, {'className': 'Hentai', 'probability': 0.01346961222589016}, {'className': 'Sexy', 'probability': 0.006554164923727512}, {'className': 'Neutral', 'probability': 0.0015426197787746787}, {'className': 'Drawing', 'probability': 1.354961841570912e-05}]
    # a known source causing unwanted shits.
    image = cv2.imread(source)
    basename = "{}.jpg".format(uuid.uuid4())
    jpg_path = os.path.join(tmpdirPath, basename)
    with tmpfile(path=jpg_path) as TF:
        # black padding will lower the probability of being porn.
        padded_resized_frame = resizeImageWithPadding(image, 224, 224)
        # RESPONSE: [{'className': 'Neutral', 'probability': 0.6441782116889954}, {'className': 'Porn', 'probability': 0.3301379978656769}, {'className': 'Sexy', 'probability': 0.010329035110771656}, {'className': 'Hentai', 'probability': 0.010134727694094181}, {'className': 'Drawing', 'probability': 0.005219993181526661}]
        # padded_resized_frame = resizeImageWithPadding(image, 224, 224,border_type='replicate')
        # RESPONSE: [{'className': 'Neutral', 'probability': 0.6340386867523193}, {'className': 'Porn', 'probability': 0.3443007171154022}, {'className': 'Sexy', 'probability': 0.011606302112340927}, {'className': 'Hentai', 'probability': 0.006618513725697994}, {'className': 'Drawing', 'probability': 0.0034359097480773926}]
        # neutral again? try porn!
        cv2.imwrite(jpg_path, padded_resized_frame)
        files = {"image": (basename, open(jpg_path, "rb"), "image/jpeg")}
        r = requests.post(gateway + "nsfw", files=files)  # post gif? or just jpg?
        print("RESPONSE:", r.json())
else:
    raise Exception("unknown test_flag: %s" % test_flag)
# you can only post gif now, or you want to post some other formats?
# if you post shit, you know it will strentch your picture and produce unwanted shits.
