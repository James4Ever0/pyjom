

ffmpeg -hide_banner -i "/root/Desktop/works/pyjom/samples/video/LiEIfnsvn.mp4" -an \
-filter:v "select='gt(scene,0.1)',showinfo" \
-f null \
- 2>&1