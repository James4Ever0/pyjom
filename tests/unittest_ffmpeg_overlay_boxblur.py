# ffmpeg对视频实现高斯模糊，给视频上下加模糊背景
# ffmpeg实现视频高斯模糊拓边效果

import ffmpeg

source = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif"

stream = ffmpeg.input(source)

video_stream = stream.video

# the damn thing because they are from the same file! fuck!

# layer_0 = video_stream.filter("scale", w=1080, h=1920).filter("boxblur", 10) # this is default?

# however, you need to generalize it here.

output_width = 1080
output_height = 1920

layer_0 = video_stream.filter("scale", w=output_width, h=1920).filter("gblur", sigma=9) # this is default?

# print('layer_0 args', layer_0.get_args())

layer_1 = video_stream.filter("scale", w=output_height, h="ih*output_width/iw")
# print('layer_1 args', layer_1.get_args())

output_stream = layer_0.overlay(layer_1, x=0, y="floor((H-h)/2)")
# print('output_stream args', output_stream.get_args())

from lazero.filesystem import tmpdir

path = "/dev/shm/medialang"
import os

with tmpdir(path=path) as T:
    filepath = os.path.join(path, "output.mp4")
    # args = ffmpeg.get_args(output_stream)
    # print(args)
    output_args =  {"preset":"veryfast"} # seems like it won't speed up so much?
    ffmpeg.output(output_stream,filepath, **output_args).run(overwrite_output=True)
    print("output file location:", filepath)
    breakpoint()
