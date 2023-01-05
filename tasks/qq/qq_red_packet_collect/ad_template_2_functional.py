import pixie
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2


def getImageW2H(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    w2h = width / height
    return w2h

TMP_DIR_PATH = "/dev/shm/qq_ad"
import shutil
import os
if os.path.exists(TMP_DIR_PATH):
    shutil.rmtree(TMP_DIR_PATH)
os.mkdir(TMP_DIR_PATH)

import random

def generateFakeVideoStats():
    play_count = "{}万".format(random.randint(100,1000)*.1) # anyway both int and str are compatible
    comment_count = random.randint(100,1000)
    danmaku_count = random.randint(500,3000)
    return play_count, comment_count,danmaku_count

RESOURCE_PATH = "/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server"

QRCODE_PATH = "MyQRCode1.png"

FONT_PATH = "wqy-microhei0.ttf"
FONT_BOLD_PATH = "wqy-microhei1.ttf"
COVER_PATH = "sample_cover.jpg"
PLAY_BUTTON_PATH = "play_white_b.png"
BILIBILI_LOGO_PATH= "bili_white_b_cropped.png"

RESOURCES_RELATIVE_PATH = [
FONT_PATH ,
FONT_BOLD_PATH ,
COVER_PATH,
PLAY_BUTTON_PATH,
BILIBILI_LOGO_PATH]

OUTPUT_STANDALONE = "ad_2_standalone_cover.png"
OUTPUT_PATH = "ad_2.png"
OUTPUT_MASKED_PATH = "ad_2_mask.png"

def prepareMaterials(tmpDirPath:str=TMP_DIR_PATH, resourcePath :str= RESOURCE_PATH):
    for path in RESOURCES_RELATIVE_PATH:
        

def generateVideoAd(
videoStats = generateFakeVideoStats(),
night_mode :bool= True,
title_text:str = "",
framework_only :bool= False,
ad_width:int=1000,
ad_height:int=1000,
font_path :str= os.path.join(TMP_DIR_PATH,FONT_PATH),
font_bold_path :str= os.path.join(TMP_DIR_PATH,FONT_BOLD_PATH),
cover_path:str = os.path.join(TMP_DIR_PATH,COVER_PATH),
qrcode_path :str= os.path.join(TMP_DIR_PATH,QRCODE_PATH),
play_button_path :str= os.path.join(TMP_DIR_PATH,PLAY_BUTTON_PATH),
output_path:str = os.path.join(TMP_DIR_PATH,OUTPUT_PATH),
output_standalone :str= os.path.join(TMP_DIR_PATH,OUTPUT_STANDALONE),
output_masked_path:str= os.path.join(TMP_DIR_PATH,OUTPUT_MASKED_PATH),
bilibili_logo_path:str = os.path.join(TMP_DIR_PATH,BILIBILI_LOGO_PATH),
    ):
    # fake these numbers.
    # one extra space.
    play_count, comment_count,danmaku_count = videoStats
    assert title_text != ""
    stats_text = " {}播放 {}评论 {}弹幕".format(play_count, comment_count, danmaku_count)
    qrcode_scan_text = "\n" + "\n".join(list("扫码观看"))
    white = pixie.Color(1, 1, 1, 1)
    black = pixie.Color(0, 0, 0, 1)
    image = pixie.Image(ad_width, ad_height)

    # we are creating this, not replacing qr code.
    if not framework_only:
        if night_mode:
            image.fill(black)
            # irreversible!
        else:
            image.fill(white)
    else:
        image2 = image.copy()  # as mask.

    # place the cover.
    cover_w2h = getImageW2H(cover_path)
    cover_width = int(ad_width * 0.9)
    cover_height = int(cover_width / cover_w2h)
    cover_round_corner_radius = int(ad_width * 0.05)
    cover = pixie.read_image(cover_path)
    cover = cover.resize(cover_width, cover_height)
    # cover gradient.

    gradient_paint = pixie.Paint(pixie.LINEAR_GRADIENT_PAINT)

    gradient_paint.gradient_handle_positions.append(
        pixie.Vector2(100, int(cover_height) * 0.8)
    )
    gradient_paint.gradient_handle_positions.append(pixie.Vector2(100, cover_height))

    gradient_paint.gradient_stops.append(pixie.ColorStop(pixie.Color(0, 0, 0, 0), 0))
    gradient_paint.gradient_stops.append(pixie.ColorStop(pixie.Color(0, 0, 0, 0.3), 1))

    cover_mask_path = pixie.Path()
    cover_mask_path.rounded_rect(
        0, 0, cover_width, cover_height, *([cover_round_corner_radius] * 4)
    )
    stroke_param = 100
    stroke_width = int(ad_width / stroke_param)
    stroke_width_half = int(ad_width / stroke_param / 2)
    cover_mask_path2 = pixie.Path()
    cover_round_corner_radius2 = int(cover_round_corner_radius * 0.85)

    cover_mask_path2.rounded_rect(
        stroke_width_half,
        stroke_width_half,
        cover_width - stroke_width,
        cover_height - stroke_width,
        *([cover_round_corner_radius2] * 4)
    )

    # path = cover_mask_path
    # cover.fill_path(cover_mask_path, gradient_paint)


    cover_mask = pixie.Mask(cover_width, cover_height)

    cover_mask.fill_path(cover_mask_path)

    cover.mask_draw(cover_mask)


    cover_transform_width = cover_transform_height = int((ad_width - cover_width) / 2)
    cover_transform = pixie.translate(cover_transform_width, cover_transform_height)

    if framework_only:
        # image2.fill(black)

        image2_paint = pixie.Paint(pixie.SOLID_PAINT)
        image2_paint.color = white
        image2.fill_path(cover_mask_path, image2_paint, cover_transform)

    cover_stroke_paint = pixie.Paint(pixie.SOLID_PAINT)
    cover_stroke_paint.color = pixie.parse_color("#FC427B")
    image.stroke_path(
        cover_mask_path,
        cover_stroke_paint,
        cover_transform,
        stroke_width=stroke_width,
    )
    if not framework_only:
        image.draw(cover, cover_transform)  # you can choose to discard the cover
    image.fill_path(cover_mask_path2, gradient_paint, cover_transform)

    # now place the bilibili logo.

    bilibili_logo = pixie.read_image(bilibili_logo_path)
    bilibili_logo_w2h = getImageW2H(bilibili_logo_path)
    bilibili_logo_width = int(ad_width * 0.2)
    bilibili_logo_height = int(bilibili_logo_width / bilibili_logo_w2h)
    bilibili_logo = bilibili_logo.resize(bilibili_logo_width, bilibili_logo_height)

    bilibili_logo_transform = pixie.translate(
        cover_transform_width + int(bilibili_logo_height / 8),
        int(cover_transform_width + (bilibili_logo_height / 4)),
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
    font.size = int(ad_width * 0.04)
    font.paint.color = pixie.Color(1, 1, 1, 1)
    stats_transform = pixie.translate(
        int(cover_transform_width * 1.3),
        cover_transform_width + cover_height - int(font.size * 2),
    )
    image.fill_text(font, stats_text, transform=stats_transform)

    # place the qrcode.
    qrcode = pixie.read_image(qrcode_path)
    qrcode_width = qrcode_height = int(0.3 * ad_width)
    qrcode = qrcode.resize(qrcode_width, qrcode_height)


    font = pixie.read_font(font_path)
    font.size = int(ad_width * 0.04)
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


    qrcode_rounded_corner = int(0.05 * ad_width)
    qrcode_stroke_path = pixie.Path()
    qrcode_stroke_path.rounded_rect(
        0, 0, qrcode_width, qrcode_height, *([qrcode_rounded_corner] * 4)
    )
    image.stroke_path(
        qrcode_stroke_path,
        cover_stroke_paint,
        qrcode_transform,
        stroke_width=stroke_width,
    )

    qrcode_mask = pixie.Mask(qrcode_width, qrcode_width)
    qrcode_mask.fill_path(qrcode_stroke_path)
    qrcode.mask_draw(qrcode_mask)

    image.draw(qrcode, qrcode_transform)


    # now for the title

    font = pixie.read_font(font_bold_path)
    font.size = int(ad_width * 0.06)
    if night_mode:
        font.paint.color = pixie.parse_color("#B0B0B0")
    else:
        font.paint.color = pixie.parse_color("#4F4F4F")
    # use some gray text.
    # font.paint.color = pixie.parse_color("#4F42B5")
    # font.paint.color = pixie.parse_color("#FC427B")
    # font.paint.color = pixie.Color(0,0,0,1)
    title_text_transform = pixie.translate(
        int(font.size * 0.8), int(ad_height - qrcode_height * 1.1)
    )
    title_text_bounds = pixie.Vector2(
        int(qrcode_scan_text_transform_x - font.size * 1.1), int(qrcode_height)
    )
    image.fill_text(
        font, title_text, bounds=title_text_bounds, transform=title_text_transform
    )
    delta = int(cover_width * 0.02)
    sub_image_params = (
        cover_transform_width - delta,
        cover_transform_height - delta,
        cover_width + 2 * delta,
        cover_height + 2 * delta,
    )
    standalone_cover_image = image.sub_image(*sub_image_params)
    standalone_cover_image.write_file(output_standalone)
    image.write_file(output_path) # make sure you write to desired temp path.
    if framework_only:
        image2.sub_image(*sub_image_params).write_file(output_masked_path)
