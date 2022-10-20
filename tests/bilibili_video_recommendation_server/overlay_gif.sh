ffmpeg -i anime.gif -i overlay.png \
	-filter_complex "[0:v][1:v] overlay=0:0" \
	-c:a copy \
	anime_overlay.gif