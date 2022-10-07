from mmflow.apis import init_model, inference_model
from mmflow.datasets import visualize_flow, write_flow
import mmcv

# Specify the path to model config and checkpoint file
config_id = 0

if config_id == 0:
    config_file = 'flownet2cs_8x1_slong_flyingchairs_384x448.py'
    checkpoint_file = 'flownet2cs_8x1_slong_flyingchairs_384x448.pth'
elif config_id == 1:
    config_file = 'gma_8x2_120k_mixed_368x768.py' # damn slow.
    checkpoint_file = 'gma_8x2_120k_mixed_368x768.pth'
# build the model from a config file and a checkpoint file
model = init_model(config_file, checkpoint_file, device='cuda:0')

# test image pair, and save the results

import cv2

video_file = "/media/root/help/pyjom/samples/video/dog_with_text.mp4"

video = cv2.VideoCapture(video_file)

ret, img = video.read()
prevImg = img.copy()

counter = 0
while True:
    ret, img = video.read()
    if img is None: break
    else:
        frame1 = prevImg
        # frame1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        frame2 = img # why freaking grayscale?
        result = inference_model(model, frame1,frame2)
        prevImg = img.copy()
        flow_map = visualize_flow(result,None)
        cv2.imshow("flowmap",flow_map)
    if cv2.waitKey(20) == ord("q"):
        break
        # can also do canny edge detection.