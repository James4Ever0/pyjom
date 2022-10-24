# this is to make it look better than before
# maybe.

alipay_link = "https://qr.alipay.com/tsx10243tdewwaxrvullge8"
wechat_link = (
    "wxp://f2f0V92qUQI0aBO5PXtWezujxMm-C1KFub6qCi1Obt3cn1KjZqDPqoWKn8ICCcwdt8zU"
)

from generate_qr_code import makeAndSaveQrcode

qrcode_path = "test_ebegging.png"
makeAndSaveQrcode(alipay_link, qrcode_path)

# now we plan to draw this thing.
# how big is the canvas? no fill?

import pixie

font_path = "./wqy-microhei0.ttf"
ad_height = 1000
ad_width = 700
night_mode = False
qrcode_scan_text = "支付宝投喂"
output_path = "ebegging_template.png"
ocean_blue = pixie.parse_color("#0A3CCF")
grass_green = pixie.parse_color("#00A619")

qrcode_stroke_paint = ocean_blue_paint  # for alipay

image = pixie.Image(ad_width, ad_height)

qrcode = pixie.read_image(qrcode_path)
qrcode_width = qrcode_height = int(0.9 * ad_width)
qrcode = qrcode.resize(qrcode_width, qrcode_height)


font = pixie.read_font(font_path)
font.size = int(qrcode_width * 0.04)
if night_mode:
    font.paint.color = pixie.Color(1, 1, 1, 1)
else:
    font.paint.color = pixie.Color(0, 0, 0, 1)

qrcode_scan_text_transform_x = int(ad_width - qrcode_width * 1.1 - font.size * 1)
qrcode_scan_text_transform = pixie.translate(
    qrcode_scan_text_transform_x + qrcode_width, int(ad_height - qrcode_height * 1.1)
)
image.fill_text(font, qrcode_scan_text, transform=qrcode_scan_text_transform)

qrcode_transform = pixie.translate(
    int(ad_width - qrcode_width * 1.1 - font.size * 1.2),
    int(ad_height - qrcode_height * 1.1),
)


qrcode_rounded_corner = int(0.05 * 0.3 * qrcode_width)
qrcode_stroke_path = pixie.Path()
qrcode_stroke_path.rounded_rect(
    0, 0, qrcode_width, qrcode_height, *([qrcode_rounded_corner] * 4)
)


stroke_param = 50
stroke_width = int(qrcode_width / stroke_param)
image.stroke_path(
    qrcode_stroke_path,
    qrcode_stroke_paint,
    qrcode_transform,
    stroke_width=stroke_width,
)

qrcode_mask = pixie.Mask(qrcode_width, qrcode_width)
qrcode_mask.fill_path(qrcode_stroke_path)
qrcode.mask_draw(qrcode_mask)

image.draw(qrcode, qrcode_transform)

image.write_file(output_path)
