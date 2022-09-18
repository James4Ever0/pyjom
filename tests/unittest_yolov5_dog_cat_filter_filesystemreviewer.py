from test_commons import *
from pyjom.modules.contentReviewer import filesystemReviewer
from pyjom.commons import keywordDecorator
from lazero.utils.logger import sprint

autoArgs = {
    "subtitle_detector": {"timestep": 0.2},
    "yolov5_detector": {"model": "yolov5x"},  # will this run? no OOM?
}

template_names = ["yolov5_detector.mdl.j2"]
semiauto = False
dummy_auto = False

reviewer = keywordDecorator(
    filesystemReviewer,
    auto=True,
    semiauto=semiauto,
    dummy_auto=dummy_auto,
    template_names=template_names,
    args={"autoArgs": autoArgs},
)
# videoPath = "/root/Desktop/works/pyjom/samples/image/dog_with_text2.png"
# fileList = [{"type": "image", "path": videoPath}]
videoPath = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.mp4"
fileList = [{"type": "video", "path": videoPath}]

resultGenerator, function_id = reviewer(
    fileList, generator=True, debug=True
)  # or at least a generator?


def extractYolov5DetectionData(detectionData, mimetype="video"):
    # plan to get some calculations!
    filepath, review_data = detectionData["review"]["review"]
    timeseries_data = review_data["yolov5_detector"]["yolov5"]["yolov5_detector"]
    data_dict = {}
    if mimetype == "video":
        dataList = []
        for frameData in timeseries_data:
            timestamp, frameNumber, frameDetectionData = [
                frameData[key] for key in ["time", "frame", "yolov5_detector"]
            ]
            sprint("timestamp:", timestamp)
            current_shot_detections = []
            for elem in frameDetectionData:
                location, confidence, identity = [
                    elem[key] for key in ["location", "confidence", "identity"]
                ]
                print("location:", location)
                print("confidence:", confidence)
                print("identity:", identity)
                current_shot_detections.append(
                    {
                        "location": location,
                        "confidence": confidence,
                        "identity": identity,
                    }
                )
            dataList.append(
                {"timestamp": timestamp, "detections": current_shot_detections}
            )
        data_dict.update({"data": dataList})
    else:
        frameDetectionData = timeseries_data
        current_shot_detections = []
        for elem in frameDetectionData:
            location, confidence, identity = [
                elem[key] for key in ["location", "confidence", "identity"]
            ]
            # print('location:', location)
            # print('confidence:', confidence)
            # print('identity:', identity)
        data_dict.update(
            {"data": current_shot_detections}
        )  # just detections, not a list in time series order
    data_dict.update({"path": filepath, "type": mimetype})
    return data_dict


def calculateVideoMaxDetectionConfidence(
    dataList, identities=["dog", "cat"]
):  # does it have a dog?
    report = {identity: 0 for identity in identities}
    for elem in dataList:
        detections = elem["detections"]
        for detection in detections:
            identity = detection["identity"]
            if identity in identities:
                if report[identity] < detection["confidence"]:
                    report[identity] = detection["confidence"]
    return report


from typing import Literal
import numpy as np


def calculateVideoMeanDetectionConfidence(
    dataList,
    identities=["dog", "cat"],
    framewise_strategy: Literal["mean", "max"] = "mean",
    timespan_strategy: Literal["max", "mean", "mean_no_missing"] = "mean_no_missing",
):
    report = {identity: [] for identity in identities}
    # report = {}
    for elem in dataList:  # iterate through selected frames
        detections = elem["detections"]
        frame_detection_dict_source = {}
        # frame_detection_dict = {key:[] for key in identities}
        for (
            detection
        ) in detections:  # in the same frame, iterate through different detections
            identity = detection["identity"]
            if identity in identities:
                frame_detection_dict_source[identity] = frame_detection_dict_source.get(
                    identity, []
                ) + [detection["confidence"]]
        frame_detection_dict = {}
        for key in identities:
            valueList = frame_detection_dict_source.get(key, [0])
            if framewise_strategy == "mean":
                frame_detection_dict.update({key: np.mean(valueList)})
            elif framewise_strategy == "max":
                frame_detection_dict.update({key: max(valueList)})
        # now update the report dict.
        for identity in identities:
            value = frame_detection_dict.get(identity, 0)
            if timespan_strategy == "mean_no_missing":
                if value == 0:
                    continue
            report[identity].append(value)
    final_report = {}
    for identity in identities:
        valueList = report.get(identity, [0])
        if timespan_strategy in ["mean_no_missing", "mean"]:
            final_report[identity] = np.mean(valueList)
        else:
            final_report[identity] = max(valueList)
    return final_report

from pyjom.commons import checkMinMaxDict

def detectionConfidenceFilter(detectionConfidence:dict, filter_dict = {'dog':{'min':0.5}}, logic:Literal['AND','OR']='OR'): # what is the logic here? and? or?
    for identity in filter_dict.keys():
        value = detectionConfidence.get(identity,0)
        key_filter = filter_dict[identity]
        result = checkMinMaxDict(value, key_filter)
        if result:
            if logic == 'OR':
                return True
        else:
            if logic == 'AND':
                return False
    return True # no matter what, if passed all the tests you can be sure to confirm this.
    # so either have dog or cat we will return True.

for result in resultGenerator:  # this is for each file.
    # sprint(result)
    detectionData = extractYolov5DetectionData(result, mimetype=fileList[0]["type"])
    print('DETECTION DATA:',detectiondata)
    detectionConfidence = calculateVideoMeanDetectionConfidence(detectionData)
    sprint("DETECTION CONFIDENCE:", detectionConfidence)
    filter_result = detectionConfidenceFilter(detectionConfidence)
    sprint("FILTER PASSED?", filter_result)
    # breakpoint()
