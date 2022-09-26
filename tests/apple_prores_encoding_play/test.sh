videoPath="/root/Desktop/works/pyjom/samples/video/cute_cat_gif.mp4"
# prores_aw
ffmpeg -hwaccel vulkan -i $videoPath -c:v prores_ks  output.mkv
# https://ottverse.com/ffmpeg-convert-to-apple-prores-422-4444-hq/#:~:text=FFmpeg%20contains%20two%20ProRes%20encoders%2C%20the%20prores-aw%20and,option%20to%20choose%20the%20ProRes%20profile%20to%20encode.
# videoPath="/Users/jamesbrown/Desktop/works/pyjom_remote/samples/video/cute_cat_gif.mp4"
# ffmpeg -hwaccel videotoolbox -i $videoPath -c:v prores_ks  \
# -profile:v 4 \
# -vendor apl0 \
# -bits_per_mb 8000 \
# -pix_fmt yuva444p10le \ 
# output.mov
# Do remember to store the output in either of these three formats that are allowed as containers for the ProRes format.

# .mov (QuickTime)
# .mkv (Matroska)
# .mxf (Material eXchange Format)
