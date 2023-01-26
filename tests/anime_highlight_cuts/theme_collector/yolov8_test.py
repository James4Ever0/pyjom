from ultralytics import YOLO

model = YOLO("genesis.pt")

output = model("simple_pip.png")
# print(output)
# breakpoint()

import cv2
for xyxy in output[0].boxes.xyxy.numpy().astype(int).tolist():
    x0,y0, x1,y1 = xyxy
    cv2.rec