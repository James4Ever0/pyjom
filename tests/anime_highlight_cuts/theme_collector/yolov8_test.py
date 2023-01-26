from ultralytics import YOLO

model = YOLO("ver2.pt")
imagePath ="simple_pip.png"
output = model(imagePath)
# print(output)
# breakpoint()

import cv2
image= cv2.imread(imagePath)
for xyxy in output[0].boxes.xyxy.numpy().astype(int).tolist():
    x0,y0, x1,y1 = xyxy
    cv2.rectangle(image,(x0, y0), (x1,y1), (0,0,255), thickness=1)
cv2.imshow("PIP", image)
cv2.waitKey(0)