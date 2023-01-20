# python3 merge_fonts.py -d ./ -o noto_full.ttf
# this is bad.
# test something.
rm 1.ttf
rm 2.ttf
# courtesy from superuser:
# https://superuser.com/questions/490922/merging-two-fonts
# echo 0 $(ls -1 | grep ttf | xargs) 0
fontforge -lang=ff -script mergefonts.ff $(ls -1 | grep ttf | grep -v output | xargs) output.ttf