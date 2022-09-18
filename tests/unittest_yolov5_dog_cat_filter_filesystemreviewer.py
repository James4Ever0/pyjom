from test_commons import *
from pyjom.modules.contentReviewer import filesystemReviewer
from pyjom.commons import keywordDecorator

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

def extractYolov5DetectionData(detectionData, mimetype='video'):
    # plan to get some calculations!
    filepath, review_data = detectionData['review']['review']
    timeseries_data = review_data['yolov5_detector']['yolov5']['yolov5_detector']
    data_dict = {}
    if mimetype == 'video':
        dataList = []
        for frameData in timeseries_data:
            timestamp, frameNumber, frameDetectionData = [frameData[key] for key in ['time','frame','yolov5_detector']]
            sprint('timestamp:', timestamp)
            current_shot_detections = []
            for elem in frameDetectionData:
                location, confidence, identity = [elem[key] for key in ['location','confidence','identity']]
                print('location:', location)
                print('confidence:', confidence)
                print('identity:', identity)
                current_shot_detections.append({'location':location, 'confidence':confidence, 'identity':identity})
            dataList.append({'timestamp':timestamp,'detections':current_shot_detections})
        data_dict.update({'data':dataList})
    else:
        frameDetectionData = timeseries_data
        current_shot_detections = []
        for elem in frameDetectionData:
            location, confidence, identity = [elem[key] for key in ['location','confidence','identity']]
            # print('location:', location)
            # print('confidence:', confidence)
            # print('identity:', identity)
        data_dict.update({'data':current_shot_detections}) # just detections, not a list in time series order
    data_dict.update({'path':filepath,'type':mimetype})
    return data_dict

def calculateVideoMaxDetectionConfidence(dataList, identities=['dog','cat']): # does it have a dog?
    report = {identity:0 for identity in identities}
    for elem in dataList:
        detections = elem['detections']
        for detection in detections:
            identity = detection['identity']
            if identity in identities:
                if report[identity] < detection['confidence']:
                    report[identity] = detection['confidence']
    return report
from typing import Literal
import numpy as np
def calculateVideoMeanDetectionConfidence(dataList, identities=['dog','cat'], framewise_strategy:Literal['mean','max']='mean', timespan_strategy:Literal['max','mean','mean_no_missing']='mean_no_missing'):
    report = {identity:[] for identity in identities}
    # report = {}
    for elem in dataList: # iterate through selected frames
        detections = elem['detections']
        frame_detection_dict = {}
        # frame_detection_dict = {key:[] for key in identities}
        for detection in detections: # in the same frame, iterate through different detections
            identity = detection['identity']
            if identity in identities:
                frame_detection_dict[identity] = frame_detection_dict.get(identity,[])+[detection['confidence']]
        if framewise_strategy == 'mean':
            frame_detection_dict = {key: np.mean(frame_detection_dict.get(key,[0])) for key in identities}
        elif framewise_strategy == 'max':
            frame_detection_dict = {key: max(frame_detection_dict.get(key,[0])) for key in identities}
        # now update the report dict.
            for identity in identities:
                value = frame_detection_dict.get(identity,0)
                if timespan_strategy == 'mean_no_missing':
                
                report[identity].append(value)
            for identity in identities:
                


for result in resultGenerator: # this is for each file.
    from lazero.utils.logger import sprint
    # sprint(result)
    extractYolov5DetectionData(result, mimetype=fileList[0]['type'])
    # breakpoint()
