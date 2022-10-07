# motion detectors are used to track objects. though you may want to separate objects with it.
import numpy as np
import cv2
import pybgs as bgs

# suspect by static image analysis, and then create bounding box over the thing.

# check image quality.

algorithm = bgs.FrameDifference() # track object we need that.
# algorithm = bgs.SuBSENSE()
# video_file = "../../samples/video/highway_car.avi"
# video_file = "../../samples/video/dog_with_text.mp4"
video_file = "../../samples/video/LiEIfnsvn.mp4" # this one with cropped boundaries. 
# video_file = "../../samples/video/LlfeL29BP.mp4"

# maybe we should consider something else to crop the thing? or not?
# accumulate the delta over time to see the result?
# use static detection method.

capture = cv2.VideoCapture(video_file)
while not capture.isOpened():
  capture = cv2.VideoCapture(video_file)
  cv2.waitKey(1000)
  print("Wait for the header")

#pos_frame = capture.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
#pos_frame = capture.get(cv2.CV_CAP_PROP_POS_FRAMES)
pos_frame = capture.get(1)
while True:
  flag, frame = capture.read()
  
  if flag:
    cv2.imshow('video', frame)
    #pos_frame = capture.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
    #pos_frame = capture.get(cv2.CV_CAP_PROP_POS_FRAMES)
    pos_frame = capture.get(1)
    #print str(pos_frame)+" frames"
    
    img_output = algorithm.apply(frame)
    img_bgmodel = algorithm.getBackgroundModel()
    
    cv2.imshow('img_output', img_output)
    cv2.imshow('img_bgmodel', img_bgmodel)

  else:
    #capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
    #capture.set(cv2.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
    #capture.set(1, pos_frame-1)
    #print "Frame is not ready"
    cv2.waitKey(1000)
    break
  
  if 0xFF & cv2.waitKey(10) == 27:
    break
  
  #if capture.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
  #if capture.get(cv2.CV_CAP_PROP_POS_FRAMES) == capture.get(cv2.CV_CAP_PROP_FRAME_COUNT):
  #if capture.get(1) == capture.get(cv2.CV_CAP_PROP_FRAME_COUNT):
    #break

cv2.destroyAllWindows()
