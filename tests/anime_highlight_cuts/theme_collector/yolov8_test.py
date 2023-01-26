from ultralytics import YOLO

model = YOLO("best.pt")

model("000000003099.png")