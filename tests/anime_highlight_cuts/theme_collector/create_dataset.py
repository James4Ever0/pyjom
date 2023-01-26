import yaml

index.zfill(12)

train_path = "images/train"
test_path = "images/test"
train_label_path = "labels/train"
test_label_path = "labels/test"
basepath = "./pip_dataset"
data = {
    "path": basepath,  # dataset root dir
    "train": train_path,  # train images (relative to 'path') 128 images
    "val": train_path,  # val images (relative to 'path') 128 images
    "test": test_path,
    "names": {0: "active_frame"},
}
import os

os.makedirs(os.path.join(basepath, train_path), exist_ok=True)
os.makedirs(os.path.join(basepath, test_path), exist_ok=True)

os.makedirs(os.path.join(basepath, train_label_path), exist_ok=True)
os.makedirs(os.path.join(basepath, test_label_path), exist_ok=True)
