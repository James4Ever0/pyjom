videoPath=""
ffmpeg -hwaccel vulkan -i $videoPath output.prores
# ffmpeg -hwaccel videotoolbox -i $videoPath output.prores