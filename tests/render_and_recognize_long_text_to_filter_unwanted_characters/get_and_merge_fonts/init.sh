URL_PREFIX="https://proxy.zyun.vip/https://github.com/satbyy/go-noto-universal/releases/download/v5.2"

cat fonts.log | xargs -iabc curl -O -L "$URL_PREFIX/abc"

cp /usr/lib/python3/dist-packages/nototools/merge_fonts.py .
cp /usr/lib/python3/dist-packages/nototools/merge_noto.py .