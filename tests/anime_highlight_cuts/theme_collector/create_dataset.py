from email import iterators
from xml.dom.expatbuilder import InternalSubsetExtractor
import yaml


train_path = "images/train"
test_path = "images/test"

train_label_path = "labels/train"
test_label_path = "labels/test"

basepath = "./pip_dataset"
data = {
    "path": basepath,  # dataset root dir
    "train": train_path,  # train images (relative to 'path')
    "val": train_path,  # val images (relative to 'path')
    "test": test_path,
    "names": {0: "active_frame"},
}

with open("pip_video.yaml", "w+") as f:
    f.write(yaml.dump(data, default_flow_style=False))

import os

index = 1

os.makedirs(os.path.join(basepath, train_path), exist_ok=True)
os.makedirs(os.path.join(basepath, test_path), exist_ok=True)

os.makedirs(os.path.join(basepath, train_label_path), exist_ok=True)
os.makedirs(os.path.join(basepath, test_label_path), exist_ok=True)

import cv2
import pandas

csvNames = [fpath for fpath in os.listdir(".") if fpath.startswith(".csv")]

for csvName in csvNames:
    dataframe = pandas.read_csv(csvName)
    videoFileName = f'{csvName.split(".")[0]}.mp4'
    #
    frameIndex = 0
    cap = cv2.VideoCapture(videoFileName)
    myIterator = dataframe.iterrows()
    frame_height, frame_width = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(
        cv2.CAP_PROP_FRAME_WIDTH
    )
    while True:
        succ, image = cap.read()
        nextRow = next(myIterator, None)
        if nextRow is None:
            break
        if succ:
            index += 1
            frameIndex += 1
            imageName = f'{f"{index}".zfill(12)}.png'
            labelName = f'{f"{index}".zfill(12)}.txt'
            _, _, x, y, w, h = nextRow[1].tolist()

dataPoints = [x / frame_width,
                                y / frame_height,
                                w / frame_width,
                                h / frame_height,]
            with open(os.path.join(basepath, train_label_path, labelName), "w+") as f:
                content = " ".join(
                    (
                        [0]
                        + [
                            f"{number:.3f}"
                            for number in dataPoints
                        ]
                    )
                )
                f.write(content)
            cv2.imwrite(os.path.join(basepath, train_path, imageName), image)
        else:
            break
    cap.release()

testVideo = "output.mp4"
w, h = 1152, 648
x, y = 384, 216


cap = cv2.VideoCapture(testVideo)
frame_height, frame_width = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(
    cv2.CAP_PROP_FRAME_WIDTH
)

dataPoints = [x / frame_width,
                                y / frame_height,
                                w / frame_width,
                                h / frame_height,]
while True:
    succ, image = cap.read()
    if succ:
        index += 1
    else:
        break

cap.release()
