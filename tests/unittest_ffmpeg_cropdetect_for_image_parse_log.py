import ffmpeg

# mediaPath = "/root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png"
mediaPath = "/root/Desktop/works/pyjom/samples/image/dog_with_black_borders.png"  # use the image with black background.
# ffmpeg -loop 1 -i /root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png -t 15 -vf cropdetect -f null -

import cv2

image = cv2.imread(mediaPath)
height, width = image.shape[:2]
total_area = height*width
areaThreshold = 0

stdout, stderr = (
    ffmpeg.input(mediaPath, loop=1, t=15)
    .filter("cropdetect")
    .output("null", f="null")
    .run(capture_stdout=True, capture_stderr=True)
)


stdout_decoded = stdout.decode("utf-8")
stderr_decoded = stderr.decode("utf-8")

# nothing here.
# for line in stdout_decoded.split("\n"):
#     print(line)

# breakpoint()
import parse

common_crops = []

for line in stderr_decoded.split("\n"):
    line = line.replace("\n", "").strip()
    formatString='[{}] x1:{x1:d} x2:{x2:d} y1:{y1:d} y2:{y2:d} w:{w:d} h:{h:d} x:{x:d} y:{y:d} pts:{pts:g} t:{t:g} crop={}:{}:{}:{}'
    # print(line)
    result = parse.parse(formatString,line)
    if result is not None:
        # print(result)
        cropString = "{}_{}_{}_{}".format(*[result[key] for key in ['w','h','x','y']])
        # print(cropString)
        # breakpoint()
        common_crops.append(cropString)
    # [Parsed_cropdetect_0 @ 0x56246a16cbc0] x1:360 x2:823 y1:0 y2:657 w:464 h:656 x:360 y:2 pts:3 t:0.120000 crop=464:656:360:2
    # this crop usually will never change. but let's count?
area = 0
if len(common_crops) > 0:
    common_crops_count_tuple_list = [(cropString, common_crops.count(cropString)) for cropString in set(common_crops)]
    common_crops_count_tuple_list.sort(key= lambda x: -x[1])
    selected_crop_string = common_crops_count_tuple_list[0][0]

    result = parse.parse('{w:d}_{h:d}_{x:d}_{y:d}', selected_crop_string)
    w,h,x,y = [result[key] for key in ['w','h','x','y']]
    x1, y1 = min(x+w, width), min(y+h, height)
    if x<x1 and y<y1:
        # allow to calculate the area.
        area = (x1-x)*(y1-y)
    cropped_area_ratio = 1-(area/total_area) # 0.5652352766414517
    # use 0.1 as threshold?
    print("CROPPED AREA RATIO:",cropped_area_ratio)