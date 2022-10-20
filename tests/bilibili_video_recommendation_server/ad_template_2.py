import pixie
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2


def getImageW2H(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
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
cover_width = int(ad_width * 0.9)
cover_height = int(cover_width / cover_w2h)
cover_round_corner_radius = int(ad_width * 0.05)
cover = pixie.read_image(cover_path)
cover = cover.resize(cover_width, cover_height)
cover_mask = pixie.Mask(cover_width, cover_height)
cover_mask_path = pixie.Path()
cover_mask_path.rounded_rect(
    0, 0, cover_width, cover_height, *([cover_round_corner_radius] * 4)
)
cover_mask.fill_path(cover_mask_path)
cover.mask_draw(cover_mask)


cover_transform_width = cover_transform_height =int((ad_width- cover_width)/2)
cover_transform = pixie.translate(cover_transform_width, cover_transform_height)

cover_shadow = cover.shadow(
    offset = pixie.Vector2(2, 2),
    spread = 2,
    blur = 10,
    color = pixie.Color(0, 0, 0, 0.78125)
)

image.draw(cover_shadow)
image.draw(cover, cover_transform)

image.write_file("ad_2.png")
