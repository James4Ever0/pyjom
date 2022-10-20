WIDTH=936
HEIGHT=598


ffmpeg -y -i anime.gif  -i ad_2_mask.png -loop 1  -filter_complex "[0]scale=$WIDTH:$HEIGHT[v];[1]alphaextract[v1];[v][v1]alphamerge" anime_masked.gif