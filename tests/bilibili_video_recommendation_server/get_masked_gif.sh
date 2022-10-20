WIDTH=936
HEIGHT=598


ffmpeg -y -i anime.gif  -i ad_2_mask.png -loop 1  -filter_complex "[0]scale=$WIDTH:$HEIGHT[v0];[1]alphaextract[v1];[v1][v0]scale2ref[mask][main];[main][mask]alphamerge" anime_masked.gif