# try to improve gif quality in some way.
# is this necessary?

# apply some filter on video size and duration first, please?
import pathlib
import sys
site_path = pathlib.Path("/usr/local/lib/python3.9/site-packages")
cv2_libs_dir = (
    site_path / "cv2" / f"python-{sys.version_info.major}.{sys.version_info.minor}"
)
print(cv2_libs_dir)
cv2_libs = sorted(cv2_libs_dir.glob("*.so"))
if len(cv2_libs) == 1:
    print("INSERTING:", cv2_libs[0].parent)
    sys.path.insert(1, str(cv2_libs[0].parent))



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

# video = core.resize.Lanczos(clip=video, format=vs.RGBS, 
#                         matrix_in_s="2020ncl",
#                         transfer_in_s="std-b67", transfer_s="linear",
#                         nominal_luminance=1000)
# video = core.tonemap.Mobius(clip=video, exposure=4)

# video = core.resize.Lanczos(clip=video, format=vs.YUV420P10, matrix_s="709",
#                         primaries_in_s="2020",  primaries_s="709",
#                         transfer_in_s="linear", transfer_s="709")

# slow as hell man.
# a very bad filter for dogs
# video = core.rcnv.RealCUGAN(video , scale=scale, 
                #   gpu_id=gpu_id, model=1)
from vsbasicvsrpp import BasicVSRPP

video = BasicVSRPP(video)
# solution from tonemap?
# https://github.com/ifb/vapoursynth-tonemap/issues/2

# video = core.resize.Lanczos(clip=video, format=vs.YUV420P10, matrix_s="709",
#                         primaries_in_s="2020",  primaries_s="709",
#                         transfer_in_s="linear", transfer_s="709")

video = core.resize.Bicubic(clip =video, format = vs.YUV420P10, matrix_s='709')
# much better, no over exposure.
video.set_output()

# maybe this shit is very freaking slow.
# why not use gaussian blur?