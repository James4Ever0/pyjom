URL_PREFIX="https://proxy.zyun.vip/https://github.com/satbyy/go-noto-universal/releases/download/v5.2"

cat fonts.log | xargs -iabc curl -O -L "$URL_PREFIX/abc"