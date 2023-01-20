# python3 merge_fonts.py -d ./ -o noto_full.ttf
# this is bad.
# test something.

# courtesy from superuser:
# 
echo $(ls -1 | grep ttf | xargs)
# fontforge -lang=ff -script mergefonts.ff $(ls -1 | grep ttf | xargs)