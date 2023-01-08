import torch
import os
from lazero.utils.importers import cv2_custom_build_init

# order:
# detect if dog/cat is there, satisfying the qualification
# remove watermark, remove text, remove potential watermark around corners using inpainting
# use ffmpeg cropdetect, if has significant area change then no further processing
# if no significant area change, use this blur detection to get the main area
# remove watermark again?? around corners?
# then reuse the dog detection and get the crop from processed/cropped image.


cv2_custom_build_init()
import cv2

os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

# Model
# localModelDir = (
#     "/root/Desktop/works/pyjom/pyjom/models/yolov5/ultralytics_yolov5_master/"
# )
# # import os
# os.environ[
#     "YOLOV5_MODEL_DIR"
# ] = "/root/Desktop/works/pyjom/pyjom/models/yolov5/"  # this is strange. must be a hack in the localModelDir
# model = torch.hub.load(
#     localModelDir, "yolov5s", source="local"
# )  # or yolov5m, yolov5l, yolov5x, custom
from test_commons import *
from pyjom.commons import configYolov5

model = configYolov5()

dog_or_cat = "dog"

# Images
# img = '/media/root/help/pyjom/samples/image/miku_on_green.png'  # or file, Path, PIL, OpenCV, numpy, list
# img = "/root/Desktop/works/pyjom/samples/image/dog_with_text.jpg"
imgPath = "/root/Desktop/works/pyjom/samples/image/dog_blue_sky.png"

img = cv2.imread(imgPath)

defaultHeight, defaultWidth = img.shape[:2]
total_area = defaultHeight * defaultWidth

# Inference
results = model(img)

# print(results)
# # Results
# breakpoint()
animal_detection_dataframe = results.pandas().xyxy[0]
# results.show()
# # results.print() # or .show(),

area = (animal_detection_dataframe["xmax"] - animal_detection_dataframe["xmin"]) * (
    animal_detection_dataframe["ymax"] - animal_detection_dataframe["ymin"]
)

animal_detection_dataframe["area_ratio"] = area / total_area

area_threshold = 0.08  # min area?
confidence_threshold = 0.7  # this is image quality maybe.

y_expansion_rate = 0.03  # to make the starting point on y axis less "headless"

df = animal_detection_dataframe

new_df = df.loc[
    (df["area_ratio"] >= area_threshold)
    & (df["confidence"] >= confidence_threshold)
    & (df["name"] == dog_or_cat)
].sort_values(
    by=["confidence"]
)  # this one is for 0.13

# count = new_df.count(axis=0)
count = len(new_df)
# print("COUNT: %d" % count)

defaultCropWidth, defaultCropHeight = 1920, 1080
# this is just to maintain the ratio.

# you shall find the code elsewhere?

allowedHeight = min(int(defaultWidth / defaultCropWidth * defaultHeight), defaultHeight)

if count >= 1:
    selected_col = new_df.iloc[0]  # it is a dict-like object.
    # print(new_df)
    # breakpoint()
    selected_col_dict = dict(selected_col)
    # these are floating point shits.
    # {'xmin': 1149.520263671875, 'ymin': 331.6445007324219, 'xmax': 1752.586181640625, 'ymax': 1082.3826904296875, 'confidence': 0.9185908436775208, 'class': 16, 'name': 'dog', 'area_ratio': 0.13691652620239364}
    x0, y0, x1, y1 = [
        int(selected_col[key]) for key in ["xmin", "ymin", "xmax", "ymax"]
    ]

    y0_altered = max(int(y0 - (y1 - y0) * y_expansion_rate), 0)
    height_current = min((y1 - y0_altered), allowedHeight)  # reasonable?
    width_current = min(
        int((height_current / defaultCropHeight) * defaultCropWidth), defaultWidth
    )  # just for safety. not for mathematical accuracy.
    # height_current = min(allowedHeight, int((width_current/defaultCropWidth)*defaultCropHeight))
    # (x1+x0)/2-width_current/2
    import random

    x0_framework = random.randint(
        max((x1 - width_current), 0), min((x0 + width_current), defaultWidth)
    )
    framework_XYWH = (x0_framework, y0_altered, width_current, height_current)
    x_f, y_f, w_f, h_f = framework_XYWH
    croppedImageCover = img[y_f : y_f + h_f, x_f : x_f + w_f, :]
    # breakpoint()
    # resize image
    croppedImageCoverResized = cv2.resize(
        croppedImageCover, (defaultCropWidth, defaultCropHeight)
    )
    cv2.imshow("CROPPED IMAGE COVER", croppedImageCover)
    cv2.imshow("CROPPED IMAGE COVER RESIZED", croppedImageCoverResized)
    # print(selected_col_dict)
    # print(count)
    # breakpoint()
    cv2.waitKey(0)
else:
    print("NO COVER FOUND.")
# # results.save()
# # # print(type(results),dir(results))
# breakpoint()
# import cv2
# image = cv2.imread("runs/detect/exp3/miku_on_green.jpg")
# cv2.imshow("NONE",image)
# # results.print()  # or .show(),
# # hold it.
# # image 1/1: 720x1280 1 bird # what the fuck is a bird?
# # os.system("pause")
# # input()

# this shit has been detected but not in the right category.
