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
    play_count = "{:.1f}万".format(
        random.randint(100, 1000) * 0.1
    )  # anyway both int and str are compatible
    comment_count = random.randint(100, 1000)
    danmaku_count = random.randint(500, 3000)
    return play_count, comment_count, danmaku_count


RESOURCE_PATH = "/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server"

QRCODE_PATH = "MyQRCode1.png"

FONT_PATH = "wqy-microhei0.ttf"
FONT_BOLD_PATH = "wqy-microhei1.ttf"
COVER_PATH = "sample_cover.jpg"
PLAY_BUTTON_PATH = "play_white_b.png"
BILIBILI_LOGO_PATH = "bili_white_b_cropped.png"

AD_LOCK = "ad_lock.lock"
import filelock


def getAdLock(lockPath: str = os.path.join(TMP_DIR_PATH, AD_LOCK)):
    return filelock.FileLock(lockPath)


# use this decorator outside. not here. not any function written in here.
def withAdLock(func):
    def innerFunc(*args, **kwargs):
        with getAdLock():
            return func(*args, **kwargs)

    return innerFunc


RESOURCES_RELATIVE_PATH = [
    FONT_PATH,
    FONT_BOLD_PATH,
    COVER_PATH,
    PLAY_BUTTON_PATH,
    BILIBILI_LOGO_PATH,
]

OUTPUT_STANDALONE = "ad_2_standalone_cover.png"
OUTPUT_PATH = "ad_2.png"
OUTPUT_MASKED_PATH = "ad_2_mask.png"

import progressbar


def prepareMaterials(tmpDirPath: str = TMP_DIR_PATH, resourcePath: str = RESOURCE_PATH):
    print("Preparing materials...")
    for path in progressbar.progressbar(RESOURCES_RELATIVE_PATH):
        shutil.copy(os.path.join(resourcePath, path), os.path.join(tmpDirPath, path))


prepareMaterials()


def generateBilibiliShortLinkMethod2(videoLink: str):

    apiUrl = (
        "https://service-ijd4slqi-1253419200.gz.apigw.tencentcs.com/release/short_url"
    )
    # longUrl = "https://www.bilibili.com/video/BV1Wv41157Wz"
    longUrl = videoLink
    import urllib.parse as urlparse

    # params = {"url": longUrl}
    params = {
        "url": urlparse.quote(longUrl).replace("/", "%2F"),
        "href": "https://xiaojuzi.fun/bili-short-url/",
    }
    # print(params)
    # exit()

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "if-none-match": 'W/"35-oPDNsqBGaZKqGe83GW6wem+lkww"',
        "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://xiaojuzi.fun/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",  # this is important.
    }

    import requests

    request_url = apiUrl + "?url={url}&href={href}".format(**params)
    # request_url = 'https://service-ijd4slqi-1253419200.gz.apigw.tencentcs.com/release/short_url?url=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1Wv41157Wz&href=https://xiaojuzi.fun/bili-short-url/'
    # print(request_url)
    r = requests.get(request_url, headers=headers)
    if r.status_code == 200:
        # print(r.json())
        r_json = r.json()
        success = r_json.get("success", False)
        if success:
            short_url = r_json.get("short_url", None)
            print(short_url)
            return short_url
    # starts with 'https://b23.tv'


def generateBilibiliShortLinkMethod1(
    videoLink: str,
):  # get bilibili user email address by asking them from chat. if they give the email address, send setu as gift. for other users, you may improvise. send video link, recommendations
    url = "https://api.bilibili.com/x/share/click"
    # burl = "https://www.bilibili.com/read/cv19232041" # my article with e-begging
    burl = videoLink
    data = {
        "build": 6700300,
        "buvid": 0,
        "oid": burl,
        "platform": "android",
        "share_channel": "COPY",
        "share_id": "public.webview.0.0.pv",
        "share_mode": 3,
    }
    import requests

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    r = requests.post(
        url, data=data, headers=headers
    )  # maybe you two share the same user agent!
    # we have the link!
    if r.status_code == 200:
        # print(r.content)
        r_json = r.json()
        code = r_json["code"]
        if code == 0:
            link = r_json["data"]["content"]
            print(link)
            return link
    # fail, obviously.


def generateBilibiliShortLink(videoLink: str):
    link = None
    try:
        link = generateBilibiliShortLinkMethod1(videoLink)
        assert link is not None
    except:
        import traceback

        traceback.print_exc()
        link = generateBilibiliShortLinkMethod2(videoLink)
        assert link is not None
    return link


def makeQRCode(content: str, savePath: str):
    # Importing library
    import qrcode

    # Encoding data using make() function
    def makeAndSaveQrcode(data, save_path, debug=False):
        img = qrcode.make(data)
        if debug:
            print("image type:", type(img))
        img.save(save_path)

    data = content
    save_path = savePath
    makeAndSaveQrcode(data, save_path)


