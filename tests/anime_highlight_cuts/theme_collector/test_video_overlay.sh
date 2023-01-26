video_0="[Sakurato] Onii-chan wa Oshimai! [未删减][02][AVC-8bit 1080p AAC][CHT].mp4"
video_1="[MLU-S] Onii-chan wa Oshimai! - 03 [1080p][Multi Subs].mkv"
basepath="/Users/jamesbrown/Downloads/anime_download"

ffmpeg -y -t 0:00:10 -i "$basepath/$video_0" -i "$basepath/$video_1" -filter_complex "[0:v][1:v]overlay=100:100" -shortest output.mp4