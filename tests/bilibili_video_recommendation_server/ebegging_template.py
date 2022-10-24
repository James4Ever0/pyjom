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
ad_height = 850
ad_width = 700
night_mode = False
qrcode_scan_text = "支付宝投喂"
output_path = "ebegging_template.png"


def makeColorAndPaintFromColorCode(color_code: str):
    assert len(color_code) == 6 + 1 and color_code.startswith("#")
    color = pixie.parse_color(color_code)
    paint = pixie.Paint(pixie.SOLID_PAINT)
    paint.color = color
    return color, paint


ocean_blue, ocean_blue_paint = makeColorAndPaintFromColorCode("#0A3CCF")
grass_green, grass_green_paint = makeColorAndPaintFromColorCode("#00A619")

qrcode_stroke_paint = ocean_blue_paint  # for alipay

image = pixie.Image(ad_width, ad_height)

qrcode = pixie.read_image(qrcode_path)
qrcode_width = qrcode_height = int(0.9 * ad_width)
qrcode = qrcode.resize(qrcode_width, qrcode_height)


qrcode_rounded_corner = int((0.05 /0.3)* qrcode_width)
qrcode_stroke_path = pixie.Path()
qrcode_stroke_path.rounded_rect(
    0, 0, qrcode_width, qrcode_height, *([qrcode_rounded_corner] * 4)
)

ebegging_mask_path = pixie.Path()
ebegging_mask_path.rounded_rect(0,0,ad_width,ad_height,*([qrcode_rounded_corner] * 4))

image.fill_path(ebedding_mask_path, )

# fill the ebegging ad with appropriate color first

font = pixie.read_font(font_path)
font.size = int(qrcode_width * (0.04/0.3)) # questionable. we shall check the font size.

if night_mode:
    font.paint.color = white
else:
    font.paint.color = black

text_bound_x = ad_width
text_bound_y = ad_height-ad_width

image.fill_text(font, qrcode_scan_text, bounds=pixie.Vector2(text_bound_x, text_bound_y),h_align = pixie.CENTER_ALIGN, v_align=pixie.MIDDLE_ALIGN)

qrcode_transform = pixie.translate(
    int((ad_width - qrcode_width)/2),
    int(ad_height - ad_width),
)


stroke_param = 100/3
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
