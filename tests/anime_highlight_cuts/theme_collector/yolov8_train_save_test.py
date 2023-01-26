from ultralytics import YOLO
# pip install opencv-python==4.5.5.64
# shit?
# https://github.com/asweigart/pyautogui/issues/706

model = YOLO("yolov8n.pt")
# print(model)

# breakpoint()
model.train(epochs=3,data="./pip_dataset/pip_dataset.yaml")
model.val()