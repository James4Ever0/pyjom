# maybe this time you can burn uploader logo to the video
# the title of the video, intro, outro.

video_path = "/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server/sample_video/sample_video.mp4"
title = "世上所有的小猫都是天使变的！"
from caer.video.frames_and_fps import get_duration
video_duration = get_duration(video_path)

# we shall use editly to do this job shall we?

# image overlay can be done in editly

editlyJson = {
    'outPath':'output.mp4',
    'width':1920,
    'height': 1080,
    'fps':30, # different from the default value.
    'fast':False,
    'keepSourceAudio':True,
    'clips':[
        {
            "trasition":"",
            "duration":video_duration,
            "layers":[
                {
                    "type":"image-overlay",
                    "path":"/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server/up_image.jpg",
                    "position":,
                    "width":,
                    "height":
                }
            ]
        }
    ]
}