from p5 import *

import os
# from test_common import demo_text


demo_text = open("demo_text.log","r",encoding="utf-8").read()

os.system("rm screenshot*")
target_dir = "demo_typography"
os.system("rm -rf {}".format(target_dir))
os.system("mkdir {}".format(target_dir))

tsize = 70
counterx = 0
xcoord = 20
ycoord = 75
scrwidth = 1920
scrheight = 1080
lineNum = 0

# what fucking ever.
s = demo_text
s0 = [""]
def setup():
    size(scrwidth,scrheight)
    # text_font(create_font('./fonts/Fonts/博洋行书3500.ttf', size=tsize))
    text_font(create_font('./fonts/Fonts/书体坊兰亭体I.ttf', size=tsize))
    # text_font(create_font('./SimHei.ttf', size=tsize))

import random

def draw():
    global counterx,xcoord,ycoord,s,s0,scrheight,scrwidth,lineNum,target_dir
    if len(s0) ==1:
        if len(s0[0]) == 0:
            background(0)
    if counterx > len(s)-1:
        exit()
    s1 = s[counterx]
    returnFlag = False
    if s1 == "\n":
        # this is return!
        returnFlag = True
        lineNum +=1
        stemp0 = "" # this is nothing.
        tw = text_width(stemp0)
        th = tsize*(lineNum+1) + tsize*0.2*(lineNum)
        if (ycoord+th> scrheight):
            # stemp0 = s1
            s0 = [stemp0]
            clear()
            background(0)
            lineNum = 0
        else:
            s0.append(stemp0)
    else:
        stemp0 = s0[-1]+s1
        tw = text_width(stemp0)
        th = tsize*(lineNum+1) + tsize*0.2*lineNum
        if (tw + xcoord+ tsize*0.5> scrwidth):
            stemp0 = s1
            s0.append(stemp0)
            lineNum +=1
            th = tsize*(lineNum+1) + tsize*0.2*lineNum
            if (ycoord+th> scrheight):
                # stemp0 = s1
                s0 = [stemp0]
                background(0)
                lineNum = 0
        else:
            s0[-1]= stemp0
        # no_loop()
        # clear
    # s0 = stemp0
        # end all evil.
    counterx+=1
    # load_font("SimHei.ttf")

    # print("text w/h:",tw,th)
    # for l, text9 in enumerate(s0):
    if len(s0) == 1 and len(s0[0])<=1: # whatever.
        # breakpoint()
        clear()
        background(0)
    # if not returnFlag:
    # print(s0)
    try:
        text9 = s0[-1][-1]
        # else:
        #     text9 = " "
        l = len(s0)-1
        # rotate = random.randint(-15,15)
        rotate = random.choice([random.randint(-20,-10),random.randint(10,20)])
        r1 = random.randint(200,255)
        r2 = random.randint(200,255)
        r3 = random.randint(200,255)
        r4 = random.randint(200,255)
        fill(red=r1, green=r2, blue=r3, alpha=r4)
        text(text9, (xcoord+text_width(s0[-1][:-1]), ycoord+ l*(tsize*1.2),),rotate = rotate)  # add str() to key
    except:
        import traceback
        traceback.print_exc()
        print("SHIT HAPPENED")
        pass
    save_frame("{}/screenshot.png".format(target_dir))

run()
print("EXITED.")