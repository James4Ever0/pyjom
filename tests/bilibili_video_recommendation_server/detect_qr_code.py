image = "test_image_with_qr_code.png"

from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2

img = cv2.imread(image)
detector = cv2.QRCodeDetector()

data, bbox, _ = detector.detectAndDecode(img)

if bbox is not None:
    # display the image with lines
    # print(bbox)
    # breakpoint()
    for i in range(len(bbox)):
        # draw all lines
        
        for index in range(4):
            pt0 = tuple(bbox[i][index%4].astype(int))
            pt1 = tuple(bbox[i][index+1%4].astype(int))
            print(pt0)
            print(pt1)
            cv2.line(
                img,
                pt0,
                pt1,
                color=(255, 0, 0),
                thickness=2,
            )
    if data:
        print("[+] QR Code detected, data:", data)
# display the result
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
