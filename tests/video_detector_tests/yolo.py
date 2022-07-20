image_path = "../../samples/video/dog_with_text.mp4"

import cv2
video = cv2.VideoCapture(image_path)

for _ in range(100):
    ret, frame = video.read() # first frame is blackout!

import torch

# don't really know how paddleocr recognize chars.
localModelDir = '/root/Desktop/works/pyjom/pyjom/models/yolov5/ultralytics_yolov5_master/'
import os
os.environ["YOLOV5_MODEL_DIR"] = '/root/Desktop/works/pyjom/pyjom/models/yolov5/'
model = torch.hub.load(localModelDir, 'yolov5s',source="local") # the yolov5s.pt file is required when loading the model.

# Image
# img = 'https://ultralytics.com/images/zidane.jpg'
img = frame[:,:,::-1].transpose((2,0,1))

# Inference
# reshape this shit.
# img = np.reshape()
results = model(img) # pass the image through our model

df = results.pandas().xyxy[0]
print(df)

data = []
for index,line in df.iterrows():
    # print(line)
    left = (line["xmin"],line["ymin"])
    right = (line["xmax"],line["ymax"])
    confidence = line["confidence"]
    class_ = line["class"]
    name = line["name"]
    data.append({"location":[left,right],"confidence":confidence,"identity":{"class":class_,"name":name}})
print(data)
cv2.imshow("name",frame)
cv2.waitKey(0)
# found the freaking dog!