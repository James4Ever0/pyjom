video_0="[Sakurato] Onii-chan wa Oshimai! [未删减][02][AVC-8bit 1080p AAC][CHT].mp4"
video_1="[MLU-S] Onii-chan wa Oshimai! - 03 [1080p][Multi Subs].mkv"
basepath="/Users/jamesbrown/Downloads/anime_download"

video_2="[Sakurato] Onii-chan wa Oshimai! [01][AVC-8bit 1080p AAC][CHT].mp4"

# ffmpeg -y -t 0:04:00 -i "$basepath/$video_0" -t 0:04:00 -i "$basepath/$video_1" -filter_complex "[0:v]scale=1152:648[v0];[1:v][v0]overlay=384:216" output.mp4

ffmpeg -y -t 0:04:00 -i "$basepath/$video_2" output_1.mp4