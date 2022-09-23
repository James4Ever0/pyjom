import os
import cv2
import numpy
import BlurDetection

# img_path = raw_input("Please Enter Image Path: ")
img_path = "/root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png"
assert os.path.exists(img_path), "img_path does not exists"
img = cv2.imread(img_path)
img_fft, val, blurry = BlurDetection.blur_detector(img)
print("this image {0} blurry".format(["isn't", "is"][blurry]))
msk, val = BlurDetection.blur_mask(img)
BlurDetection.scripts.display('img', img)
BlurDetection.scripts.display('msk', msk)
cv2.waitKey(0)