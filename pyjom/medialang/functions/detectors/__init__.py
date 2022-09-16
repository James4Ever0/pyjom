# from pyjom.medialang.functions.detectors.mediaDetector import *
from .blackoutDetector import *
from .subtitleDetector import *
from .videoDiffDetector import *
from .yolov5_Detector import *
from .frameborder_Detector import *

# maybe these shits are gonna ruin my life...

def getMedialangInputFixed(medialangPathsInput):
    for fbase0 in medialangPathsInput:
        if type(fbase0) == str:
            yield fbase0
        elif type(fbase0) == list and len(fbase0) == 1 and type(fbase0[0] == dict) and 'cache' in fbase0[0].keys():
            yield fbase0[0]['cache']
        else:
            print('weird medialang detector input')
            print(fbase0)
        # then it must be the medialang shit.

def processInputWrapperFunction(function,wrapperFunction, *args, **kwargs):

medialangDetectors = {
    "subtitle_detector": mediaSubtitleDetector,
    "framediff_detector": videoDiffDetector,
    "blackout_detector": blackoutDetector,
    "yolov5_detector": yolov5_Detector,
    "frameborder_detector": frameborder_Detector,
}
