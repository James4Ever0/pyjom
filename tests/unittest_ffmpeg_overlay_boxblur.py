# ffmpeg对视频实现高斯模糊，给视频上下加模糊背景
# ffmpeg实现视频高斯模糊拓边效果

import ffmpeg

source = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif"

ffmpeg.input()

filter('scale',w=1080,h=1920)
filter('boxblur',10,5)


filter('scale',w=1080, h='ih*1080')