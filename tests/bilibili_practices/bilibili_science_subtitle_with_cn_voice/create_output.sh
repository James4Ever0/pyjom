ffmpeg -y -vsync 0 -hwaccel_output_format cuda -i "Scientists Discovered a Bubble Around Our Solar System! [At7ORzmAaT4].webm"  -vf "subtitles=zh_translated.srt:force_style='MarginV=60',subtitles=en_.srt:force_style='Fontsize=10,PrimaryColour=&H00FFFF00,Alignment=6,MarginV=228'" scientists_bubbles.mp4
# ffmpeg -y -vsync 0 -hwaccel_output_format cuda -i "Scientists Discovered a Bubble Around Our Solar System! [At7ORzmAaT4].webm" -ss 00:00:07 -to 00:01:00  -vf "subtitles=zh_translated.srt:force_style='MarginV=60',subtitles=en_.srt:force_style='Fontsize=10,PrimaryColour=&H00FFFF00,Alignment=6,MarginV=228'" scientists_bubbles.mp4
# https://www.zhihu.com/question/20779091
# https://www.jianshu.com/p/cfdbfdc6d3a7
# https://fileformats.fandom.com/wiki/SubStation_Alpha#Style_overrides
# PlayResX: 384
# PlayResY: 288
# 384×288是标准的4：3画面分辨率之一。ssa字幕里的坐标（字幕的位置）即根据这2个数值的范围来定义。
# ffmpeg -y -vsync 0 -hwaccel_output_format cuda -i "Scientists Discovered a Bubble Around Our Solar System! [At7ORzmAaT4].webm" -ss 00:00:07 -to 00:01:00  -vf "subtitles=zh_translated.srt:force_style='MarginV=0',subtitles=en_.srt" scientists_bubbles.mp4