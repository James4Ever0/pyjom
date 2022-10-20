WIDTH=936
HEIGHT=598
ffmpeg -y -i anime.gif -loop 1 -t 1 -i ad_2_mask.png -filter_complex "[0:v]scale=$WIDTH:$HEIGHT;[1:v]alphaextract[m];[v0][1:v]alphamerge‌​"  anime_masked.gif