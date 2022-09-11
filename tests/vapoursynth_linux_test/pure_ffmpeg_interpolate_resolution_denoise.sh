ffmpeg -y -i "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif" -vf "minterpolate,scale=w=iw*2:h=ih*2:flags=lanczos,hqdn3d" -r 60 ffmpeg_samoyed.mp4
# ffmpeg -y -i "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif" -filter "minterpolate=mi_mode=2" -r 60 ffmpeg_samoyed.mp4
# use deep learning models:
# https://video.stackexchange.com/questions/29337/how-do-the-super-resolution-filters-in-ffmpeg-work