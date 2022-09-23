import blur_detector
from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()
import cv2
imagePath = 
if __name__ == '__main__':
    img = cv2.imread(imagePath)
    blur_map = blur_detector.detectBlur(img, downsampling_factor=4, num_scales=4, scale_start=2, num_iterations_RF_filter=3)
    cv2.imshow('ori_img', img)
    cv2.imshow('blur_map', blur_map)
    cv2.waitKey(0)