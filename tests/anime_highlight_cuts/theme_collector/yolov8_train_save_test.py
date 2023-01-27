from ultralytics import YOLO

# pip install opencv-python==4.5.5.64
# shit?
# https://github.com/asweigart/pyautogui/issues/706

model = YOLO("yolov8n.pt")
# print(model)
# model.to('mps')
# The operator 'aten::_slow_conv2d_forward' is not current implemented for the MPS device.
# fuck.

# breakpoint()
import rich

train_result = model.train(epochs=3, data="./pip_dataset/pip_dataset.yaml")

print("TRAIN RESULT?")
rich.print(train_result)

val_result = model.val()

print("VALIDATION RESULT?")
rich.print(val_result)

test_result = model("./pip_dataset/images/test/000000003099.png")
test_boxes = test_result[0].boxes

test_classes, test_xywh, test_confidence = (
    test_boxes.cls.numpy(),
    test_boxes.xywh.numpy(), # the xy in this xywh means the center of the bounding box.
    test_boxes.conf.numpy(),
)

print("XYWH?", test_xywh)
print("CLASSES?", test_classes)
print("CONFIDENCE?", test_confidence)

# model.export(format="pytorch", path="./pip_detector.pth")
