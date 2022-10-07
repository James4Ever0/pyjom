import os
from vidpy import Clip, Composition  #many shitty things...
# tarot_target = "/root/Desktop/works/bilibili_tarot/tarot_pictures/0_THE_FOOL.jpg"
import random

def gen_tarot(tarot_target,bgm_path,final_output):
    os.system("rm tarot_demo.mp4")
    fps =60
    # myprofile = {'width': 1320, 'height': 2644} # wtf?
    # just create profile from it. are you sure?
    clip = Clip(tarot_target, output_fps=fps,start=0, end=16,override=True)
    # clip.edgeglow()
    # clip.crop
    # 1320x2645 # unbelievable.
    # clip.fx("",{})
    # clip.resize(w=1920, h=1080, distort=True)
    # distort=False
    c_w = clip.width
    c_h = clip.height
    # comp = Composition([clip])
    clip.dither(amount=0.07) # the greater the better.

    clip.fadein(0.5)      # fade the clip in over 1 second
    # clip.fadeout(3.5)   # fade the clip over 0.5 seconds
    # clip.glow(3.5)         # add a glow effect
    clip.spin(4, axis="z")
    clip.vignette()
    clip.dust()
    clip.hue(shift = 1-random.random()*0.5)
    clip.pixelize(width = 0.005,height=0.01)
    # clip.invert()
    # clip.luminance
    # clip.charcoal()
    # clip.crop(right=c_w,bottom=c_h)
    clip.save("tarot_demo.mp4", fps=60,duration = 3,width=c_w,height=c_h) # good.
    # print(c_w,c_h)
    # 720 576
    r1 = c_w/c_h
    target_w, target_h = 1920, 1080
    r2 = target_w/ target_h
    if r1 < r2:
        os.system('ffmpeg -y -i tarot_demo.mp4  -vf "scale=-1:{},pad={}:ih:(ow-iw)/2"  tarot_demo2.mp4'.format(target_h,target_w))
    else:
        os.system('ffmpeg -y -i tarot_demo.mp4  -vf "scale={}:-1,pad=iw:{}:0:(oh-ih)/2"  tarot_demo2.mp4'.format(target_w,target_h))
    
    os.system("ffmpeg -y -i {} -i {} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest {}".format("tarot_demo2.mp4",bgm_path,final_output))

    os.system("rm -rf tarot_demo2.mp4")
    os.system("rm -rf tarot_demo.mp4")