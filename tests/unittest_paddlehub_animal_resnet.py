source = "/root/Desktop/works/pyjom/samples/video/kitty_flash_15fps.gif" # check that kitty video!

from test_commons import *
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS
from pyjom.imagetoolbox import resizeImageWithPadding

import paddlehub as hub
import cv2

from lazero.utils.logger import sprint

classifier = hub.Module(name="resnet50_vd_animals")
# 'ResNet50vdAnimals' object has no attribute 'gpu_predictor'
# no gpu? really?
for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
    padded_resized_frame = resizeImageWithPadding(
        frame, 224, 224, border_type="replicate"
    )
    result = classifier.classification(images=[padded_resized_frame],top_k=3,use_gpu=False) # check it?
    sprint("RESULT:", result)
    breakpoint()