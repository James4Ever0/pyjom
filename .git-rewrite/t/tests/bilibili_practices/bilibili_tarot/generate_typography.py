from p5 import *

import os

os.system("rm screenshot*")
tsize = 100
counterx = 0
xcoord = 20
ycoord = 75
scrwidth = 1920
scrheight = 1080
lineNum = 0

# what fucking ever.
s = "[START]"+"SOME TEXT"*500+"[END]"
s0 = [""]
def setup():
    size(scrwidth,scrheight)
    text_font(create_font('./SimHei.ttf', size=tsize))


def draw():
    global counterx,xcoord,ycoord,s,s0,scrheight,scrwidth,lineNum
    if len(s0) ==1:
        if len(s0[0]) == 0:
            background(0)
    if counterx > len(s)-1:
        exit()
    s1 = s[counterx]
    stemp0 = s0[-1]+s1
    tw = text_width(stemp0)
    th = tsize*(lineNum+1) + tsize*0.2*lineNum
    # th = tsize*(stemp0.count("\n")+1)
    # if (ycoord+th> scrheight):
    #     s0 = s1
    # else:
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

    print("text w/h:",tw,th)
    # for l, text9 in enumerate(s0):
    text9 = s0[-1][-1]
    l = len(s0)-1
    text(text9, (xcoord+text_width(s0[-1][:-1]), ycoord+ l*(tsize*1.2)))  # add str() to key
    save_frame("screenshot.png")

run()
print("EXITED.")