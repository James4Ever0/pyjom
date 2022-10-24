# this is to make it look better than before
# maybe.

# according to the blend mode, that guy seems to be using some special blend mode to hide his qrcode from being detected. so you may want to do the same when you add this to your own picture.

alipay_link = "https://qr.alipay.com/tsx10243tdewwaxrvullge8"
wechat_link = (
    "wxp://f2f0V92qUQI0aBO5PXtWezujxMm-C1KFub6qCi1Obt3cn1KjZqDPqoWKn8ICCcwdt8zU"
)


from generate_qr_code import makeAndSaveQrcode

qrcode_path = "test_ebegging.png"

# now we plan to draw this thing.
# how big is the canvas? no fill?

import pixie

font_path = "./wqy-microhei0.ttf"
ad_height = 800
ad_width = 700
night_mode = True
style_mode = True
output_path = "ebegging_template.png"
# white = pixie.Color(1, 1, 1, 1)
# black = pixie.Color(0, 0, 0, 1)
background_opacity = 1

def makeColorAndPaintFromColorCode(color_code: str):
    assert len(color_code) == 6 + 1 and color_code.startswith("#")
    color = pixie.parse_color(color_code)
    paint = pixie.Paint(pixie.SOLID_PAINT)
    paint.color = color
    return color, paint


ocean_blue, ocean_blue_paint = makeColorAndPaintFromColorCode("#0A3CCF")
grass_green, grass_green_paint = makeColorAndPaintFromColorCode("#00A619")
white, white_paint = makeColorAndPaintFromColorCode("#FFFFFF")
black, black_paint = makeColorAndPaintFromColorCode("#000000")


styleSuites = {
    "alipay":{
        'paint':ocean_blue_paint,
        'qrcode':alipay_link,
        'text':"支付宝投喂"
    },
    'wechat':{
        'paint':grass_green_paint,
        'qrcode':wechat_link,
        'text':"微信投喂"
    }
}

# selected_style_suite = styleSuites['wechat']
selected_style_suite = styleSuites['alipay']


qrcode_link = selected_style_suite['qrcode']
makeAndSaveQrcode(qrcode_link, qrcode_path)


qrcode_stroke_paint = selected_style_suite['paint']  # for alipay
qrcode_scan_text = selected_style_suite['text']

image = pixie.Image(ad_width, ad_height)

qrcode = pixie.read_image(qrcode_path)
qrcode_width = qrcode_height = int(0.9 * ad_width)
qrcode = qrcode.resize(qrcode_width, qrcode_height)


qrcode_rounded_corner = int((0.05 / 0.3) * qrcode_width)
qrcode_stroke_path = pixie.Path()
qrcode_stroke_path.rounded_rect(
    0, 0, qrcode_width, qrcode_height, *([qrcode_rounded_corner] * 4)
)


qrcode_width_margin = int((ad_width - qrcode_width) / 2)
qrcode_height_margin = int(ad_height - qrcode_height - qrcode_width_margin)

ebegging_mask_path = pixie.Path()
ebegging_mask_path.rounded_rect(
    0, 0, ad_width, ad_height, *([int(qrcode_rounded_corner*1.2)] * 4)
)

if not style_mode:
    if not night_mode:
        fill_paint = white_paint
    else:
        fill_paint = black_paint
else:
    fill_paint = qrcode_stroke_paint

import copy
fill_paint = copy.deepcopy(fill_paint)
fill_paint.color = copy.deepcopy(fill_paint.color)
fill_paint.opacity = background_opacity

image.fill_path(
    ebegging_mask_path, fill_paint
)

# fill the ebegging ad with appropriate color first

font = pixie.read_font(font_path)
font.size = int(
    qrcode_width * (0.04 / 0.3)
)  # questionable. we shall check the font size.

if not style_mode:
    if night_mode:
        font.paint.color = white
        # font.paint.color = qrcode_stroke_paint.color
    else:
        # font.paint.color = qrcode_stroke_paint.color
        font.paint.color = black
else:
    font.paint.color = white

text_bound_x = ad_width
text_bound_y = qrcode_height_margin

image.fill_text(
    font,
    qrcode_scan_text,
    bounds=pixie.Vector2(text_bound_x, text_bound_y),
    h_align=pixie.CENTER_ALIGN,
    v_align=pixie.MIDDLE_ALIGN,
)

qrcode_transform = pixie.translate(
    qrcode_width_margin,
    qrcode_height_margin,
)


stroke_param = 100 / 3
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