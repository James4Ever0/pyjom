import os
import shutil

targets = ["images/miku_on_green.png","images/miku_on_green.txt"]


for target in targets:
    for x in range(200):
        name, suffix = target.split(".")
        real_name = ".".join([name,str(x),suffix])
        shutil.copy(target, real_name)
        if "png" in real_name:
            print("/media/root/help/pyjom/tests/mmd_human_dance_pose/alphapose_anime_human/AlphaPose/detector/yolo/anime_data/"+real_name)