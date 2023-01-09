import traceback
from pyjom.config import *
from typing import Union
from pyjom.mathlib import checkMinMaxDict

import datetime
import os
import shutil
import socket
import json
import mimetypes
import jinja2
import copy
import uuid
import numpy as np
import torch

import pathlib
import site
import sys
import random

# from functools import lru_cache

commonRedisPort = 9291
os.system("ulimit -n 1048576")
from lazero.utils.logger import sprint
from functools import lru_cache
import time


def getJSTimeStamp():
    return int(time.time() * 1000)


from pymilvus import connections


@lru_cache(maxsize=1)
def connectMilvusDatabase(alias="default", host="localhost", port="19530"):
    connection = connections.connect(
        alias=alias, host=host, port=port
    )  # can we reconnect?
    print("milvus connected")
    return connection


# what is the redis connection?
import redis


@lru_cache(maxsize=1)
def getRedisConnection(host="localhost", port=commonRedisPort):
    connection = redis.Redis(host=host, port=port)
    return connection


def removeRedisValueByKey(
    key: str, debug: bool = False, host="localhost", port=commonRedisPort
):
    connection = getRedisConnection(host=host, port=port)
    returnCode = connection.delete(key)
    messages = {
        0: "key {} not found".format(key),
        1: "delete key {} successfully".format(key),
    }
    if debug:
        print(messages.get(returnCode, "unknown return code: {}".format(returnCode)))
    return returnCode


def removeRedisValueByKeys(
    keys: list[str], debug: bool = False, host="localhost", port=commonRedisPort
):
    for key in keys:
        removeRedisValueByKey(key, debug=debug, host=host, port=port)


# @lru_cache(maxsize=1)
# def getSafeEvalEnvironment():
#     return sf


def safe_eval(
    code, safenodes=["List", "Dict", "Tuple", "Set", "Expression", "Constant", "Load"]
):  # strange.
    from evalidate import safeeval

    result = safeeval(code, {}, safenodes=safenodes)
    return result


import pickle, dill

commonIterableDataTypes = [tuple, list, dict, set]
commonNonIterableDataTypes = [int, float, str, bool]
commonDataTypes = commonNonIterableDataTypes + commonIterableDataTypes


def stringifiableCheck(value, debug: bool = False):
    try:
        str_value = repr(value)
        restored_value = safe_eval(value)
        return restored_value == value
    except:
        if debug:
            traceback.print_exc()
    return False


def setRedisValueByKey(
    key: str,
    value,
    dataType=None,
    encoding: str = "utf-8",
    host="localhost",
    port=commonRedisPort,
    debug: bool = False,
):
    def stringifyAndEncode(value):
        data = repr(value)
        data = data.encode(encoding)
        return data

    connection = getRedisConnection(host=host, port=port)
    if dataType is None:
        dataType = type(value)
        if dataType in commonDataTypes and stringifiableCheck(
            value, debug=debug
        ):  # this automation only happens when leaving blank for dataType.
            data = stringifyAndEncode(value)
        else:
            dataType = "dill"
            data = dill.dumps(value)
    else:
        if dataType in commonDataTypes:
            data = stringifyAndEncode(value)
        elif dataType == "dill":
            data = dill.dumps(value)
        elif dataType == "pickle":
            data = pickle.dumps(value)
        else:
            raise Exception("unknown dataType:", dataType)
    connection.set(key, data)
    return dataType


def getRedisValueByKey(
    key: str,
    dataType=None,
    encoding: str = "utf-8",
    debug: bool = False,
    host="localhost",
    port=commonRedisPort,
):
    connection = getRedisConnection(host=host, port=port)
    value = connection.get(key)
    if value is not None:
        if debug:
            print('data "{}" is not None'.format(key))
        if dataType == None:
            return dataType
        elif dataType in commonDataTypes:
            decoded_value = value.decode(encoding)
            if dataType in commonNonIterableDataTypes:
                if dataType == str:
                    return decoded_value
                else:
                    return dataType(decoded_value)
            else:
                # safe eval using nsjail?
                return safe_eval(decoded_value)
        elif dataType == "pickle":
            return pickle.loads(value)
        elif dataType == "dill":
            return dill.loads(value)
        else:
            raise Exception("unknown dataType:", dataType)
    if debug:
        print('data "{}" is None'.format(key))


