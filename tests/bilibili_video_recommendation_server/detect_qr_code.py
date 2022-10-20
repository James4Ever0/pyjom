image = "test_image_with_qr_code.png"

from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()
import cv2

img = cv2.imread(image)
detector = cv2.QRCodeDetector()

data, bbox, _ = detector.detectAndDecode(img)

if bbox is not None:
    # display the image with lines
    for i in range(len(bbox)):
        # draw all lines
        cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
    if data:
        print("[+] QR Code detected, data:", data)
# display the result
cv2.imshow("img", img)  
cv2.waitKey(0)
cv2.destroyAllWindows()