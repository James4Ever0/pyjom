from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()
import blur_detector
import cv2
imagePath = "/root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png"

if __name__ == '__main__':
    img = cv2.imread(imagePath,0)
    blur_map = blur_detector.detectBlur(img, downsampling_factor=4, num_scales=4, scale_start=2, num_iterations_RF_filter=3)
    cv2.imshow('ori_img', img)
    cv2.imshow('blur_map', blur_map)
    cv2.waitKey(0)