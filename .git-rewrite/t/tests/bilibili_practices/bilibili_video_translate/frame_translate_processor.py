import cv2
import progressbar as pb
source_video = "japan_day.webm"
output_json = "japan_day.json"
# output_video = "japan_day_translated.mp4"

# OOM for local translation!

# in this we will get no audio.
# use ffmpeg and time strencher.

from functional_redraw_chinese_text_offline import redraw_english_to_chinese
# this is ideal for frame by frame processing.
# oh shit!
# the task is very long to run, i believe.

video_cap = cv2.VideoCapture(source_video)
fps = video_cap.get(cv2.CAP_PROP_FPS) # 60.
frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (frame_width, frame_height)
frame_count = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D') # h.264

# video_writer =cv2.VideoWriter(output_video,fourcc,fps,frame_size)

# frame_index_counter = 0
# this is determinism.
# or you could use framedifference? come on...
# while True:
import json
mjson_result = {}
for frame_index_counter in pb.progressbar(range(frame_count)): # are you sure?
    success, frame = video_cap.read() # let's just use 1, no frame skip.
    if not success: break
    print("processing frame",frame_index_counter)
    # write the frame to the output file
    processed_frame_data= redraw_english_to_chinese(frame) # step 1
    mjson_result.update({frame_index_counter:processed_frame_data})
    # video_writer.write(processed_frame) # what frame?
    # frame_index_counter+=1
    # if cv2.waitKey(20) == ord('q'):
        # break
with open(output_json,"w+",encoding="utf-8") as f:
    data = json.dumps(mjson_result,indent=4)
    f.write(data)
print("VIDEO DONE ANALYSING. SAVED AT:",output_json)