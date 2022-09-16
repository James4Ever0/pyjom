# from pyjom.medialang.functions.detectors.mediaDetector import *
from .blackoutDetector import *
from .subtitleDetector import *
from .videoDiffDetector import *
from .yolov5_Detector import *
from .frameborder_Detector import *

# maybe these shits are gonna ruin my life...
medialangDetectors = {
    "subtitle_detector": mediaSubtitleDetector,
    "framediff_detector": videoDiffDetector,
    "blackout_detector": blackoutDetector,
    "yolov5_detector": yolov5_Detector,
    "frameborder_detector": frameborder_Detector,
}
