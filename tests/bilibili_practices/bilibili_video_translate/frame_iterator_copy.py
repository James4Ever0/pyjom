import cv2
import progressbar as pb
source_video = "japan_day.webm"
output_video = "japan_day_copy.mp4"

# in this we will get no audio.
# use ffmpeg and time strencher.

# from functional_redraw_chinese_text_offline import 
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

video_writer =cv2.VideoWriter(output_video,fourcc,fps,frame_size)

# frame_index_counter = 0
# while True:
for frame_index_counter in pb.progressbar(range(frame_count)): # are you sure?
    success, frame = video_cap.read()
    if not success: break
    print("processing frame",frame_index_counter)
    # write the frame to the output file
    video_writer.write(frame) # what frame?
    # frame_index_counter+=1
    # if cv2.waitKey(20) == ord('q'):
        # break
print("VIDEO DONE. SAVED AT:",output_video)