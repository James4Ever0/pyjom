import pixie
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2


def getImageW2H(image_path):
    height, width, _ = cv2.imread(image_path)
    w2h = width / height
    return w2h


ad_width, ad_height = 1000, 1000
font_path = "./wqy-microhei0.ttf"
cover_path = "sample_cover.jpg"
qrcode_path = "MyQRCode1.png"
play_button_path = "play_button.png"
bilibili_logo_path = "bilibili.png"
white = pixie.Color(1, 1, 1, 1)
image = pixie.Image(ad_width, ad_height)
# we are creating this, not replacing qr code.
image.fill(white)

# place the cover.
cover_w2h = getImageW2H(cover_path)
cover_width = int(ad_width*0.8)
cover_height = int(cover_width/cover_w2h)
cover = pixie.image


image.write_file("ad_2.png")
