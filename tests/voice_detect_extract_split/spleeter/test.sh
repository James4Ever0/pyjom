# wget https://github.com/deezer/spleeter/raw/master/audio_example.mp3
# separate the example audio into two components
python3 -m spleeter separate -p spleeter:2stems -o output audio_example.mp3
# seems not working at all