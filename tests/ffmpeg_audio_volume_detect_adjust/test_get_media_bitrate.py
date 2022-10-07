from test import getAudioBitrate

mediaPaths = ["","/root/Desktop/works/pyjom/tests/ffmpeg_audio_volume_detect_adjust/normalized.mp4"]
for mediaPath in mediaPaths:
    result = getAudioBitrate(mediaPath)