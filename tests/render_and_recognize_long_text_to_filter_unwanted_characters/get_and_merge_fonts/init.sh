URL_PREFIX="https://raw.githubusercontent.com/"

echo "GoNotoAfricaMiddleEast.ttf
GoNotoAncient.ttf
GoNotoAncientSerif.ttf
GoNotoAsiaHistorical.ttf
GoNotoCJKCore.ttf
GoNotoCurrent.ttf
GoNotoCurrentSerif.ttf
GoNotoEastAsia.ttf
GoNotoEuropeAmericas.ttf
GoNotoSouthAsia.ttf
GoNotoSouthEastAsia.ttf
" | xargs -iabc curl -O -L "$URL_PREFIX/abc"