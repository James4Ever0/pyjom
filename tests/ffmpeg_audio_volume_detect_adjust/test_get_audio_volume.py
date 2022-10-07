import test
from pyjom.audiotoolbox import getAudioDuration

audioPath = (
    "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3",
)  # 320000

audioDuration = getAudioDuration(audioPath)
print("audioDuration:", audioDuration)
