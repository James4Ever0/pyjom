# wget https://github.com/deezer/spleeter/raw/master/audio_example.mp3
# separate the example audio into two components
python3 -m spleeter separate -p spleeter:2stems -o output you_got_me.mp3
python3 -m spleeter separate -p spleeter:2stems -o output tarot_desc.mp3
# seems not working at all
