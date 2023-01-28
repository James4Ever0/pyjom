import yaml

# why you are taking so much RAM?

## suggest that you label some (many) still image and mark out the picture-in-picture parts from it? about 2000 images?

## man just make sure these pictures are not "pip" so we can put borders and arrange them randomly to create our super dataset. use MSCOCO/coco128?

train_path = "images/train"
test_path = "images/test"

train_label_path = "labels/train"
test_label_path = "labels/test"

basepath = "pip_dataset"


data = {
    "path": f"../{basepath}",  # dataset root dir
    "train": train_path,  # train images (relative to 'path')
    "val": train_path,  # val images (relative to 'path')
    "test": test_path,
    "names": {0: "active_frame"},
}


import os

os.system(f"rm -rf {basepath}")

index = 1

os.makedirs(os.path.join(basepath, train_path), exist_ok=True)
os.makedirs(os.path.join(basepath, test_path), exist_ok=True)

os.makedirs(os.path.join(basepath, train_label_path), exist_ok=True)
os.makedirs(os.path.join(basepath, test_label_path), exist_ok=True)

with open("pip_dataset/pip_dataset.yaml", "w+") as f:
    f.write(yaml.dump(data, default_flow_style=False))

import cv2
import pandas

csvNames = [fpath for fpath in os.listdir(".") if fpath.endswith(".csv")]

import progressbar

remainder = 7 # changed? heck?
for csvName in csvNames:
    dataframe = pandas.read_csv(csvName)
    videoFileName = f'{csvName.split(".")[0]}.mp4'
    #
    frameIndex = 0
    cap = cv2.VideoCapture(videoFileName)
    myIterator = progressbar.progressbar(dataframe.iterrows())
    frame_height, frame_width = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(
        cv2.CAP_PROP_FRAME_WIDTH
    )
    while True:
        succ, image = cap.read()
        nextRow = next(myIterator, None)
        if nextRow is None:
            break
        if succ:
            frameIndex += 1
            if frameIndex % remainder != 0:
                continue
            _, _, min_x, min_y, w, h = nextRow[1].tolist()
            if (min_x, min_y, w, h) == (0, 0, 0, 0) or w == 0 or h == 0:
                continue
            index += 1
            imageName = f'{f"{index}".zfill(12)}.png'
            labelName = f'{f"{index}".zfill(12)}.txt'

            dataPoints = [
                (min_x + w / 2) / frame_width,
                (min_y + h / 2) / frame_height,
                w / frame_width,
                h / frame_height,
            ]
            with open(os.path.join(basepath, train_label_path, labelName), "w+") as f:
                content = " ".join((["0"] + [f"{number:.3f}" for number in dataPoints]))
                f.write(content)
            cv2.imwrite(os.path.join(basepath, train_path, imageName), image)
            del image
        else:
            break
    cap.release()
    del cap
    del dataframe

testVideo = "output.mp4"
w, h = 1152, 648
min_x, min_y = 384, 216

print("creating 4min pip dataset")

cap = cv2.VideoCapture(testVideo)
frame_height, frame_width = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(
    cv2.CAP_PROP_FRAME_WIDTH
)

dataPoints = [
    (min_x + w / 2) / frame_width,
    (min_y + h / 2) / frame_height,
    w / frame_width,
    h / frame_height,
]
frameCounter = 0
while True:
    succ, image = cap.read()
    if succ:
        frameCounter += 1
        if frameCounter % remainder != 0:
            continue
        index += 1

        imageName = f'{f"{index}".zfill(12)}.png'
        labelName = f'{f"{index}".zfill(12)}.txt'

        with open(os.path.join(basepath, train_label_path, labelName), "w+") as f:
            content = " ".join((["0"] + [f"{number:.3f}" for number in dataPoints]))
            f.write(content)
        cv2.imwrite(os.path.join(basepath, train_path, imageName), image)
        del image
    else:
        break

cap.release()
del cap
print("creating reference dataset")

testVideo = "output_1.mp4"

cap = cv2.VideoCapture(testVideo)
frame_height, frame_width = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(
    cv2.CAP_PROP_FRAME_WIDTH
)

dataPoints = [0.5, 0.5, 1, 1]
frameCounter = 0

while True:
    succ, image = cap.read()
    if succ:
        frameCounter += 1
        if frameCounter % remainder != 0:
            continue
        index += 1

        imageName = f'{f"{index}".zfill(12)}.png'
        labelName = f'{f"{index}".zfill(12)}.txt'

        with open(os.path.join(basepath, train_label_path, labelName), "w+") as f:
            content = " ".join((["0"] + [f"{number:.3f}" for number in dataPoints]))
            f.write(content)
        cv2.imwrite(os.path.join(basepath, train_path, imageName), image)
        del image
    else:
        break

cap.release()
del cap

print("dataset created.")
