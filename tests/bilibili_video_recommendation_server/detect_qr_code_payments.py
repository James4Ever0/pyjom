# image = "test_image_with_qr_code.png"
# fail to obtain the qrcode.
# but we might want use our original qrcode.
# image = "output_qrcode2.png"
images=['alipay_payment_code.png','wechat_payment_code.jpg']


# qrcodes:
# https://qr.alipay.com/tsx10243tdewwaxrvullge8
# wxp://f2f0V92qUQI0aBO5PXtWezujxMm-C1KFub6qCi1Obt3cn1KjZqDPqoWKn8ICCcwdt8zU

# they are both long urls. which one is effective in qq?

from lazero.utils.importers import cv2_custom_build_init

from PIL import Image
from pyzbar.pyzbar import decode, ZBarSymbol

# @function 'detect_qr' detect and decode qrcode from frame using pyzbar lib
# @param 'inputFrame' type <class 'numpy.ndarray'>
# @return if detected type 'bool'
def detect_qr(inputFrame):
    img = Image.fromarray(inputFrame)
    decodedImg = decode(img, symbols=[ZBarSymbol.QRCODE])
    # it reads the content. but where is the code?
    print('total %d qrcode detected' % len(decodedImg))
    # breakpoint()
    # length: 2

    if len(decodedImg) > 0:
        for code in decodedImg:
            decodedBytes = code.data
            stringData = decodedBytes.decode("utf-8")
            print("QRCode content:")
            print(stringData)
            polygon = code.polygon
            print('POLYGON CONTENT:')
            print(polygon)

        return True
    else:
        return False

cv2_custom_build_init()
import cv2
for image in images:
# shit! for picture with 2 qrcodes it fails to detect.
# bbox return None
    img = cv2.imread(image)
    result=detect_qr(img)
    print("RESULT:", result)
    print("_"*20)