vspipe -c y4m denoise_and_upscale_samoyed.py - | ffmpeg -y -i pipe: -vf scale=w=in_w*2:h=in_h*2:flags=lanczos improved.mp4
# vspipe -c y4m denoise_and_upscale_samoyed.py - | ffmpeg -y -i pipe: output.bmp
# https://write.corbpie.com/upscaling-and-downscaling-video-with-ffmpeg/