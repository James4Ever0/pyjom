import os
from vidpy import Clip, Composition  #many shitty things...
tarot_target = "/root/Desktop/works/bilibili_tarot/tarot_pictures/0_THE_FOOL.jpg"
os.system("rm tarot_demo.mp4")
fps =60
myprofile = {'width': 1320, 'height': 2644}
# just create profile from it. are you sure?
clip = Clip(tarot_target, output_fps=fps,start=0, end=16, profile_override=myprofile,override=False)
# clip.edgeglow()
# clip.crop
# 1320x2645 # unbelievable.
# clip.fx("",{})
# clip.resize(w=1920, h=1080, distort=True)
# distort=False
c_w = clip.width
c_h = clip.height
# comp = Composition([clip])
clip.dither(amount=0.2) # the greater the better.

clip.fadein(0.5)      # fade the clip in over 1 second
# clip.fadeout(3.5)   # fade the clip over 0.5 seconds
# clip.glow(3.5)         # add a glow effect
clip.spin(4, axis="z")
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
