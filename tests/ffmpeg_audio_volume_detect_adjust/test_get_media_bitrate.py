import test
from pyjom.audiotoolbox import getAudioBitrate

mediaPaths = [
    "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3", # 320000
    "/root/Desktop/works/pyjom/tests/ffmpeg_audio_volume_detect_adjust/normalized.mp4", # 130770
]
for mediaPath in mediaPaths:
    print("media path:", mediaPath)
    result = getAudioBitrate(mediaPath)
    print("RESULT:", result)
