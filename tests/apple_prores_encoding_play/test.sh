# videoPath="/root/Desktop/works/pyjom/samples/video/cute_cat_gif.mp4"
# ffmpeg -i $videoPath output.ProRes
videoPath="/Users/jamesbrown/Desktop/works/pyjom_remote/samples/video/cute_cat_gif.mp4"
ffmpeg -hwaccel videotoolbox -i $videoPath -c:v prores_ks output.mov
# Do remember to store the output in either of these three formats that are allowed as containers for the ProRes format.

# .mov (QuickTime)
# .mkv (Matroska)
# .mxf (Material eXchange Format)
