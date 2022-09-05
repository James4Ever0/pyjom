# motion detectors are used to track objects. though you may want to separate objects with it.
import numpy as np
import cv2
import pybgs as bgs

# suspect by static image analysis, and then create bounding box over the thing.
# check image quality.

# for donga, you must change the framerate to skip identical frames.

# also donga have strange things you may dislike, e.g.: when only part of the image changes.

algorithm = bgs.FrameDifference() # this is not stable since we have more boundaries. shall we group things?
# can we use something else? 
video_file = "../../samples/video/LiEIfnsvn.mp4" # this one with cropped boundaries. 

capture = cv2.VideoCapture(video_file)
while not capture.isOpened():
  capture = cv2.VideoCapture(video_file) 
  cv2.waitKey(1000)
  print("Wait for the header")

pos_frame = capture.get(1)
while True:
  flag, frame = capture.read()
  
  if flag:
    pos_frame = capture.get(1)
    img_output = algorithm.apply(frame)
    img_bgmodel = algorithm.getBackgroundModel()
    _, contours = cv2.findContours(img_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # maybe you should merge all active areas.
    if contours is not None:
            # continue
        counted = False
        for contour in contours:
            [x, y, w, h] = cv2.boundingRect(img_output)
            if not counted:
                min_x, min_y = x,y
                max_x, max_y = x+w, y+h
                counted = True
            else:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x+w)
                max_y = max(max_y, y+h)
                # only create one single bounding box.
        cv2.rectangle(frame,(min_x,min_y),(max_x,max_y), (255,0,0), 2)
        # how to stablize this shit?
    cv2.imshow('video', frame)
    
    cv2.imshow('img_output', img_output)
    cv2.imshow('img_bgmodel', img_bgmodel)

  else:
    cv2.waitKey(1000)
    break
  
  if 0xFF & cv2.waitKey(10) == 27:
    break
  

cv2.destroyAllWindows()