def generateQRCodeFromBVID(
    bvid: str, qrCodeSavePath: str = os.path.join(TMP_DIR_PATH, QRCODE_PATH)
):
    videoLink = "https://www.bilibili.com/video/{}".format(bvid)
    shortLink = generateBilibiliShortLink(videoLink)
    makeQRCode(shortLink, qrCodeSavePath)
    return shortLink


def generateBilibiliVideoAd(
    bvid: str,
    title_text: str,
    image_link: str,
    cover_path: str = os.path.join(TMP_DIR_PATH, COVER_PATH),
):
    import requests

    r = requests.get(image_link)
    with open(cover_path, "wb") as f:
        c = r.content
        f.write(c)
    link = generateQRCodeFromBVID(bvid)
    return (generateVideoAdUniversal(
        videoStats=generateFakeVideoStats(),
        title_text=title_text,
        cover_path=cover_path,
    ), link)


# you must have some lock outside while using this.
def generateVideoAdUniversal(
    videoStats=None,  # will it work?
    night_mode: bool = True,
    title_text: str = "",
    framework_only: bool = False,
    ad_width: int = 1000,
    ad_height: int = 1000,
    font_path: str = os.path.join(TMP_DIR_PATH, FONT_PATH),
    font_bold_path: str = os.path.join(TMP_DIR_PATH, FONT_BOLD_PATH),
    cover_path: str = os.path.join(TMP_DIR_PATH, COVER_PATH),
    qrcode_path: str = os.path.join(TMP_DIR_PATH, QRCODE_PATH),
    play_button_path: str = os.path.join(TMP_DIR_PATH, PLAY_BUTTON_PATH),
    output_path: str = os.path.join(TMP_DIR_PATH, OUTPUT_PATH),
    output_standalone: str = os.path.join(TMP_DIR_PATH, OUTPUT_STANDALONE),
    output_masked_path: str = os.path.join(TMP_DIR_PATH, OUTPUT_MASKED_PATH),
    bilibili_logo_path: str = os.path.join(TMP_DIR_PATH, BILIBILI_LOGO_PATH),
):
    # fake these numbers.
    # one extra space.
    assert videoStats is not None
    play_count, comment_count, danmaku_count = videoStats
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
        qrcode_scan_text_transform_x + qrcode_width,
        int(ad_height - qrcode_height * 1.1),
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
    image.write_file(output_path)  # make sure you write to desired temp path.
    if framework_only:
        image2.sub_image(*sub_image_params).write_file(output_masked_path)
    return (
        output_path,
        output_standalone,
        output_masked_path,
    )  # well, pick up if you want.


IMAGE_WITH_QRCODE_PATH = "image_with_qrcode.png"
OUTPUT_WITH_QRCODE_PATH = "output_with_qrcode.png"


def removeQRCodes(
    image_with_qrcode_path: str = os.path.join(TMP_DIR_PATH, IMAGE_WITH_QRCODE_PATH)
):
    # use best method to remove qrcode.
    # import cv2
    # import imutils
    from PIL import Image
    from pyzbar.pyzbar import decode, ZBarSymbol

    # @function 'detect_qr' detect and decode qrcode from frame using pyzbar lib
    # @param 'inputFrame' type <class 'numpy.ndarray'>
    # @return if detected type 'bool'
    import numpy as np

    def detect_qr(inputFrame):
        img = Image.fromarray(inputFrame)  # fuck?
        decodedImg = decode(img, symbols=[ZBarSymbol.QRCODE])
        # it reads the content. but where is the code?
        print("total %d qrcode detected" % len(decodedImg))
        # breakpoint()
        # length: 2

        if len(decodedImg) > 0:
            polygons = []
            for code in decodedImg:
                decodedBytes = code.data
                # stringData = decodedBytes.decode("utf-8")
                # print("QRCode content:")
                # print(stringData)
                polygon = code.polygon
                # print('POLYGON CONTENT:')
                # print(polygon)
                mpolygon = []
                for point in polygon:
                    mpolygon.append([point.x, point.y])
                #     print('POINT:',point.x,point.y)
                polygons.append(np.array(mpolygon, dtype=np.int32))
            return polygons
        else:
            return []

    def getInputFrameFromImagePath(imagePath: str):
        inputFrame = cv2.imread(imagePath)
        return inputFrame

    inputFrame = getInputFrameFromImagePath(image_with_qrcode_path)
    QRCodeCoordinates = detect_qr(inputFrame)
    img = cv2.imread(image_with_qrcode_path)

    if QRCodeCoordinates != []:
        mask_image = np.zeros((*img.shape[:2], 1), dtype=img.dtype)
        for poly in QRCodeCoordinates:
            cv2.fillPoly(mask_image, [poly], 255)
        inpainted_im = cv2.inpaint(img, mask_image, 3, cv2.INPAINT_TELEA)
    else:
        inpainted_im = img
    return QRCodeCoordinates, inpainted_im


from typing import Union


