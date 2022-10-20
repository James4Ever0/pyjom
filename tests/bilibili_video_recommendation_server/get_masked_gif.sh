WIDTH=936
HEIGHT=598

ffmpeg -y -i anime.gif -i ad_2_mask.png -filter_complex "[0:v]scale=$WIDTH:$HEIGHT[v0];[1:v]loop=-1:size=2,setsar=1[alpha];[v0][alpha]alphamerge‌[vt]​"  anime_masked.gif