# try to improve gif quality in some way.
# is this necessary?

# apply some filter on video size and duration first, please?

videoPath = "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif"
# videoPath = "/root/Desktop/works/pyjom/tests/random_giphy_gifs/pikachu.gif"

import vapoursynth

# install this:
# https://github.com/HomeOfVapourSynthEvolution/mvsfunc
import vapoursynth as vs
from vapoursynth import core

video = core.ffms2.Source(source=videoPath)

# visit here for more usage details:
# https://github.com/HomeOfVapourSynthEvolution/VapourSynth-BM3D

import mvsfunc as mvf # denoising

video = mvf.BM3D(video, sigma=3.0, radius1=1, profile1="fast")

from vsrife import RIFE # frame interpolate

video = core.resize.Bicubic(video, format=vs.RGBS)

video = RIFE(video)

# super resolution
# copy compiled .so file to here:
# /root/vapoursynth/plugins/lib/
# ln -s /root/Desktop/works/pyjom/tests/vapoursynth_linux_test/models /root/vapoursynth/plugins/lib/models
gpu_id = 0
# noise = 2
scale = 2

# slow.
# video = core.srmdnv.SRMD(video,scale=scale, noise=noise, 
#                   gpu_id=gpu_id)
# video = core.resize.Bicubic(video, format=vs.YUV420P8, matrix_s="709")
video = core.resize.Lanczos(clip=video, format=vs.YUV420P10, matrix_s="709",
                        primaries_in_s="2020",  primaries_s="709",
                        transfer_in_s="linear", transfer_s="709")
video = core.rcnv.RealCUGAN(video , scale=scale, 
                  gpu_id=gpu_id, model=1)

video.set_output()

# maybe this shit is very freaking slow.
# why not use gaussian blur?