def getRedisCachedSet(
    setName: str,
    debug: bool = False,
    host="localhost",
    port=commonRedisPort,
    dataType="dill",
) -> set:
    # so we know this datatype is set!
    # but what is our plan? we use dill by default.
    data = getRedisValueByKey(
        setName, debug=debug, host=host, port=port, dataType=dataType
    )
    if data is None:
        return set()
    assert type(data) == set
    return data


def addToRedisCachedSet(
    item,
    setName: str,
    debug: bool = False,
    host="localhost",
    port=commonRedisPort,
    dataType="dill",
):
    cachedSet = getRedisCachedSet(
        setName, debug=debug, host=host, port=port, dataType=dataType
    )
    cachedSet.add(item)
    setRedisValueByKey(setName, cachedSet, dataType=dataType, host=host, port=port)
    return cachedSet


def shuffleAndPopFromList(mlist):
    import random

    random.shuffle(mlist)
    return mlist.pop(0)


def getMediaBitrate(mediaPath, audioOnly=False, videoOnly=False):
    # demo output:
    # {'programs': [], 'streams': [{'bit_rate': '130770'}]}
    commandArguments = [
        "ffprobe",
        "-i",
        mediaPath,
        "-v",
        "quiet",
    ]
    if audioOnly:
        commandArguments += [
            "-select_streams",
            "a:0",
        ]
    elif videoOnly:
        commandArguments += [
            "-select_streams",
            "v:0",
        ]
    commandArguments += [
        "-show_entries",
        "stream=bit_rate",
        "-hide_banner",
        "-print_format",
        "json",
    ]
    result = subprocess.run(commandArguments, capture_output=True, encoding="UTF-8")
    stdout = result.stdout
    stderr = result.stderr
    try:
        assert result.returncode == 0
        stdout_json = json.loads(stdout)
        return stdout_json
    except:
        import traceback

        traceback.print_exc()
        print("potential error logs:")
        print(stderr)
        print("error when getting media bitrate")
        return {}


def getFileExtensionToMeaningDictFromString(inputString):
    inputStringList = inputString.split("\n")
    fileExtensionToMeaningDict = {}
    for line in inputStringList:
        line = line.strip()
        if len(line) < 5:
            continue
        # try:
        meaning, extensions = line.split(" - ")  # problem fixed.
        # except:
        #     print('line:',[line])
        #     breakpoint()
        meaning = meaning.strip()
        extensions = extensions.split(" or ")
        for extension in extensions:
            extension = extension.strip()
            if len(extension) > 0:
                fileExtensionToMeaningDict.update({extension: meaning})
    return fileExtensionToMeaningDict


@lru_cache(maxsize=1)
def getMediaFileExtensionToMeaningDict():
    # no input needed.
    videoExtensions = """MP4 or MPEG4 video file - .mp4
264 video file - .h264
AVI video file - .avi
MKV or Matroska Multimedia Container - .mkv
MPEG video file - .mpeg or .mpg
MOV or Apple QuickTime video file - .mov
Apple MP4 video file - .m4v
Adobe flash video - .flv
3GP video file - .3gp
Windows Media Video file - .wmv
DVD Video Object - .vob"""
    imageExtensions = """JPEG image - .jpeg or .jpg
PNG image - .png
GIF image - .gif
Photoshop or PSD image - .psd
Adobe Illustrator image - .ai
TIFF image - .tif or .tiff"""
    documentExtensions = """Microsoft Word file - .doc or .docx
PDF file - .pdf
Text file - .txt
Microsoft Excel file - .xls
Microsoft Excel Open XML file - .xlsx
Microsoft Excel file with macros - .xlsm
Microsoft PowerPoint presentation - .ppt
Microsoft PowerPoint slide show - .pps
Microsoft PowerPoint Open XML presentation - .pptx"""
    audioExtensions = """MP3 audio file - .mp3
AAC audio file - .aac
AC3 audio file - .ac3
WAV audio file - .wav
WMA audio file - .wma
Ogg Vorbis audio file - .ogg
MIDI audio file - .midi or .mid
CD audio file - .cda
AIF audio file - .aif"""
    mapping = [
        ("video", videoExtensions),
        ("audio", audioExtensions),
        ("image", imageExtensions),  # gif could be video.
        ("document", documentExtensions),
    ]
    mediaFileExtensionToMeaningDict = {
        key: getFileExtensionToMeaningDictFromString(value) for key, value in mapping
    }
    return mediaFileExtensionToMeaningDict


