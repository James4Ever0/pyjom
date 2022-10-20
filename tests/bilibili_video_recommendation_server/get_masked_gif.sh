WIDTH=936
HEIGHT=598


ffmpeg -y -i anime.gif  -loop 1 -t 1 -i ad_2_mask.png -filter_complex "[0]scale=$WIDTH:$HEIGHT[v0];[1]alphaextract,negate,setsar=1[v1];[v0][v1]alphamerge" anime_masked.gif