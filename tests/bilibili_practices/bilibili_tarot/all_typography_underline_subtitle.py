from tarot_descriptions import *

# mdict, smdict2
import os

def gen_typography_part1(content):
    with open("demo_text.log","w+",encoding="utf8") as f:
        f.write(content)
    os.system("xvfb-run -s '-screen 0 1920x1080x24' python3 scriptable_generate_typography_with_voice_underline_subtitle.py")

def kill_script():
    os.system("bash kill_xb.sh")

typ_0 = "typo_0"
typ_1 = "typo_1"


# os.system("rm -rf {}".format(typ_0))
# os.system("rm -rf {}".format(typ_1))
# os.mkdir(typ_0)
# os.mkdir(typ_1)

from functional_voice_with_pictures import gen_typography_part3


# intro_text = """塔罗牌，是一种针对人、事、物进行分析、预测和提供建议的工具，被称为“大自然的奥秘库”。
# 抽取一张塔罗牌，今天的你会是怎样的呢？"""
intro_text = """奥拓是只猫～"""

# bgm_path = "/root/Desktop/works/bilibili_tarot/tarot_random_shuffle.mp3"

target_video = "cat_intro_video.mp4"
os.system("rm {}".format(target_video))

kill_script()
# v = mdict[k]
v = intro_text
gen_typography_part1(v)
# target_video = "/".join([typ_0,"{}.mp4".format(k)])
gen_typography_part3(v,target_video)
kill_script()

intro_text = """喜欢本期视频的话 点个关注再走吧～"""

# bgm_path = "/root/Desktop/works/bilibili_tarot/tarot_random_shuffle.mp3"

target_video = "cat_outro_video.mp4"
os.system("rm {}".format(target_video))

kill_script()
# v = mdict[k]
v = intro_text
gen_typography_part1(v)
# target_video = "/".join([typ_0,"{}.mp4".format(k)])
gen_typography_part3(v,target_video)
kill_script()

