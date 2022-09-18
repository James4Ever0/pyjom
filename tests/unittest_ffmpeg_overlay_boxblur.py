# ffmpeg对视频实现高斯模糊，给视频上下加模糊背景
# ffmpeg实现视频高斯模糊拓边效果

import ffmpeg

source = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif"

stream = ffmpeg.input(source)

video_stream = stream.video


# the damn thing because they are from the same file! fuck!

layer_0 = video_stream.filter('scale',w=1080,h=1920).filter('boxblur',10,5)


layer_1 = video_stream.filter('scale',w=1080, h='ih*1080/iw')

output =  layer_0.overlay(layer_1,x=0, y=)