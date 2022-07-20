background = 'tarot_pictures2/BLANK.jpg'
foreground = 'tarot_pictures2/ACE_OF_SWORDS.jpg'

import cv2
import numpy as np

pic1 = cv2.imread(background)
pic2 = cv2.imread(foreground)

h2,w2,c2 = pic2.shape

pic1.resize(h2,w2,c2)

# print(pic1.shape)
# print(pic2.shape)
pic1_b = cv2.cvtColor(pic1, cv2.COLOR_BGR2GRAY)
pic2_b = cv2.cvtColor(pic2, cv2.COLOR_BGR2GRAY)

pic3 = np.where(abs(pic1_b-pic2_b)<40, 0,255).astype(np.uint8)

cv2.imshow("mask",pic3)
cv2.waitKey(0)
# print(pic3)
# print(pic1.dtype)