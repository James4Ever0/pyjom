from ultralytics import YOLO

model = YOLO("best.pt")

output = model("000000003099.png")
print(output)
breakpoint()