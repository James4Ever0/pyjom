# sample few images from a video.
import random
## we import our version of cv2 here? or uninstall and reinstall opencv-python with custom things?

import pathlib
import sys
site_path = pathlib.Path("/usr/local/lib/python3.9/site-packages")
cv2_libs_dir = site_path / 'cv2' / f'python-{sys.version_info.major}.{sys.version_info.minor}'
print(cv2_libs_dir)
cv2_libs = sorted(cv2_libs_dir.glob("*.so"))
if len(cv2_libs) == 1:
    print("INSERTING:",cv2_libs[0].parent)
    sys.path.insert(1, str(cv2_libs[0].parent))

import cv2
import progressbar as pb

videoPaths = [
    "/root/Desktop/works/pyjom/tests/still_watermark_auto_removal/kunfu_cat.mp4", # bilibili animal video compilation
    "/root/Desktop/works/pyjom/tests/bilibili_practices/bilibili_video_translate/japan_day.webm", # youtube animation with watermark
    "/root/Desktop/works/pyjom/samples/video/LiGHT3ZCi.mp4", # animal video compilation with pip and large area of watermark
]  # his watermark. scorpa.
video_path = videoPaths[2]
# will change this shit.
# shall we downscale this thing?

# video = cv2.
# video_path = ""
# long loading time since we are backing up.

sample_count = 60

video_cap = cv2.VideoCapture(video_path)

fps = video_cap.get(cv2.CAP_PROP_FPS)  # 60.
frame_count = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(frame_count)

sample_indexs = [x for x in range(frame_count)]
sample_indexs = random.sample(sample_indexs, sample_count)
# import copy

imageSet = []

for frame_index_counter in pb.progressbar(range(frame_count)):  # are you sure?
    success, frame = video_cap.read()
    if not success:
        break
    if frame_index_counter in sample_indexs:
        imageSet.append(frame.copy())

from src import *

gx, gy, gxlist, gylist = estimate_watermark_imgSet(imageSet)
# print(len(imageSet))
cropped_gx, cropped_gy, watermark_location = crop_watermark(gx, gy, location=True)
W_m = poisson_reconstruct(cropped_gx, cropped_gy)

W_full = poisson_reconstruct(gx, gy)

print(cropped_gx.shape, cropped_gy.shape, W_m.shape)  # (50, 137, 3) may vary.
print(watermark_location)  # ((1022, 21), (1072, 158)) inverted x,y! hell.

# cv2.imshow("WATERMARK",W_m)
# cv2.imshow("WATERMARK_FULL",W_full)
# # remove the freaking watermark please?
# cv2.waitKey(0)

# east_net = "/media/root/help/pyjom/tests/still_watermark_auto_removal/EAST-Detector-for-text-detection-using-OpenCV-master/frozen_east_text_detection.pb"

# net = cv2.dnn.readNet(east_net)
# H,W = W_full.shape[:2]

# newH = (H//32)*32
# newW = (W//32)*32

# rH, rW = H/float(newH), W/float(newW)
# W_full = cv2.resize(W_full,(newW,newH))
maxval, minval = np.max(W_full), np.min(W_full)
W_full = (W_full - minval) * (255 / (maxval - minval))  # is that necessary?
# # print(,W_full.shape,W_full.dtype)
W_full = W_full.astype(np.uint8)
# # breakpoint()
# newH,newW = W_full.shape[:2]
# # 14.122540090957173 -17.575702620638673 (1080, 1920, 3) float64
# # you even have negative values. what the fuck?
# blob = cv2.dnn.blobFromImage(W_full, 1.0, (newW, newH), (123.68, 116.78, 103.94), swapRB=True, crop=False)
# # start = time.time()
# net.setInput(blob)
# layerNames = [
# 	"feature_fusion/Conv_7/Sigmoid",
# 	"feature_fusion/concat_3"]
# (scores, geometry) = net.forward(layerNames)

