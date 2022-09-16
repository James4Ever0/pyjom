# from pyjom.medialang.functions.detectors.mediaDetector import *
from .blackoutDetector import *
from .subtitleDetector import *
from .videoDiffDetector import *
from .yolov5_Detector import *
from .frameborder_Detector import *

# maybe these shits are gonna ruin my life...

def getMedialangInputFixed(medialangPathsInput):
    for fbase0 in medialangPathsInput:
        if type(fbase0) == list and len(fbase0) == 1:
            if type(fbase0[0] == dict)
        # then it must be the medialang shit.

medialangDetectors = {
    "subtitle_detector": mediaSubtitleDetector,
    "framediff_detector": videoDiffDetector,
    "blackout_detector": blackoutDetector,
    "yolov5_detector": yolov5_Detector,
    "frameborder_detector": frameborder_Detector,
}