def determineMediaTypeByExtension(extension):
    extension = extension.strip()
    if not extension.startswith("."):
        extension = "." + extension
    extension_lower = extension.lower()
    # this has to be cached.
    mediaFileExtensionToMeaningDict = getMediaFileExtensionToMeaningDict()
    for (
        mediaType,
        fileExtensionToMeaningDict,
    ) in mediaFileExtensionToMeaningDict.items():
        for fileExtension, meaning in fileExtensionToMeaningDict.items():
            if fileExtension.lower == extension_lower:
                return mediaType
    return "unknown"


def corruptMediaFilter(
    mediaPath, tag: str = "media", bad_words: list[str] = ["invalid", "failed", "error"]
):
    if not os.path.exists(mediaPath):
        print("{} file does not exist".format(tag))
    import ffmpeg

    not_nice = [word.lower() for word in bad_words]
    corrupted = False
    try:
        stdout, stderr = (
            ffmpeg.input(mediaPath)
            .output("null", f="null")
            .run(capture_stdout=True, capture_stderr=True)
        )
        stderr_lower = stderr.decode("utf-8").lower()
        for word in not_nice:
            if word in stderr_lower:
                print("{} is corrupted".format(tag))
                corrupted = True
                break
    except:
        import traceback

        traceback.print_exc()
        corrupted = True
        print("corrupt {}".format(tag))

    if not corrupted:
        print("video is fine")
    # return True for fine video.
    valid = not corrupted
    sprint("{} file path:".format(tag), mediaPath)
    return valid


## bring about 'redis cache' for faster testing.
import redis
from redis_lru import RedisLRU

# from functools import lru_cache
oneDay = 60 * 60 * 24  # one day?
redisExpire = oneDay * 7  # god damn it!

# @lru_cache(maxsize=1)
def redisLRUCache(
    ttl=redisExpire,
    redisAddress="127.0.0.1",
    redisPort=commonRedisPort,
    max_size=20,
    debug=True,
):
    client = redis.StrictRedis(host=redisAddress, port=redisPort)
    cache = RedisLRU(client, max_size=max_size, debug=debug)
    return cache(ttl=ttl)


# this is root. this is not site-packages.
def frameSizeFilter(frameMeta, frame_size_filter):
    width, height = frameMeta["width"], frameMeta["height"]
    flagWidth, (minWidth, maxWidth) = checkMinMaxDict(
        width, frame_size_filter.get("width", {}), getMinMaxVal=True
    )  # type: ignore
    flagHeight, (minHeight, maxHeight) = checkMinMaxDict(
        height, frame_size_filter.get("height", {}), getMinMaxVal=True
    )  # type: ignore
    if not (flagWidth and flagHeight):
        print("Filter out invalid video with shape of {}x{}".format(width, height))
        print(
            "Valid Width and Height are {}-{}x{}-{}".format(
                minWidth, maxWidth, minHeight, maxHeight
            )
        )
        return False
    return True


# site_path = pathlib.Path([x for x in site.getsitepackages() if "site-packages" in x][0])
os.environ["USE_NVIDIA_OPENCV"] = "yes"
if os.environ["USE_NVIDIA_OPENCV"] == "yes":
    site_path = pathlib.Path("/usr/local/lib/python3.9/site-packages")
    cv2_libs_dir = (
        site_path / "cv2" / f"python-{sys.version_info.major}.{sys.version_info.minor}"
    )
    print(cv2_libs_dir)
    cv2_libs = sorted(cv2_libs_dir.glob("*.so"))
    if len(cv2_libs) == 1:
        print("INSERTING:", cv2_libs[0].parent)
        sys.path.insert(1, str(cv2_libs[0].parent))


mimetypes.init()