# def decode_predictions(scores, geometry,min_confidence=0.5):
# 	# grab the number of rows and columns from the scores volume, then
# 	# initialize our set of bounding box rectangles and corresponding
# 	# confidence scores
# 	(numRows, numCols) = scores.shape[2:4]
# 	rects = []
# 	confidences = []
# 	# loop over the number of rows
# 	for y in range(0, numRows):
# 		# extract the scores (probabilities), followed by the
# 		# geometrical data used to derive potential bounding box
# 		# coordinates that surround text
# 		scoresData = scores[0, 0, y]
# 		xData0 = geometry[0, 0, y]
# 		xData1 = geometry[0, 1, y]
# 		xData2 = geometry[0, 2, y]
# 		xData3 = geometry[0, 3, y]
# 		anglesData = geometry[0, 4, y]
# 		# loop over the number of columns
# 		for x in range(0, numCols):
# 			# if our score does not have sufficient probability,
# 			# ignore it
# 			if scoresData[x] < min_confidence:
# 				continue
# 			# compute the offset factor as our resulting feature
# 			# maps will be 4x smaller than the input image
# 			(offsetX, offsetY) = (x * 4.0, y * 4.0)
# 			# extract the rotation angle for the prediction and
# 			# then compute the sin and cosine
# 			angle = anglesData[x]
# 			cos = np.cos(angle)
# 			sin = np.sin(angle)
# 			# use the geometry volume to derive the width and height
# 			# of the bounding box
# 			h = xData0[x] + xData2[x]
# 			w = xData1[x] + xData3[x]
# 			# compute both the starting and ending (x, y)-coordinates
# 			# for the text prediction bounding box
# 			endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
# 			endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
# 			startX = int(endX - w)
# 			startY = int(endY - h)
# 			# add the bounding box coordinates and probability score
# 			# to our respective lists
# 			rects.append((startX, startY, endX, endY))
# 			confidences.append(scoresData[x])
# 	# return a tuple of the bounding boxes and associated confidences
# 	return (rects, confidences)

# (rects, confidences) = decode_predictions(scores, geometry)

# from imutils.object_detection import non_max_suppression

# boxes = non_max_suppression(np.array(rects), probs=confidences)

# rW=rH=1

# no box painting.
# for (startX, startY, endX, endY) in boxes:
#     # scale the bounding box coordinates based on the respective
#     # ratios
#     startX = int(startX * rW)
#     startY = int(startY * rH)
#     endX = int(endX * rW)
#     endY = int(endY * rH)
#     # draw the bounding box on the frame
#     cv2.rectangle(W_full, (startX, startY), (endX, endY), (0, 255, 0), 2)
# # you could implement your own watermark detector network so far. it is easy.
# # maybe directly using optical flow and gradients will be prettier?

# W_full
src = W_full
scale_percent = 50

# calculate the 50 percent of original dimensions
width = int(src.shape[1] * scale_percent / 100)
height = int(src.shape[0] * scale_percent / 100)

# dsize
dsize = (width, height)

# resize image
output = cv2.resize(src, dsize)

gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

gray_output = cv2.GaussianBlur(gray_output, (11, 3), 0)

thresh_output = cv2.adaptiveThreshold(
    gray_output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)

thresh_output = 255 - thresh_output

# cnts, hierachy = cv2.findContours(thresh_output,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # really freaking bad. we should invert this.
cnts, hierachy = cv2.findContours(
    thresh_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)  # really freaking bad. we should invert this.
# cv2.RETR_EXTERNAL

[a, b] = output.shape[:2]
myMask = np.zeros(shape=[a, b], dtype=np.uint8)

# this is for video watermarks. how about pictures? do we need to cut corners? how to find the freaking watermark again?
for cnt in cnts:
    x, y, w, h = cv2.boundingRect(cnt)  # Draw the bounding box image=
    # cv2.rectangle(output, (x,y), (x+w,y+h), (0,0,255),2)
    cv2.rectangle(myMask, (x, y), (x + w, y + h), 255, -1)

dilated_mask = cv2.GaussianBlur(myMask, (11, 11), 0)
cv2.threshold(dilated_mask, 256 / 2, 255, cv2.THRESH_BINARY, dilated_mask)
cnts2, hierachy2 = cv2.findContours(
    dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

myMask2 = np.zeros(shape=[a, b], dtype=np.uint8)

# this is for video watermarks. how about pictures? do we need to cut corners? how to find the freaking watermark again?

height, width = myMask2.shape[:2]
rectangles = []

for cnt in cnts2:
    x, y, w, h = cv2.boundingRect(cnt)  # Draw the bounding box image=
    # cv2.rectangle(output, (x,y), (x+w,y+h), (0,0,255),2)
    rectangles.append((x,y,w,h))
    cv2.rectangle(myMask2, (x, y), (x + w, y + h), 255, -1)

import json
data = {"canvas":(width, height), 'rectangles':rectangles}
dataString = json.dumps(data)
with open("test.json", 'w+') as f: f.write(dataString)

print("TOTAL {} CONTOURS.".format(len(cnts2)))  # paint those contours.

# cv2.imshow("IMAGE",thresh_output)
cv2.imshow("MPICTURE", myMask2)
cv2.waitKey(0)

# fill those areas and you will get it.
# how do we remove this shit?
# also how do we remove other weird things? like floating watermarks?

# print(imageSet[0].shape)
# breakpoint()
