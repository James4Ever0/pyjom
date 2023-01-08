import parse
from pyjom.videotoolbox import getVideoWidthHeight
from test_commons import *
import ffmpeg

commandString = "delogo_0_671_360_6|delogo_144_662_6_4|delogo_355_661_5_7|delogo_117_661_7_5|delogo_68_661_18_5|delogo_182_658_165_9|delogo_252_492_3_1|delogo_214_492_1_2|delogo_200_492_3_1|delogo_74_492_2_1|delogo_170_490_6_4|delogo_145_490_9_4|delogo_129_490_12_4|delogo_107_490_4_3|delogo_91_487_8_6|delogo_72_485_4_3|delogo_147_484_4_3|delogo_178_483_11_11|delogo_219_480_1_1|delogo_53_480_6_2|delogo_268_478_1_1|delogo_164_478_8_4|delogo_128_477_8_4|delogo_295_475_1_1|delogo_105_475_10_4|delogo_61_474_5_4|delogo_274_472_3_2|delogo_196_470_5_2|delogo_209_469_1_1|delogo_143_469_8_5|delogo_75_467_26_6|delogo_0_33_360_25|delogo_0_24_360_6"


videoPath = "/root/Desktop/works/pyjom/samples/video/LkS8UkiLL.mp4"
outputPath = "/dev/shm/output.mp4"


def delogoParser(command):
    return parse.parse("delogo_{x:d}_{y:d}_{w:d}_{h:d}", command)


width, height = getVideoWidthHeight(videoPath)


def delogoFilter(stream, commandParams):
    return stream.filter(
        "delogo",
        x=commandParams["x"],
        y=commandParams["y"],
        w=commandParams["w"],
        h=commandParams["h"],
    )


# minArea = 20


def checkXYWH(XYWH, canvas, minArea=20):
    x, y, w, h = XYWH
    width, height = canvas
    if x >= width - 1 or y >= height - 1:
        return False, None
    if x == 0:
        x = 1
    if y == 0:
        y = 1
    if x + w >= width:
        w = width - x - 1
        if w <= 2:
            return False, None
    if y + h >= height:
        h = height - y - 1
        if h <= 2:
            return False, None
    if w * h <= minArea:
        return False, None
    return True, (x, y, w, h)


for command in commandString.split("|"):
    try:
        stream = ffmpeg.input(videoPath, ss=0, to=5).video
        commandArguments = delogoParser(command)
        x = commandArguments["x"]
        y = commandArguments["y"]
        w = commandArguments["w"]
        h = commandArguments["h"]

        status, XYWH = checkXYWH((x, y, w, h), (width, height))
        if not status:
            continue
        x, y, w, h = XYWH

        commandArguments = {"x": x, "y": y, "w": w, "h": h}
        stream = delogoFilter(stream, commandArguments)
        ffmpeg.output(stream, outputPath).run(overwrite_output=True)
    except:
        import traceback

        traceback.print_exc()
        print("WIDTH:", width, "HEIGHT:", height)
        maxX, maxY = (
            commandArguments["x"] + commandArguments["w"],
            commandArguments["y"] + commandArguments["h"],
        )
        print("MAX X:", maxX, "MAX Y:", maxY)
        print("ERROR!", commandArguments)
        breakpoint()