def waitForServerUp(
    port, message, timeout=1, messageLength: Union[None, int] = None  # for netease.
):  # this messageLength is the length of the binary message.
    import requests

    while True:
        try:
            url = "http://localhost:{}".format(port)
            with requests.get(url, timeout=timeout) as r:
                if messageLength is not None:
                    contentLength = len(r.content)
                    if messageLength <= contentLength:
                        break
                else:
                    if type(message) == str:
                        text = r.text.strip('"').strip("'")
                    else:
                        text = r.json()
                    print("SERVER AT PORT %d RESPONDS:" % port, [text])
                    assert text == message
                    print("SERVER AT PORT %d IS UP" % port)
                    break
        except:
            import traceback

            traceback.print_exc()
            print("SERVER AT PORT %d MIGHT NOT BE UP" % port)
            print("EXPECTED MESSAGE:", [message])
            import time

            time.sleep(1)


class D2Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def doRectOverlap(l1, r1, l2, r2):
    # if rectangle has area 0, no overlap
    if l1.x == r1.x or l1.y == r1.y or r2.x == l2.x or l2.y == r2.y:
        return False
    # If one rectangle is on left side of other
    if l1.x >= r2.x or l2.x >= r1.x:
        return False
    if l1.y >= r2.y or l2.y >= r1.y:
        return False
    return True


def checkRectOverlap(rect0, rect1):
    assert len(rect0) == 2
    assert len(rect1) == 2
    return doRectOverlap(
        D2Point(*rect0[0]), D2Point(*rect0[1]), D2Point(*rect1[0]), D2Point(*rect1[1])
    )


def getOverlapRect(rect0, rect1):
    if checkRectOverlap(rect0, rect1):
        leftXList = (rect0[0][0], rect1[0][0])
        leftYList = (rect0[0][1], rect1[0][1])
        rightXList = (rect0[1][0], rect1[1][0])
        rightYList = (rect0[1][1], rect1[1][1])
        leftX = max(leftXList)
        leftY = max(leftYList)
        rightX = min(rightXList)
        rightY = min(rightYList)
        return [(leftX, leftY), (rightX, rightY)]
    else:
        return None


def makeValueInRange(value, minVal, maxVal):
    assert minVal < maxVal
    return min(max(minVal, value), maxVal)


# this sucks...
def infiniteShuffle(access_list, shuffle=True, infinite=True, endMark=True):
    flag = True
    while flag:
        if shuffle:
            random.shuffle(access_list)
        for data in access_list:
            yield data
        if endMark and infinite:
            yield None
        if not infinite:
            flag = False


def inRange(target, mRange, tolerance=1):
    assert tolerance <= 1
    assert tolerance > 0
    start, end = mRange
    start, end = start * tolerance, end / tolerance
    return target >= start and target <= end


def overlapRange(range_a, range_b):
    begin_a, end_a = range_a
    begin_b, end_b = range_b
    possible_overlap = (max(begin_a, begin_b), min(end_a, end_b))
    if possible_overlap[0] < possible_overlap[1]:  # overlapping
        return possible_overlap
    # return common range.


from lazero.utils.json import jsonWalk2, jsonify, jsonWalk, jsonLocate, jsonUpdate

json.__dict__.update({"walk": jsonWalk, "locate": jsonLocate, "update": jsonUpdate})


def replacer(content, sources=[], target=""):
    for source in sources:
        content = content.replace(source, target)
    return content


def multi_replacer(content, replacer_list=[[[], ""]]):
    for sources, target in replacer_list:
        content = replacer(content, sources=sources, target=target)
    return content


from pyjom.mathlib import extract_span, convoluted


import MediaInfo

import subprocess


def json_auto_float_int(jsonObj):
    jsonObj = jsonify(jsonObj)
    for location, content in jsonWalk(jsonObj):
        # content = jsonLocate(jsonObj,location)
        if type(content) == str:
            if "/" in content:
                try:
                    content = eval(content)  # could be dangerous!
                    if type(content) in [float, int]:
                        jsonUpdate(jsonObj, location=location, update_content=content)
                except:
                    pass
            elif "." in content:
                try:
                    content = float(content)
                    jsonUpdate(jsonObj, location=location, update_content=content)
                except:
                    pass
            else:
                try:
                    content = int(content)
                    jsonUpdate(jsonObj, location=location, update_content=content)
                except:
                    pass
    return jsonObj


