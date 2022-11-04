import mclahe
import cv2


colorimage = cv2.imread("IWWS.jpeg")
# print(colorimage.shape)

k = (30,30,3)
colorimage_clahe = mclahe.mclahe(colorimage,kernel_size=k,n_bins=400,adaptive_hist_range=True)

cv2.imwrite("clahe_image.jpeg", colorimage_clahe)
