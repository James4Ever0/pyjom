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
videoPath = "/root/Desktop/works/pyjom/samples/image/dog_with_text2.png"
fileList = [{"type": "image", "path": videoPath}]
# videoPath = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.mp4"
# fileList = [{"type": "video", "path": videoPath}]

resultGenerator, function_id = reviewer(
    fileList, generator=True, debug=True
)  # or at least a generator?

def extractYolov5DetectionData(detectionData, mimetype='video'):
    # plan to get some calculations!
    filepath, review_data = detectionData['review']['review']
    timeseries_data = review_data['yolov5_detector']['yolov5']['yolov5_detector']
    if mimetype == 'video':
        for frameData in timeseries_data:
            timestamp, frameNumber, frameDetectionData = [frameData[key] for key in ['time','frame','yolov5_detector']]
            sprint('timestamp:', timestamp)
            for elem in frameDetectionData:
                location, confidence, identity = [elem[key] for key in ['location','confidence','identity']]
                print('location:', location)
                print('confidence:', confidence)
                print('identity:', identity)
    else:
        frameDetectionData = timeseries_data
        for elem in frameDetectionData:
            location, confidence, identity = [elem[key] for key in ['location','confidence','identity']]
            print('location:', location)
            print('confidence:', confidence)
            print('identity:', identity)

for result in resultGenerator:
    from lazero.utils.logger import sprint
    # sprint(result)
    extractYolov5DetectionData(result, mimetype=fiieList[0]['type'])
    breakpoint()
