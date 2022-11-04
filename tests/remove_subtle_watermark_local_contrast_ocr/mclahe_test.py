import mclahe
import cv2


colorimage = cv2.imread("IWWS.jpeg")
# print(colorimage.shape)

k = (30,30,)
colorimage_clahe = mclahe.mclahe(colorimage,kernel_size=k)

# cv2.imwrite("clahe_image.jpeg", colorimage_clahe)
