from ultralytics import YOLO

## yolov8 tracking needs special ultralytics version. it is been updated too damn often. you need to downgrade.
## https://github.com/mikel-brostrom/yolov8_tracking
## this might add unwanted overheads. warning!

# no one will miss `genesis.pt`, right?

model = YOLO("general_ver1.pt")
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

imagePaths = [fpath for fpath in os.listdir(".") if fpath.split(".")[-1].lower() in ('jpg','jpeg','png')]

import cv2

for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    output = model(image)
    for xyxy in output[0].boxes.xyxy.numpy().astype(int).tolist():
        x0, y0, x1, y1 = xyxy
        area = 
        cv2.rectangle(image, (x0, y0), (x1, y1), (0, 0, 255), thickness=10)
    cv2.imshow("PIP", image)
    cv2.waitKey(0)
