WIDTH=936
HEIGHT=598

ffmpeg -i anime.gif -i ad_2_mask.png -filter_complex "[0:v]scale=936:598[v0];[1:v]alphaextract[alpha];[v0][alpha]alphamerge‌[vt]​"  anime_masked.gif