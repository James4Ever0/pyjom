
# output motion vectors.

ffmpeg -i "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif" -vf "mestimate=epzs:mb_size=16:search_param=7, codecview=mv=pf+bf+bb"  mestimate_output.mp4 -y