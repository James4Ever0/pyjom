from ultralytics import YOLO

model = YOLO("genesis.pt")

output = model("000000003099.png")
print(output)
breakpoint()