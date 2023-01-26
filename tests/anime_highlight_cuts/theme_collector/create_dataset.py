import yaml

index.zfill(12)

train_path = "images/train"
test_path = "images/test"
data = {
    "path": "./pip_dataset",  # dataset root dir
    "train": train_path,  # train images (relative to 'path') 128 images
    "val": train_path,  # val images (relative to 'path') 128 images
    "test": test_path,
    "names": {0: "active_frame"},
}
import shutil
import os
os.makedirs()
