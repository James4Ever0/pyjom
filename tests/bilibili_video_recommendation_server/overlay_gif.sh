ffmpeg -i anime.gif -i overlay.png \
	-filter_complex "[0:v]scale=936:598[v1];[v1][1:v]overlay=0:0" \
	-c:a copy \
	anime_overlay.gif