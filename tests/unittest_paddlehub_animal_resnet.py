# source = "/root/Desktop/works/pyjom/samples/video/kitty_flash_15fps.gif"  # check that kitty video!
source = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif" # another kitty!

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
dog_labels = labelFileReader("/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/dogs.txt")
cat_labels = labelFileReader("/root/Desktop/works/pyjom/tests/animals_paddlehub_classification_resnet/cats.txt")

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

def dog_cat_name_recognizer(name):
    if name in dog_labels:
        return "dog"
    elif name in cat_labels:
        return "cat"
    elif name not in forbidden_words:
        for dog_suffix in dog_suffixs:
            if name.endswith(dog_suffix):
                return "dog"
        for cat_suffix in cat_suffixs:
            if name.endswith(cat_suffix):
                return "cat"
    return None

from lazero.utils.logger import sprint

classifier = hub.Module(name="resnet50_vd_animals")
# 'ResNet50vdAnimals' object has no attribute 'gpu_predictor'
# no gpu? really?
# test_flag = "video"
test_flag = "image"

def paddleAnimalDetectionResultToList(result):
    resultDict = result[0]
    resultList = [(key,value) for key,value in resultDict.items()]
    resultList.sort(key=lambda item: -item[1])
    return resultList

def translateResultListToDogCatList(resultList):
    final_result_list = []
    for name, confidence in resultList:
        new_name = dog_cat_name_recognizer(name)
        final_result_list.append((new_name, confidence))
    return final_result_list

if test_flag == "video":
    for frame in getVideoFrameIteratorWithFPS(source, -1, -1, fps=1):
        padded_resized_frame = resizeImageWithPadding(
            frame, 224, 224, border_type="replicate"
        )  # pass the test only if three of these containing 'cats'
        result = classifier.classification(
            images=[padded_resized_frame], top_k=3, use_gpu=False
        )  # check it?
        resultList = paddleAnimalDetectionResultToList(result)
        final_result_list = translateResultListToDogCatList(resultList)
        sprint("RESULT LIST:", final_result_list)
        # RESULT: [{'美国银色短毛猫': 0.23492032289505005, '虎斑猫': 0.14728288352489471, '美国银虎斑猫': 0.13097935914993286}]
        # so what is the major categories?
        # thanks to chinese, we are never confused.
        # check the labels, shall we?
        # what about samoyed?
        # sprint("RESULT:", result)
        breakpoint()
elif test_flag == "image":
    # source = "/root/Desktop/works/pyjom/samples/image/samoyed.jpeg"
    # [('dog', 0.8835851550102234), ('dog', 0.08754527568817139), ('dog', 0.008648859336972237)]
    # source = "/root/Desktop/works/pyjom/samples/image/dog_saturday_night.jpg"
    # not animal? wtf?
    # source = "/root/Desktop/works/pyjom/samples/image/porn_shemale.jpeg" # definitely not animal
    # [(None, 0.9894463419914246), ('dog', 1.564090962347109e-05), ('dog', 1.3550661606132053e-05)]
    #  [(None, 0.33663231134414673), ('dog', 0.32254937291145325), ('dog', 0.0494903139770031)]
    frame = cv2.imread(source)
    padded_resized_frame = resizeImageWithPadding(
        frame, 224, 224, border_type="replicate"
    )
    result = classifier.classification(
        images=[padded_resized_frame], top_k=3, use_gpu=False
    )
    resultList = paddleAnimalDetectionResultToList(result)
    final_result_list = translateResultListToDogCatList(resultList)
    sprint("FINAL RESULT LIST:", final_result_list)
    breakpoint()
else:
    raise Exception("unknown test flag: %s" % test_flag)
