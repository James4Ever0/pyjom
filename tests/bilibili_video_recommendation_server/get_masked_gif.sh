WIDTH=936
HEIGHT=598

# ffmpeg -y -i anime.gif  -loop 1 -t 1 -i ad_2_mask.png -filter_complex "[0]scale=$WIDTH:$HEIGHT[v0];[1]alphaextract[v1];[v0][v1]alphamerge[vf];color=black:d=1[c];[c][vf]scale2ref[cs][vf0];[cs][vf0]overlay" anime_masked.gif
ffmpeg -y -i anime.gif  -loop 1 -t 1 -i ad_2_mask.png -i overlay.png -filter_complex "[0]scale=$WIDTH:$HEIGHT[v0];[1]alphaextract[v1];[v0][v1]alphamerge[vf];color=black:d=1[c];[c][vf]scale2ref[cs][vf0];[cs][vf0]overlay[vf1];[vf1][2]overlay" anime_masked_overlay.gif