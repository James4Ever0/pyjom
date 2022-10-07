dirs = ["major","minor","typo_0","typo_1"]

import os
import shutil

os.system("mkdir final_output")

for d in dirs:
    files = os.listdir(d)
    for f in files:
        fname = "{}_{}".format(d,f)
        shutil.move(os.path.join(d,f),os.path.join("final_output",fname))

for x in ["intro_video.mp4","outro_video.mp4"]:
    shutil.move(x,os.path.join("final_output",x))