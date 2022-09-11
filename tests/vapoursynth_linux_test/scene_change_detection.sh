

ffmpeg -hide_banner -i "$file" -an \
-filter:v "select='gt(scene,0.2)',showinfo" \
-f null \
- 2>&1