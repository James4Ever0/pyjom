import mclahe
import cv2


colorimage = cv2.imread("IWWS.jpeg")
# print(colorimage.shape)

# k = (30,30,3)
colorimage_clahe = mclahe.mclahe(colorimage,n_bins=400,adaptive_hist_range=False)

cv2.imwrite("clahe_image_mclahe.jpeg", colorimage_clahe)
