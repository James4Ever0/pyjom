import pixie
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2


def getImageW2H(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    w2h = width / height
    return w2h

night_mode = True
ad_width, ad_height = 1000, 1000
font_path = "./wqy-microhei0.ttf"
font_bold_path = "./wqy-microhei1.ttf"
cover_path = "sample_cover.jpg"
qrcode_path = "MyQRCode1.png"
play_button_path = "play_white_b.png"
# play_button_path = "play_b.png"
bilibili_logo_path = "bili_white_b_cropped.png"

play_count = comment_count = danmaku_count = "1万"
# one extra space.
stats_text = " {}播放 {}评论 {}弹幕".format(play_count, comment_count, danmaku_count)
qrcode_scan_text = "\n"+"\n".join(list("扫码观看"))
title_text = "真·朋克！揭秘《赛博朋克2077》屏幕之外的魔幻换弹操作"
white = pixie.Color(1, 1, 1, 1)
black = pixie.Color(0,0,0, 1)
image = pixie.Image(ad_width, ad_height)
# we are creating this, not replacing qr code.
if night_mode:
    image.fill(black)
else:
    image.fill(white)

# place the cover.
cover_w2h = getImageW2H(cover_path)
cover_width = int(ad_width * 0.9)
cover_height = int(cover_width / cover_w2h)
cover_round_corner_radius = int(ad_width * 0.05)
cover = pixie.read_image(cover_path)
cover = cover.resize(cover_width, cover_height)
# cover gradient.

paint = pixie.Paint(pixie.LINEAR_GRADIENT_PAINT)

paint.gradient_handle_positions.append(pixie.Vector2(100,int(cover_height)*0.8))
paint.gradient_handle_positions.append(pixie.Vector2(100, cover_height))

paint.gradient_stops.append(pixie.ColorStop(pixie.Color(0, 0, 0, 0), 0))
paint.gradient_stops.append(pixie.ColorStop(pixie.Color(0, 0, 0, 1), 1))

cover_mask_path = pixie.Path()
cover_mask_path.rounded_rect(
    0, 0, cover_width, cover_height, *([cover_round_corner_radius] * 4)
)
path = cover_mask_path
cover.fill_path(path, paint)



cover_mask = pixie.Mask(cover_width, cover_height)

cover_mask.fill_path(cover_mask_path)
cover.mask_draw(cover_mask)


cover_transform_width = cover_transform_height = int((ad_width - cover_width) / 2)
cover_transform = pixie.translate(cover_transform_width, cover_transform_height)

cover_stroke_paint = pixie.Paint(pixie.SOLID_PAINT)
cover_stroke_paint.color = pixie.parse_color("#FC427B")
image.stroke_path(
    cover_mask_path,
    cover_stroke_paint,
    cover_transform,
    stroke_width=int(ad_width / 100),
)
image.draw(cover, cover_transform)

# now place the bilibili logo.

bilibili_logo = pixie.read_image(bilibili_logo_path)
bilibili_logo_w2h = getImageW2H(bilibili_logo_path)
bilibili_logo_width = int(ad_width * 0.2)
bilibili_logo_height = int(bilibili_logo_width / bilibili_logo_w2h)
bilibili_logo = bilibili_logo.resize(bilibili_logo_width, bilibili_logo_height)

bilibili_logo_transform = pixie.translate(
    cover_transform_width+int(bilibili_logo_height/8), int(cover_transform_width +(bilibili_logo_height/4))
)
# bilibili_logo_transform = pixie.translate(
#     cover_transform_width, 0
# )
image.draw(bilibili_logo, bilibili_logo_transform)

# now place the play button.

play_button = pixie.read_image(play_button_path)
play_button_w2h = getImageW2H(play_button_path)
play_button_width = play_button_height = int(ad_width * 0.2)
play_button = play_button.resize(play_button_width, play_button_height)

play_button_transform = pixie.translate(
    int(cover_transform_width + (cover_width - play_button_width) / 2),
    int(cover_transform_width + (cover_height - play_button_height) / 2),
)
image.draw(play_button, play_button_transform)

# place some stats.

font = pixie.read_font(font_path)
font.size = int(ad_width*0.04)
font.paint.color = pixie.Color(1,1,1,1)
stats_transform = pixie.translate(int(cover_transform_width*1.3), cover_transform_width+cover_height - int(font.size*2))
image.fill_text(
    font,stats_text, transform=stats_transform
)

# place the qrcode.
qrcode = pixie.read_image(qrcode_path)
qrcode_width = qrcode_height = int(0.3*ad_width)
qrcode = qrcode.resize(qrcode_width, qrcode_height)


font = pixie.read_font(font_path)
font.size = int(ad_width*0.04)
if night_mode:
    font.paint.color = pixie.Color(1,1,1,1)
else:
    font.paint.color = pixie.Color(0,0,0,1)
qrcode_scan_text_transform_x = int(ad_width-qrcode_width*1.1-font.size*1)
qrcode_scan_text_transform = pixie.translate(qrcode_scan_text_transform_x+qrcode_width, int(ad_height-qrcode_height*1.1))
image.fill_text(
    font,qrcode_scan_text, transform=qrcode_scan_text_transform
)

qrcode_transform = pixie.translate(int(ad_width-qrcode_width*1.1-font.size*1.2), int(ad_height-qrcode_height*1.1))


qrcode_rounded_corner = int(0.05*ad_width)
qrcode_stroke_path = pixie.Path()
qrcode_stroke_path.rounded_rect(0,0,qrcode_width,qrcode_height, *([qrcode_rounded_corner]*4))
image.stroke_path(qrcode_stroke_path,cover_stroke_paint, qrcode_transform,stroke_width=int(ad_width / 100))

qrcode_mask = pixie.Mask(qrcode_width, qrcode_width)
qrcode_mask.fill_path(qrcode_stroke_path)
qrcode.mask_draw(qrcode_mask)

image.draw(qrcode, qrcode_transform)




# now for the title

font = pixie.read_font(font_bold_path)
font.size = int(ad_width*0.06)
if night_mode:
    font.paint.color = pixie.parse_color("#B0B0B0")
else:
    font.paint.color = pixie.parse_color("#4F4F4F")
# use some gray text.
# font.paint.color = pixie.parse_color("#4F42B5")
# font.paint.color = pixie.parse_color("#FC427B")
# font.paint.color = pixie.Color(0,0,0,1)
title_text_transform = pixie.translate(int(font.size*0.8), int(ad_height-qrcode_height*1.1))
title_text_bounds = pixie.Vector2(int(qrcode_scan_text_transform_x -font.size*1.1),int(qrcode_height))
image.fill_text(
    font,title_text, bounds = title_text_bounds,transform=title_text_transform
)


image.write_file("ad_2.png")


standalone_cover_image = 