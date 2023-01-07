images = ['/root/Desktop/works/pyjom/samples/image/qrcode_test/no_qrcode.webp','/root/Desktop/works/pyjom/samples/image/qrcode_test/with_qrcode.jpg']

qrcode_path = ""

from ad_template_2_functional import removeAndInsertQRCode
import cv2

for img in images:
    output = removeAndInsertQRCode(img, qrcode_path, None)
    cv2.imshow("IMG", output)
    cv2.waitKey(0)