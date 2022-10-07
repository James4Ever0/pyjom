# generate all flipcards.
from tarot_correspondences import *

from functional_generate_demo_tarot import gen_tarot
# mtarget_0, mtarget_1
dir_0 = "major"
dir_1 = "minor"

os.system("rm -rf {}".format(dir_0))
os.system("rm -rf {}".format(dir_1))
os.mkdir(dir_0)
os.mkdir(dir_1)

bgm_path = "/root/Desktop/works/bilibili_tarot/some_bgm.mp3"


for k in mtarget_0.keys():
    value = mtarget_0[k]
    videoPath = "/".join([dir_0,"{}.mp4".format(k)])
    picture_path = value
    gen_tarot(picture_path,bgm_path,videoPath)

for k in mtarget_1.keys():
    value = mtarget_1[k]
    videoPath = "/".join([dir_1,"{}.mp4".format(k)])
    picture_path = value
    gen_tarot(picture_path,bgm_path,videoPath)