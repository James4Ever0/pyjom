import torch
import os
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

# Model
localModelDir = '/root/Desktop/works/pyjom/pyjom/models/yolov5/ultralytics_yolov5_master/'
# import os
os.environ["YOLOV5_MODEL_DIR"] = '/root/Desktop/works/pyjom/pyjom/models/yolov5/' # this is strange. must be a hack in the localModelDir
model = torch.hub.load(localModelDir, 'yolov5s',source="local")  # or yolov5m, yolov5l, yolov5x, custom

# Images
img = '/media/root/help/pyjom/samples/image/miku_on_green.png'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
# results.print() # or .show(),
results.save()
# print(type(results),dir(results))
# breakpoint()
import cv2
image = cv2.imread("runs/detect/exp3/miku_on_green.jpg")
cv2.imshow("NONE",image)
# results.print()  # or .show(),
# hold it.
# image 1/1: 720x1280 1 bird # what the fuck is a bird?
# os.system("pause")
# input()

# this shit has been detected but not in the right category.