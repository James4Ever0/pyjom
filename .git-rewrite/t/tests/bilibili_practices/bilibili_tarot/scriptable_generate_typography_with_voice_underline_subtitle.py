from p5 import *

import os
# from test_common import demo_text


demo_text = open("demo_text.log","r",encoding="utf-8").read()

os.system("rm screenshot*")
target_dir = "demo_typography"
os.system("rm -rf {}".format(target_dir))
os.system("mkdir {}".format(target_dir))

tsize = 100
counterx = 0
scrwidth = 1920
xcoord = int(scrwidth/2) # how to get this shit?
scrheight = 1080
ycoord = scrheight - tsize - 75
lineNum = 0

# what fucking ever.
s = demo_text
s0 = [""]
def setup():
    size(scrwidth,scrheight)
    # text_font(create_font('./fonts/Fonts/博洋行书3500.ttf', size=tsize))
    # text_font(create_font('./fonts/Fonts/书体坊兰亭体I.ttf', size=tsize))
    text_font(create_font('./SimHei.ttf', size=tsize))

import random

def draw():
    global counterx,xcoord,ycoord,s,s0,scrheight,scrwidth,lineNum,target_dir
    #force override.
    background(0)
    if counterx > len(s)-1:
        exit()
    s1 = s[:counterx]
    counterx+=1
    mtext_width = text_width(s1)
    try:
        text9 = s1
        # else:
        #     text9 = " "
        # l = len(s0)-1
        # rotate = random.randint(-15,15)
        # rotate = random.choice([random.randint(-20,-10),random.randint(10,20)])
        rotate = 0
        # r1 = random.randint(220,255)
        # r2 = random.randint(220,255)
        # r3 = random.randint(220,255)
        # r4 = random.randint(220,255)
        r1 = r2 = r3 = r4 = 255
        fill(red=r1, green=r2, blue=r3, alpha=r4)
        text(text9, (xcoord-int(mtext_width/2), ycoord,),rotate = rotate)  # add str() to key
    except:
        import traceback
        traceback.print_exc()
        print("SHIT HAPPENED")
        pass
    save_frame("{}/screenshot.png".format(target_dir))

run()
print("EXITED.")