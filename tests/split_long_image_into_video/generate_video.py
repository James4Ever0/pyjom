# to get a proper cover, let's simply crop.

# to find a proper title for this video, extract keywords, generate title and find the best cover by embeddings.

# first, get picture aspect.

import cv2
d = cv2.imread("long_and_funny_image_about_ai_painting.jpg")
# print(d.shape)
height, width, channels = d.shape
# very high, low width.
# calculate actual output?
mheight, mwidth = 1080,1920