def ffprobe_media_info(filename, video_size: Union[None, str] = None):
    cmd = "ffprobe{} -v quiet -print_format json -show_format -show_streams".format(
        " -video_size {}".format(video_size.strip()) if video_size else ""
    )
    cmd = cmd.split(" ")
    cmd = cmd + [filename]
    output = subprocess.check_output(cmd)
    return json_auto_float_int(json.loads(output))


def json_media_info(filename):
    cmd = ["mediainfo", "--Output=JSON", filename]
    output = subprocess.check_output(cmd)
    return json_auto_float_int(json.loads(output))


def get_media_info(filename):
    mdf = MediaInfo.MediaInfo(filename=filename)
    return json_auto_float_int(mdf.getInfo())


def getTextFileLength(path):
    with open(path, "r", encoding="utf-8") as f:
        return len(f.read())


def append_sublist(main_dict, sublist_key, item):
    main_dict[sublist_key] = main_dict.get(sublist_key, []) + [item]


def update_subdict(mdict, key, subdict):
    # print("UPDATING SUBDICT", mdict,key, subdict)
    if key not in mdict:
        mdict[key] = subdict
    else:
        mdict[key].update(subdict)
    return mdict


def read_json(filepath):
    with open(filepath, "r") as f:
        return json.loads(f.read())


def list_to_range(mlist, rangeLimit):
    mlist = set(mlist)
    mlist = list(sorted(mlist))
    currentRange = []
    lastElem = None
    myRanges = []
    for elem in mlist:
        if lastElem == None:
            lastElem = elem
            currentRange = [elem]
            continue
        myRange = elem - lastElem
        if rangeLimit >= myRange:
            lastElem = elem
            if len(currentRange) == 2:
                currentRange[1] = elem
            else:
                currentRange.append(elem)
        else:
            myRanges.append(currentRange)
            lastElem = elem
            currentRange = [elem]
    if len(myRanges) > 0:
        if myRanges[-1] != currentRange:
            myRanges.append(currentRange)
    else:
        myRanges.append(currentRange)
    return myRanges


# from youtube science.
def list_startswith(a, b):
    value = 0
    if len(a) < len(b):
        return False
    for i, v in enumerate(b):
        v0 = a[i]
        if v == v0:
            value += 1
    return value == len(b)


def list_endswith(a, b):
    value = 0
    if len(a) < len(b):
        return False
    c = a[-len(b) :]
    for i, v in enumerate(b):
        v0 = c[i]
        if v == v0:
            value += 1
    return value == len(b)


def cv2_HWC2CHW(frame):
    if len(frame.shape) == 3:
        img = frame[:, :, ::-1].transpose((2, 0, 1))
    else:
        img = frame[np.newaxis, :, :]
    return img


ocrCore = None
ocrConfig = {
    "use_angle_cls": True,
    "lang": "ch",
}  # it can detect english too. but no space included.


def configOCR(**kwargs):
    global ocrCore, ocrConfig
    if ocrCore is not None:
        if kwargs == ocrConfig:
            pass
    else:
        ocrConfig = kwargs
        from paddleocr import PaddleOCR

        # breakpoint()
        ocrCore = PaddleOCR(**kwargs)
        # breakpoint() # this is not the problem. maybe.
    return ocrCore


def getScriptFileBaseDir(script_file):
    basepath = os.path.abspath(script_file)
    basepath = basepath.replace(os.path.basename(basepath), "")
    return basepath


def getTemplateFileBaseDir(tmpDir="templates"):
    basedir = getScriptFileBaseDir(__file__)
    basedir = os.path.join(basedir, tmpDir)
    assert os.path.exists(basedir)
    return basedir


yolov5_model = None


@lru_cache(maxsize=1)
def configYolov5(model="yolov5s"):
    global yolov5_model  # not the same
    if yolov5_model == None:
        basedir = getTemplateFileBaseDir(tmpDir="models/yolov5")
        os.environ["YOLOV5_MODEL_DIR"] = basedir
        localModelPath = os.path.join(
            basedir, "ultralytics_yolov5_master/"
        )  # required to load it. we have modified this shit somehow.
        modelPath = model
        # we set enviorment variable instead.
        # breakpoint()
        yolov5_model = torch.hub.load(localModelPath, modelPath, source="local")
    return yolov5_model


