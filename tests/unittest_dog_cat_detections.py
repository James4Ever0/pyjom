import torch
import os
from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2

os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

# Model
localModelDir = (
    "/root/Desktop/works/pyjom/pyjom/models/yolov5/ultralytics_yolov5_master/"
)
# import os
os.environ[
    "YOLOV5_MODEL_DIR"
] = "/root/Desktop/works/pyjom/pyjom/models/yolov5/"  # this is strange. must be a hack in the localModelDir
model = torch.hub.load(
    localModelDir, "yolov5s", source="local"
)  # or yolov5m, yolov5l, yolov5x, custom

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

area_threshold = 0.08 # min area?
confidence_threshold = 0.7  # this is image quality maybe.

y_expansion_rate = 0.1  # to make the starting point on y axis less "headless"

df = animal_detection_dataframe

new_df = df.loc[(df['area_ratio'] >= area_threshold) & (df['confidence'] >= confidence_threshold) & (df['name'] == dog_or_cat)].sort_values(by=['confidence']) # this one is for 0.13

# count = new_df.count(axis=0)
count = len(new_df)
# print("COUNT: %d" % count)
if count>=1:
    selected_col = new_df.iloc(0) # it is a dict-like object.
    # print(new_df)
    selected_col_dict = dict(selected_col)
    # these are floating point shits.
    # {'xmin': 1149.520263671875, 'ymin': 331.6445007324219, 'xmax': 1752.586181640625, 'ymax': 1082.3826904296875, 'confidence': 0.9185908436775208, 'class': 16, 'name': 'dog', 'area_ratio': 0.13691652620239364}
    x0, y0, x1, y1 = [int(selected_col_dict[key]) for key in ['xmin','ymin','xmax','ymax']]

    y0_altered = max(int(y0-(y1-y0)*y_expansion_rate),0)
    # print(selected_col_dict)
    # print(count)
    # breakpoint()
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
