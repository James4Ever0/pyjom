
# output motion vectors.

# ffmpeg -i "/root/Desktop/works/pyjom/tests/random_giphy_gifs/samoyed.gif" -vf "mestimate=epzs:mb_size=16:search_param=7, codecview=mv=pf+bf+bb"  mestimate_output.mp4 -y

# not just toy, but can find PIP
# picture in picture, crop detect?

ffmpeg -i  -vf mestimate,cropdetect=mode=mvedges,metadata=mode=print -f null -