def removeAndInsertQRCode(
    image_with_qrcode_path: str = os.path.join(TMP_DIR_PATH, IMAGE_WITH_QRCODE_PATH),
    qrcode_path: str = os.path.join(TMP_DIR_PATH, QRCODE_PATH),
    output_with_qrcode_path: Union[None, str] = os.path.join(
        TMP_DIR_PATH, OUTPUT_WITH_QRCODE_PATH
    ),
):  # remove all detected QRCodes. add qrcode nevertheless.
    # TODO: use more advanced models to detect QRCodes.
    # TODO: increase the size of the original image if too small.
    QRImage = cv2.imread(qrcode_path)
    import math

    def get_rotation_angle_and_center(p1, p2, p3, p4):
        # Find the center of the rectangle
        center_x = int((p1[0] + p3[0]) / 2 + (p2[0] + p4[0]) / 2) / 2
        center_y = int((p1[1] + p3[1]) / 2 + (p2[1] + p4[1]) / 2) / 2
        center = (center_x, center_y)
        width = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        height = math.sqrt((p2[0] - p3[0]) ** 2 + (p2[1] - p3[1]) ** 2)

        # Calculate the slope of one of the edges
        slope = (p2[1] - p1[1]) / (p2[0] - p1[0])

        # Calculate the angle of the edge from the x-axis
        angle = (math.pi / 2) - math.atan(
            slope
        )  # correct the angle. according to opencv.
        while True:
            if angle > math.pi / 2:
                angle -= math.pi / 2
            elif angle < 0:
                angle += math.pi / 2
            else:
                break
        return angle, center, width, height

    QRCodeCoordinates, img = removeQRCodes(image_with_qrcode_path)
    hasQRCode = len(QRCodeCoordinates) > 0
    from shapely.geometry import Polygon
    import numpy as np

    if hasQRCode:  # put the biggest one there.
        QRCodeCoordinates.sort(key=lambda x: -Polygon(x.tolist()).area)
        biggest_polygon = QRCodeCoordinates[0]
        cv2.fillPoly(img, [biggest_polygon], (0, 0, 0))
        angle, center, width, height = get_rotation_angle_and_center(
            *biggest_polygon.tolist()
        )  # will fail?
        QRWidth, QRHeight = int(width), int(height)
        startingPoint = [int(center[0] - QRWidth / 2), int(center[1] - QRHeight / 2)]
    else:
        # randomly select one place to insert the shit.
        height, width = img.shape[:2]
        QRSize = min(height, width) / 5
        QRHeight, QRWidth = QRImage.shape[:2]
        if QRWidth > QRHeight:
            QRHeight = int((QRHeight / QRWidth) * QRSize)
            QRWidth = int(QRSize)
        else:
            QRWidth = int((QRWidth / QRHeight) * QRSize)
            QRHeight = int(QRSize)
        startingPoint = [
            random.randint(0, math.floor(width - QRWidth)),
            random.randint(0, math.floor(height - QRHeight)),
        ]
        angle, center = 0, [
            startingPoint[0] + int(QRWidth / 2),
            startingPoint[1] + int(QRHeight / 2),
        ]
        biggest_polygon = np.array(
            [
                startingPoint,
                [startingPoint[0], startingPoint[1] + QRHeight],
                [startingPoint[0] + QRWidth, startingPoint[1] + QRHeight],
                [startingPoint[0] + QRWidth, startingPoint[1]],
            ]
        )
        cv2.fillPoly(img, [biggest_polygon], (0, 0, 0))

    QRImage = cv2.resize(QRImage, (QRWidth, QRHeight), interpolation=cv2.INTER_LINEAR)
    # then we expand the image.
    expanded_QR = np.zeros(img.shape, dtype=img.dtype)
    height, width = QRImage.shape[:2]
    slice_x_start, slice_x_end = startingPoint[1], height + startingPoint[1]
    slice_y_start, slice_y_end = startingPoint[0], width + startingPoint[0]
    # print("SLICES?", slice_x_start, slice_x_end , slice_y_start, slice_y_end )
    # print("IMAGE SHAPE?",QRImage.shape)
    expanded_QR[slice_x_start:slice_x_end, slice_y_start:slice_y_end] = QRImage

    # then rotate.
    if angle == 0:
        rotated_im = expanded_QR
    else:
        angle_deg = 180 * (angle / np.pi)  # rotation error.
        rotation_matrix = cv2.getRotationMatrix2D(center, angle_deg, 1)
        rotated_im = cv2.warpAffine(
            expanded_QR, rotation_matrix, (img.shape[1], img.shape[0])
        )

    # combine. what?
    output_img = rotated_im + img

    # regularize
    output_img.put(np.where(output_img > 255), 255)
    output_img.put(np.where(output_img < 0), 0)

    # save the image.
    if output_with_qrcode_path is not None:
        cv2.imwrite(output_with_qrcode_path, output_img)
    return output_img  # for viewing.
