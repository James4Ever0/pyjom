import yaml

index.zfill(12)

train_path = ""images/train""
test_path = "images/test"
data = {
"path": "./pip_dataset",  # dataset root dir
"train": ,  # train images (relative to 'path') 128 images
"val": "images/train",  # val images (relative to 'path') 128 images
"test": "images/test",

"names":
  {0: "active_frame"}
  }