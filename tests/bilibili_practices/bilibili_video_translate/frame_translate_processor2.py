from functional_redraw_chinese_text_offline2 import redraw_english_to_chinese2

import cv2
import progressbar as pb
source_video = "japan_day.webm"
output_json = "japan_day.json"
output_video = "japan_day_change_color2.mp4"
import os

if os.path.exists(output_video): os.remove(output_video)

# OOM for local translation!
# this will not work. fucking shit. though ocr is speedy.

# in this we will get no audio.
# use ffmpeg and time strencher.

# this is ideal for frame by frame processing.
# oh shit!
# the task is very long to run, i believe.

video_cap = cv2.VideoCapture(source_video)
fps = video_cap.get(cv2.CAP_PROP_FPS) # 60.
frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (frame_width, frame_height)
frame_count = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

# fourcc = cv2.VideoWriter_fourcc(*'H264') # h.264
# fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D') # h.264 
# this is builtin ffmpeg. not external shits.

# video_writer = cv2.VideoWriter(output_video,fourcc,fps,frame_size)

# frame_index_counter = 0
# this is determinism.
# or you could use framedifference? come on...
# while True:
import json
mjson_result = open(output_json, 'r',encoding='utf8').read()
mjson_result = json.loads(mjson_result)
import copy

# use some tweening? pytweening?
from test_curve_converter import curve_converter
    # for index, (orig, target) in enumerate(curve_function):
    #     if value <= orig:
    #         forig,ftarget = curve_function[index+1]
    #         if value == orig: return target
    #         elif value <=forig:
    #             if value ==forig: return ftarget
    #             else:
    #                 loc = (value-orig)/(forig-orig)
    #                 new_diff = loc*(ftarget-target)
    #                 new_value = target+new_diff
    #                 return new_value
    # return curve_function[-1][1]

def remove_much_red(image,curve_function):
    target = copy.copy(image[:,:,2])
    target = curve_converter(target,curve_function)
    image[:,:,2] = target
    return image

def remove_much_red_with_rate(image,reduce_rate = 0.8):
    target = copy.copy(image[:,:,2])
    target = target*(1-reduce_rate)
    image[:,:,2] = target
    return image

curve_function = [[0,0],[40,30],[100,50],[150,100],[255,130]]

for frame_index_counter in pb.progressbar(range(frame_count)): # are you sure?
    success, frame = video_cap.read() # let's just use 1, no frame skip.
    if not success: break
    # print("processing frame",frame_index_counter)
    # write the frame to the output file
    string_frame_index_counter = str(frame_index_counter)  #inpainting is still slow somehow. freaking shit. though i have the freaking shit.
    # maybe you can improvise.
    # this is done purely in CPU.
    processed_frame_data = mjson_result[string_frame_index_counter]# fucking string key.
    processed_frame = redraw_english_to_chinese2(frame,processed_frame_data) # step 1
    processed_frame = remove_much_red(processed_frame,curve_function)
    # mjson_result.update({frame_index_counter:processed_frame_data})
    # video_writer.write(processed_frame) # what frame?

    # frame_index_counter+=1
    cv2.imshow("image",processed_frame) #
    # # cv2.waitKey(1) # not wait infinitely.
    if cv2.waitKey(20) == ord('q'):
        break
# with open(output_json,"w+",encoding="utf-8") as f:
#     data = json.dumps(mjson_result,indent=4)
#     f.write(data)
# cv2.close
print("VIDEO DONE. SAVED AT:",output_video)