# ffmpeg -y -i "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif" -vf "minterpolate,scale=w=iw*2:h=ih*2:flags=lanczos,hqdn3d" -r 60 ffmpeg_samoyed.mp4

# SRCNN=espcn.pb

# 5fps or something
# env LD_LIBRARY_PATH=/root/anaconda3/pkgs/cudatoolkit-10.0.130-0/lib/:/root/anaconda3/pkgs/cudnn-7.6.5-cuda10.0_0/lib/:$LD_LIBRARY_PATH ffmpeg -i "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif" -y -vf "sr=dnn_backend=tensorflow:model=./sr_models/dnn_models/espcn.pb"  ffmpeg_samoyed_espcn.mp4

# 9fps or something
# ffmpeg -i "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif" -y -vf "yaepblur"  ffmpeg_samoyed_srcnn.mp4

# strange shit.
env LD_LIBRARY_PATH=/root/anaconda3/pkgs/cudatoolkit-10.0.130-0/lib/:/root/anaconda3/pkgs/cudnn-7.6.5-cuda10.0_0/lib/:$LD_LIBRARY_PATH ffmpeg -i "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif" -y -vf "sr=dnn_backend=tensorflow:model=./sr/espcn.pb,yaepblur,hqdn3d"  ffmpeg_samoyed_srcnn.mp4

#  TSC hqdn3d            V->V       Apply a High Quality 3D Denoiser.
# check out all filters by `ffmpeg -filters`
# yaepblur
# yet another edge preserving blur filter

# ffmpeg -y -i "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif" -filter "minterpolate=mi_mode=2" -r 60 ffmpeg_samoyed.mp4
# use deep learning models:
# https://video.stackexchange.com/questions/29337/how-do-the-super-resolution-filters-in-ffmpeg-work