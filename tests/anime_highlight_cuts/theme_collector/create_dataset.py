import yaml

index.zfill(12)
data = {
"path": "./pip_dataset",  # dataset root dir
"train": "images/train",  # train images (relative to 'path') 128 images
"val": "images/train",  # val images (relative to 'path') 128 images
"test": "images/test",

"names":
  {0: "active_frame"}