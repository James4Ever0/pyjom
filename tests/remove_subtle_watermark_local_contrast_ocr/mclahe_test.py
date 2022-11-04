import mclahe
import cv2


colorimage = cv2.imread("IWWS.jpeg")

colorimage_clahe = mclahe.mclahe(colorimage,kernel_size=)

cv2.imwrite("clahe_image.jpeg", colorimage_clahe)
