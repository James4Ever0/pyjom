from ultralytics import YOLO

model = YOLO("genesis.pt")

output = model("simple_pip.png")
# print(output)
# breakpoint()