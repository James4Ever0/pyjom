wget https://media.xiph.org/video/derf/y4m/flower_cif.y4m

# no good for using docker gpu containers.

# alias ffmpeg-tensorflow='docker run --rm --gpus all -u $(id -u):$(id -g) -v "$PWD":/data -w /data -i miratmu/ffmpeg-tensorflow'
# ffmpeg-tensorflow -i flower_cif.y4m -filter_complex '[0:v] format=pix_fmts=yuv420p, extractplanes=y+u+v [y][u][v]; [y] sr=dnn_backend=tensorflow:scale_factor=2:model=/models/espcn.pb [y_scaled]; [u] scale=iw*2:ih*2 [u_scaled]; [v] scale=iw*2:ih*2 [v_scaled]; [y_scaled][u_scaled][v_scaled] mergeplanes=0x001020:yuv420p [merged]' -map [merged] -sws_flags lanczos -c:v libx264 -crf 17 -c:a copy -y flower_cif_2x.mp4