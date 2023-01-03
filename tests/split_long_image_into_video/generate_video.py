# to get a proper cover, let's simply crop.

# to find a proper title for this video, extract keywords, generate title and find the best cover by embeddings.

# first, get picture aspect.

import cv2

def getWidthHeight(impath):
    d = cv2.imread(impath)
    # print(d.shape)
    height, width, channels = d.shape
    return width, height

im0 = "long_and_funny_image_about_ai_painting.jpg"
im1 = "intermediate.png"
# very high, low width.
# calculate actual output?
mheight, mwidth = 1080,1920
width, height = getWidthHeight(im0)
import ffmpeg
ffmpeg.input(im0).