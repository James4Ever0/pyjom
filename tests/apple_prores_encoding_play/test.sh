# videoPath="/root/Desktop/works/pyjom/samples/video/cute_cat_gif.mp4"
# ffmpeg -i $videoPath output.ProRes
videoPath="/Users/jamesbrown/Desktop/works/pyjom_remote/samples/video/cute_cat_gif.mp4"
ffmpeg -hwaccel videotoolbox -i $videoPath -c:v prores_ks output.mov