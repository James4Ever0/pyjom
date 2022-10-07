# ffmpeg -hwaccels
# vdpau
# cuda
# vaapi
# vulkan
# no blood.
ffmpeg -y -vsync 0 -hwaccel_output_format cuda -i "Wolfenstein 2 The New Colossus - Courthouse Battle ( I am death incarnate & no HUD ) 4k_60Fps [FuV63EEhS8c].webm" -vf "hue=h=45:s=0.7" Wolfenstein_courthouse_battle.mp4
# ffmpeg -y -vsync 0 -hwaccel_output_format cuda -i "Wolfenstein 2 The New Colossus - Courthouse Battle ( I am death incarnate & no HUD ) 4k_60Fps [FuV63EEhS8c].webm"  Wolfenstein_courthouse_battle.mp4
# ffmpeg -y -vsync 0 -hwaccel vdpau -hwaccel_output_format vulkan -i "Wolfenstein 2 The New Colossus - Courthouse Battle ( I am death incarnate & no HUD ) 4k_60Fps [FuV63EEhS8c].webm"  Wolfenstein_courthouse_battle.mp4
# ffmpeg -y -vsync 0 -hwaccel vulkan -hwaccel_output_format vulkan -i "Wolfenstein 2 The New Colossus - Courthouse Battle ( I am death incarnate & no HUD ) 4k_60Fps [FuV63EEhS8c].webm"  Wolfenstein_courthouse_battle.mp4
# ffmpeg -y -vsync 0 -hwaccel cuda -hwaccel_output_format cuda -i "Wolfenstein 2 The New Colossus - Courthouse Battle ( I am death incarnate & no HUD ) 4k_60Fps [FuV63EEhS8c].webm"  Wolfenstein_courthouse_battle.mp4  # this is not avaliable. nvenc is not for everyone.

# use vulkan or cuda. but vulkan is universal.
# "hue=H=30+10*cos(2*PI*t):s=0.2*cos(2*PI*t)+0.6"