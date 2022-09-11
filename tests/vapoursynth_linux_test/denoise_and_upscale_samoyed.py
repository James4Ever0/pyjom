# try to improve gif quality in some way.
# is this necessary?

# apply some filter on video size and duration first, please?

videoPath = "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif"
# videoPath = "/root/Desktop/works/pyjom/tests/random_giphy_gifs/pikachu.gif"

import vapoursynth

# install this:
# https://github.com/HomeOfVapourSynthEvolution/mvsfunc

src = vapoursynth.

# visit here for more usage details:
# https://github.com/HomeOfVapourSynthEvolution/VapourSynth-BM3D

import mvsfunc as mvf # denoising

clip = mvf.BM3D(src, sigma=3.0, radius1=1, profile1="fast")

from vsrife import RIFE # frame interpolate

ret = RIFE(clip)

# super resolution
# copy compiled .so file to here:
# /root/vapoursynth/plugins/lib/


