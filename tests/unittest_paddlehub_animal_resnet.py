source = "" # check that kitty video!

from test_commons import *
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS
from pyjom.imagetoolbox import resizeImageWithPadding

import paddlehub as hub
import cv2

from lazero.utils.logger import sprint

classifier = hub.Module(name="resnet50_vd_animals")

for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
    padded_resized_frame = resizeImageWithPadding(
        frame, 224, 224, border_type="replicate"
    )
    result = classifier.classification(images=[padded_resized_frame])
    sprint("RESULT:", result)