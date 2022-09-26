videoPath="/root/Desktop/works/pyjom/samples/video/cute_cat_gif.mp4"
ffmpeg -hwaccel vulkan -i $videoPath -c:v prores output.prores
# ffmpeg -hwaccel videotoolbox -i $videoPath output.prores