ffmpeg -y -i "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif" -filter_complex "minterpolate;hqdn3d" -r 60 ffmpeg_samoyed.mp4
# ffmpeg -y -i "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif" -filter "minterpolate=mi_mode=2" -r 60 ffmpeg_samoyed.mp4