curl -O -L https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems.tar.gz
curl -O -L https://github.com/deezer/spleeter/releases/download/v1.4.0/4stems.tar.gz
curl -O -L https://github.com/deezer/spleeter/releases/download/v1.4.0/5stems.tar.gz

mv {2stems.tar.gz, 4stems.tar.gz, 5stems.tar.gz} pretrained_models
cd pretrained_models