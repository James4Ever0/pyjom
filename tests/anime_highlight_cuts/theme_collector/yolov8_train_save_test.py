from ultralytics import YOLO
# pip install opencv-python==4.5.5.64
# shit?
# https://github.com/asweigart/pyautogui/issues/706

model = YOLO("yolov8n.pt")
# print(model)

# breakpoint()
import rich
train_result = model.train(epochs=3,data="./pip_dataset/pip_dataset.yaml")

print("TRAIN RESULT?")
rich.print(train_result)

val_result =model.val()

print("VALIDATION RESULT?")
rich.print(val_result)

model("./pip_dataset/images/test")


model.export(format='pytorch',path='./pip_detector.pth')