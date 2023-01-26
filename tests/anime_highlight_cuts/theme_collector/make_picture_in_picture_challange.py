basepath = "/Users/jamesbrown/Downloads/anime_download"

import os

source_video = os.path.join(
    basepath, "[Sakurato] Onii-chan wa Oshimai! [未删减][02][AVC-8bit 1080p AAC][CHT].mp4"
)

background_video = os.path.join(
    basepath, "[MLU-S] Onii-chan wa Oshimai! - 03 [1080p][Multi Subs].mkv"
)

video_duration = 10  # just for test.

# use ffplay?
# better save metadata in the filename.
import ffmpeg



ffmpeg -y -t 0:00:10 -i "$basepath/$video_0" -t 0:00:10 -i "$basepath/$video_1" -filter_complex "[0:v]scale=1152:648[v0];[1:v][v0]overlay=384:216" output.mp4