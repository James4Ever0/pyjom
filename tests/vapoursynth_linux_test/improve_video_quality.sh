vspipe -c y4m denoise_and_upscale_samoyed.py - | ffmpeg -y -i pipe: -vf  improved.mp4
# vspipe -c y4m denoise_and_upscale_samoyed.py - | ffmpeg -y -i pipe: improved.mp4