import test
from pyjom.audiotoolbox import getAudioDuration

audioPath = "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3"

audioDuration = getAudioDuration(audioPath)
print("audioDuration:", audioDuration)
# audioDuration: 302.915918367
# obviously floating point duration.
