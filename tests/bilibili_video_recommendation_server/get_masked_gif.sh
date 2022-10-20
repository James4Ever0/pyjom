WIDTH=936
HEIGHT=598


# ffmpeg -i anime.gif -i ad_2_mask.png -filter_complex "[0]scale=936:598[v0]​" anime_masked.gif

ffmpeg -i anime.gif -i ad_2_mask.png -filter_complex "scale=$WIDTH:$HEIGHT"