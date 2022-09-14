from pyjom.config import *
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

# this is root. this is not site-packages.

def checkMinMaxDict(value, minMaxDict):
    minVal = minMaxDict['min']
    minVal = minMaxDict['min']

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



def waitForServerUp(port, message, timeout=1):
    import requests

    while True:
        try:
            url = "http://localhost:{}".format(port)
            r = requests.get(url, timeout=timeout)
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


def jsonify(jsonObj):
    return json.loads(json.dumps(jsonObj))


def jsonWalk(jsonObj, location=[]):
    # this is not tuple. better convert it first?
    # mlocation = copy.deepcopy(location)
    if type(jsonObj) == dict:
        for key in jsonObj:
            content = jsonObj[key]
            if type(content) not in [dict, list, tuple]:
                yield location + [key], content
            else:
                # you really ok with this?
                for mkey, mcontent in jsonWalk(content, location + [key]):
                    yield mkey, mcontent
    elif type(jsonObj) in [
        list,
        tuple,
    ]:  # this is not pure JSON. we only have list and dicts.
        for key, content in enumerate(jsonObj):
            # content = jsonObj[key]
            if type(content) not in [dict, list, tuple]:
                yield location + [key], content
            else:
                for mkey, mcontent in jsonWalk(content, location + [key]):
                    yield mkey, mcontent
    else:
        raise Exception("Not a JSON compatible object: {}".format(type(jsonObj)))


def jsonWalk2(jsonObj):
    jsonObj = jsonify(jsonObj)
    return jsonWalk(jsonObj)


def jsonLocate(jsonObj, location=[]):
    # print("object:",jsonObj)
    # print("location:",location)
    if location != []:
        # try:
        return jsonLocate(jsonObj[location[0]], location[1:])
        # except:
        #     breakpoint()
    return jsonObj


def jsonUpdate(jsonObj, location=[], update_content=None):
    if location != []:
        if type(jsonObj) == dict:
            target = {
                location[0]: jsonUpdate(
                    jsonObj[location[0]],
                    location=location[1:],
                    update_content=update_content,
                )
            }
            # print("keys:", location)
            # print("JSONOBJ:", jsonObj)
            # print("update target:", target)
            jsonObj.update(target)
            return jsonObj
        elif type(jsonObj) == list:
            target = jsonUpdate(
                jsonObj[location[0]],
                location=location[1:],
                update_content=update_content,
            )
            # print("keys:", location)
            # print("JSONOBJ:", jsonObj)
            # print("override target:", target)
            jsonObj[location[0]] = target
            return jsonObj
        else:
            raise Exception("Unsupported JSON update target type:", type(jsonObj))
    return update_content


json.__dict__.update({"walk": jsonWalk, "locate": jsonLocate, "update": jsonUpdate})


def replacer(content, sources=[], target=""):
    for source in sources:
        content = content.replace(source, target)
    return content


def multi_replacer(content, replacer_list=[[[], ""]]):
    for sources, target in replacer_list:
        content = replacer(content, sources=sources, target=target)
    return content


from itertools import groupby


def extract_span(mlist, target=0):
    counter = 0
    spanList = []
    target_list = [(a, len(list(b))) for a, b in groupby(mlist)]
    for a, b in target_list:
        nextCounter = counter + b
        if a == target:
            spanList.append((counter, nextCounter))
        counter = nextCounter
    return spanList


def convoluted(array, k=2, pad=0):  # simple convolution. no tail.
    pad_size = k - 1
    new_array = [pad] * pad_size + array
    result = []
    for i in range(len(array)):
        sliced = new_array[i : i + k]
        value = sum(sliced) / k
        result.append(value)
    return result


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


def ffprobe_media_info(filename):
    cmd = "ffprobe -v quiet -print_format json -show_format -show_streams".split(" ")
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
    return json.loads(open(filepath, "r").read())


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
        return func(*args, **kwargs, config=config)

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


def getFileType(fbase):
    mimestart = mimetypes.guess_type(fbase)[0]
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
                return func(*margs, **kwargs, **kwargs2), ".".join(
                    [__name__, func.__name__]
                )
        return func(*margs, **kwargs, **kwargs2)

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
