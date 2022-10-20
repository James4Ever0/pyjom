
# import sys
import cv2
# import imutils
from PIL import Image
from pyzbar.pyzbar import decode, ZBarSymbol

# @function 'detect_qr' detect and decode qrcode from frame using pyzbar lib
# @param 'inputFrame' type <class 'numpy.ndarray'>
# @return if detected type 'bool'
def detect_qr(inputFrame):
    img = Image.fromarray(inputFrame)
    decodedImg = decode(img, symbols=[ZBarSymbol.QRCODE])
    # it reads the content. but where is the code?
    print('total %d qrcode detected',len(decodedImg))
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
image = "output_qrcode2.png"

inputImage = cv2.imread(image)
# frame = imutils.resize(inputImage, width=400)
print(detect_qr(inputImage))

# fantastic.

# usually there should be no more than 1 qrcode in image to allow user to scan the code in qq.