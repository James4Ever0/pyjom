from ultralytics import YOLO

## yolov8 tracking needs special ultralytics version. it is been updated too damn often. you need to downgrade.
## https://github.com/mikel-brostrom/yolov8_tracking
## this might add unwanted overheads. warning!

# no one will miss `genesis.pt`, right?

model = YOLO("general_ver1.pt")
## TODO: create dataset to prevent detection of pure color/gradient borders
# model = YOLO("ver3.pt")

# find trained weights on huggingface:
# https://huggingface.co/James4Ever0/yolov8_pip_ultralytics


# imagePaths = [
#     "000000003099.png",
#     "simple_pip.png",
#     "no_border_0.jpg",
#     "has_border_0.jpg",
#     "has_border_1.jpg",
#     "has_border_2.jpg",
# ]

import os

imagePaths = [
    fpath
    for fpath in os.listdir(".")
    if fpath.split(".")[-1].lower() in ("jpg", "jpeg", "png")
]

import cv2

frameRatioFilters = [(16 / 9, 0.2, "landscape")]

frameAreaThreshold = 0.15
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    output = model(image)
    height, width, _ = image.shape
    center = (width / 2, height / 2)
    # print("CENTER:",center)
    candidates = []
    for xyxy in output[0].boxes.xyxy.numpy().astype(int).tolist():
        x0, y0, x1, y1 = xyxy
        currentFrameWidth = x1 - x0
        currentFrameHeight = y1 - y0
        currentFrameArea = currentFrameWidth * currentFrameHeight
        # area filter? a must.
        if currentFrameArea / (height * width) < frameAreaThreshold:
            continue
        else:
            # filter out malformed frames? just for anime?
            currentFrameRatio = currentFrameWidth / currentFrameHeight
            if all(
                [
                    (
                        currentFrameRatio < frameRatioStandard - frameRatioMargin
                        or currentFrameRatio > frameRatioStandard + frameRatioMargin
                    )
                    for frameRatioStandard, frameRatioMargin, _ in frameRatioFilters
                ]
            ):
                continue
            candidates.append((x0, y0, x1, y1))

    # sort it by area, then by centrality?

    candidates.sort(
        key=lambda points: -(points[2] - points[0]) * (points[3] - points[1])
    )
    # print("SORT_AREA:", [(points[2] - points[0]) * (points[3] - points[1]) for points in candidates])
    candidates = candidates[:2]
    candidates.sort(
        key=lambda points: (((points[2] + points[0]) / 2) - center[0]) ** 2
        + (((points[3] + points[1]) / 2) - center[1]) ** 2
    )
    # print("SORT_CENTRALITY:", [(((points[2] + points[0]) / 2) - center[0]) ** 2
    # + (((points[3] + points[1]) / 2) - center[1]) ** 2 for points in candidates])
    if len(candidates) > 0:
        print("main frame found.")
        x0, y0, x1, y1 = candidates[0]
        cv2.rectangle(image, (x0, y0), (x1, y1), (0, 0, 255), thickness=10)
    else:
        print("no main frame found.")
    cv2.imshow("PIP", image)
    cv2.waitKey(0)
