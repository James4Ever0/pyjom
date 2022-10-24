# maybe this time you can burn uploader logo to the video
# the title of the video, intro, outro.

video_path = "/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server/sample_video/sample_video.mp4"
up_image_path = (
    "/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server/up_image.jpg"
)
output_path = "output.mp4"
fontPath = "/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server/wqy-microhei0.ttf"
cat_image = (
    "/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server/cat_image.jpg"
)
title = "世上所有的小猫\n\n都是天使变的！" # add newline, change it into another catchy title, as compliment.
audio_path = "output.mp3.mp3"
audio_duration = 3.31
template_name = "template.json"
from caer.video.frames_and_fps import get_duration, get_res

video_duration = get_duration(video_path)
video_width, video_height = get_res(video_path)
# we shall use editly to do this job shall we?

min_video_scalar = min(video_width, video_height)
up_image_scalar = int(min_video_scalar * 0.2)
up_image_width = up_image_scalar / video_width
up_image_height = up_image_scalar / video_height

# some parameters are using floating point numbers between 0 and 1
# image overlay can be done in editly

# no need to render that silly karaoke effects.

editlyJson = {
    "outPath": output_path,
    "width": video_width,
    "height": video_height,
    "fps": 30,  # different from the default value.
    "fast": True,  # just for preview. if not turning this on, will be too slow.
    "keepSourceAudio": True,  # it does!
    "defaults": {
        "transition": {
            "duration": 0.5,
            "name": "fade",
            "audioOutCurve": "tri",
            "audioInCurve": "tri",
        }
    },
    "clips": [
        # {
        #     "duration": 0.5,
        #     "layers": [
        #         # {"type": "fill-color", "color": "#000000"},
        #         # {"type": "detached-audio", "path": audio_path}, # will make sure nothing visual presents.
        #     ],
        # },
        # we disable this clip.
        {
            "duration": audio_duration,
            "layers": [
                {
                    "type": "image-overlay",
                    "path": cat_image,
                    "position": "center",
                    "width": 1,
                    "height": 1,
                },
                {
                    # "type": "title-background",
                    "type": "title",
                    "text": title,
                    # "background": "#000000",
                    "fontPath": fontPath,
                    "textColor": "#FFFFFF",
                },
                {"type": "audio", "path": audio_path},  # order matters!
            ],
        },
        {
            # "transition": "fade",  # or we just use random?
            "duration": video_duration,
            "layers": [
                {"type": "video", "path": video_path},  # order is important.
                {
                    "type": "image-overlay",
                    "path": up_image_path,
                    "position": "top-left",
                    "width": up_image_width,  # float numbers.
                    "height": up_image_height,
                },
            ],
        },
        {"duration": 0.5, "layers": [{"type": "fill-color", "color": "#000000"}]},
    ],
}

from lazero.filesystem.io import writeJsonObjectToFile

writeJsonObjectToFile(template_name, editlyJson)

import subprocess

# use xvfb you SOB
command = [
    "xvfb-run",
    "editly",
    template_name,
]  # no need to specify --out outputPath here
subprocess.run(command)
