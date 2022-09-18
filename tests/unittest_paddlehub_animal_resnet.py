source = ""

from test_commons import *
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS
from pyjom.imagetoolbox import resizeImageWithPadding

for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
    padded_resized_frame = resizeImageWithPadding(
        frame, 224, 224, border_type="replicate"
    )