def getTemplatePath(template_dirs, template_path):
    basedir = getTemplateFileBaseDir()
    for template_dir in template_dirs:
        basedir = os.path.join(basedir, template_dir)
        assert os.path.exists(basedir)
    template_path = os.path.join(basedir, template_path)
    assert os.path.exists(template_path)
    return template_path


def joinScriptFileBaseDir(script_file, local_file_path):
    basepath = getScriptFileBaseDir(script_file)
    file_path = os.path.join(basepath, local_file_path)
    return file_path


def renderTemplate(template, template_args, enable_json=True):
    template = jinja2.Template(template)
    if enable_json:
        for key in template_args.keys():
            data = template_args[key]
            if type(data) in [dict, list, tuple]:
                try:
                    data = json.dumps(data)
                    template_args[key] = data
                except:
                    pass
    script = template.render(**template_args)
    return script


def configDecorator(func, config="config.json"):
    def mytarget(*args, **kwargs):
        return func(*args, **(kwargs | {"config": config}))

    return mytarget


def jsonPrettyPrint(feedback, indent=4):
    assert type(indent) == int
    mtype = "json"
    feedback_type = type(feedback)
    if feedback_type != str:
        try:
            mfeedback_content = json.dumps(feedback, indent=indent)
        except:
            mfeedback_content = str(feedback)
            mtype = str(feedback_type)
    else:
        mfeedback_content = feedback
        mtype = "str"
    return mtype, mfeedback_content


def getFileType(fbase0):
    # quick dirty fix.
    # for gif we have a hard fix.
    translateTable = {"gif": "video"}  # force conversion.
    # print("FBASE:", fbase0)
    suffix = fbase0.split(".")[-1]
    guessedType = translateTable.get(suffix, None)
    # breakpoint()
    if guessedType:
        return guessedType
    mimestart = mimetypes.guess_type(fbase0)[0]
    if mimestart != None:
        mimestart = mimestart.split("/")[0]
        return mimestart
    return "unknown"


def getAbsoluteFilePath(fpath):
    assert os.path.exists(fpath)
    if os.path.isabs(fpath):
        return fpath
    return os.path.abspath(fpath)


def getFileExtension(fpath):
    basename = os.path.basename(fpath)
    assert "." in basename
    return basename.split(".")[-1]


def getLocalFileType(fpath):  # this is guessing, not file probing.
    fbase = os.path.basename(fpath)
    return getFileType(fbase)


def getHostname():
    return socket.gethostname()


def keywordDecorator(func, **kwargs2):
    def mytarget(*margs, **kwargs):
        if "trace_source" in kwargs.keys():
            if kwargs2["trace_source"]:
                return func(*margs, **(kwargs | kwargs2)), ".".join(
                    [__name__, func.__name__]
                )
        return func(*margs, **(kwargs | kwargs2))

    return mytarget


def decorator(func):
    def mytarget(*args, **kwargs):
        return func(*args, **kwargs), ".".join([__name__, func.__name__])

    return mytarget


def chineseDetector(string):
    base, celi = 0x4E00, 0x9FA5
    for elem in string:
        mydata = ord(elem)
        if mydata >= base and mydata <= celi:
            return True
    return False


def getTimestamp():
    return datetime.datetime.now().timestamp()


def dumpTrashDir(trash_dir):
    if os.path.exists(trash_dir):
        if os.path.isdir(trash_dir):
            shutil.rmtree(trash_dir)
        else:
            os.remove(trash_dir)


def writeFileWithPath(path, fname, content, mode, encoding=None):
    if not os.path.exists(path):
        os.makedirs(path)
    log_path = os.path.join(path, fname)
    if "b" not in mode:
        if encoding == None:
            with open(log_path, mode) as f:
                f.write(content)
        else:
            with open(log_path, mode, encoding=encoding) as f:
                f.write(content)
    else:
        with open(log_path, mode) as f:
            f.write(content)
    print("file written at:\n{}".format(log_path))
