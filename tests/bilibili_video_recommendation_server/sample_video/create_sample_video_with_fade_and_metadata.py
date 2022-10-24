# maybe this time you can burn uploader logo to the video
# the title of the video, intro, outro.

video_path = "/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server/sample_video/sample_video.mp4"
up_image_path = "/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server/up_image.jpg"
output_path = 'output.mp4'
title = "世上所有的小猫都是天使变的！"
from caer.video.frames_and_fps import get_duration, get_res
video_duration = get_duration(video_path)
video_width, video_height = get_res(video_path)
# we shall use editly to do this job shall we?

min_video_scalar = min(video_width, video_height)
up_image_scaler = int(min_video_scalar*0.2)

# image overlay can be done in editly

editlyJson = {
    'outPath':output_path,
    'width':video_width,
    'height': video_height,
    'fps':30, # different from the default value.
    'fast':False,
    'keepSourceAudio':True,
    'clips':[
        {
            "trasition":"fade", # or we just use random?
            "duration":video_duration,
            "layers":[
                {
                    "type":"image-overlay",
                    "path":up_image_path,
                    "position":"top-left",
                    "width":up_image_scaler,
                    "height":up_image_scaler,
                },
                {
                    "type":"video",
                    "path":video_path,
                    
                }
            ]
        }
    ]
}