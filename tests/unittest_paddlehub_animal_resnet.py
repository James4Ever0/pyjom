source = "/root/Desktop/works/pyjom/samples/video/kitty_flash_15fps.gif"  # check that kitty video!

from test_commons import *
from pyjom.videotoolbox import getVideoFrameIteratorWithFPS
from pyjom.imagetoolbox import resizeImageWithPadding

import paddlehub as hub
import cv2

def labelFileReader(filename):
    with open(filename, 'r') as f:
        content = f.read()
        content = content.split("\n")
        content = [elem.replace("\n","").strip() for elem in content]
        content = [elem for elem in content if len(elem)>0]
    return content

dog_suffixs = ["狗", "犬", "梗"]
cat_suffixs = ["猫"]  # ends with this, and not containing forbidden words.
dog_labels = labelFileReader("")
cat_labels = labelFileReader("")

forbidden_words = [
    "灵猫",
    "熊猫",
    "猫狮",
    "猫头鹰",
    "丁丁猫儿",
    "绿猫鸟",
    "猫鼬",
    "猫鱼",
    "玻璃猫",
    "猫眼",
    "猫蛱蝶",
]

from lazero.utils.logger import sprint

classifier = hub.Module(name="resnet50_vd_animals")
# 'ResNet50vdAnimals' object has no attribute 'gpu_predictor'
# no gpu? really?
test_flag = "image"

if test_flag == "video":
    for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
        padded_resized_frame = resizeImageWithPadding(
            frame, 224, 224, border_type="replicate"
        )  # pass the test only if three of these containing 'cats'
        result = classifier.classification(
            images=[padded_resized_frame], top_k=3, use_gpu=False
        )  # check it?
        # RESULT: [{'美国银色短毛猫': 0.23492032289505005, '虎斑猫': 0.14728288352489471, '美国银虎斑猫': 0.13097935914993286}]
        # so what is the major categories?
        # thanks to chinese, we are never confused.
        # check the labels, shall we?
        # what about samoyed?
        sprint("RESULT:", result)
        breakpoint()
elif test_flag == "image":
    source = "/root/Desktop/works/pyjom/samples/image/samoyed.jpeg"
    frame = cv2.imread(source)
    padded_resized_frame = resizeImageWithPadding(
        frame, 224, 224, border_type="replicate"
    )
    result = classifier.classification(
        images=[padded_resized_frame], top_k=3, use_gpu=False
    )
    sprint("RESULT:", result)
    breakpoint()
else:
    raise Exception("unknown test flag: %s" % test_flag)
