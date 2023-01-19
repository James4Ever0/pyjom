URL_PREFIX="https://download.fastgit.org/satbyy/go-noto-universal/releases/download/v5.2"

rm -rf *.ttf
rm -rf *.aria2

cat fonts.log | xargs -iabc aria2c -x 16 "$URL_PREFIX/abc"

cp /usr/lib/python3/dist-packages/nototools/merge_fonts.py .
cp /usr/lib/python3/dist-packages/nototools/merge_noto.py .
