import mclahe
import cv2


colorimage = cv2.imread("IWWS.jpeg")
# print(colorimage.shape)

k = (30,30,1)
colorimage_clahe = mclahe.mclahe(colorimage, kernel_size=k) # not working! what the fuck?

cv2.imwrite("clahe_image_mclahe.jpeg", colorimage_clahe)
