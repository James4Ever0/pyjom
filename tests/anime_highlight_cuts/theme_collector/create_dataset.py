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
    # f"{index}".zfill(12)
    cap = cv2.VideoCapture(videoFileName)
    ...
    cap.release()

testVideo = "output.mp4"
w, h = 1152, 648
x, y = 384, 216

