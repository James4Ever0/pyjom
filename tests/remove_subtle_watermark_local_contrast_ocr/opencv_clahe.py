# https://www.geeksforgeeks.org/clahe-histogram-eqalization-opencv/

import cv2
# import numpy as np

# Reading the image from the present directory
color_image = cv2.imread("IWWS.jpeg")
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
colorimage_b = clahe_model.apply(colorimage[:,:,0])
colorimage_g = clahe_model.apply(colorimage[:,:,1])
colorimage_r = clahe_model.apply(colorimage[:,:,2])

# Ordinary thresholding the same image
# _, ordinary_img = cv2.threshold(image_bw, 155, 255, cv2.THRESH_BINARY)

# Showing all the three images
# cv2.imshow("ordinary threshold", ordinary_img)
# cv2.imshow("CLAHE image", final_img)
cv2.imwrite("clahe_image.jpeg", final_img)