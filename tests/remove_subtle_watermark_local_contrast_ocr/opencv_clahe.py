# https://www.geeksforgeeks.org/clahe-histogram-eqalization-opencv/

## highly unstable. do not use.

import cv2
import numpy as np

# Reading the image from the present directory
colorimage = cv2.imread("IWWS.jpeg")
# Resizing the image for compatibility
# image = cv2.resize(image, (500, 600))
# why?

# The initial processing of the image
# image = cv2.medianBlur(image, 3)
# image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# The declaration of CLAHE
# clipLimit -> Threshold for contrast limiting
clahe_model = cv2.createCLAHE(clipLimit = 5)

# you may use grayscale image for the luminosity output.
# final_img = clahe.apply(image)

# For ease of understanding, we explicitly equalize each channel individually
# colorimage_b = clahe_model.apply(colorimage[:,:,0])
# colorimage_g = clahe_model.apply(colorimage[:,:,1])
# colorimage_r = clahe_model.apply(colorimage[:,:,2])


img = cv2.cvtColor(img, cv2.COLOR_RGB2Lab)

#configure CLAHE
clahe = cv2.createCLAHE(clipLimit=10,tileGridSize=(8,8))

#0 to 'L' channel, 1 to 'a' channel, and 2 to 'b' channel
img[:,:,0] = clahe.apply(img[:,:,0])

img = cv2.cvtColor(img, cv2.COLOR_Lab2RGB)

# colorimage_clahe = np.stack((colorimage_b,colorimage_g,colorimage_r), axis=2)

# Ordinary thresholding the same image
# _, ordinary_img = cv2.threshold(image_bw, 155, 255, cv2.THRESH_BINARY)

# Showing all the three images
# cv2.imshow("ordinary threshold", ordinary_img)
# cv2.imshow("CLAHE image", final_img)
cv2.imwrite("clahe_image.jpeg", colorimage)