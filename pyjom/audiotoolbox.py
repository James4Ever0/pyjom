# first and foremost is the audio correction, the volume detector, the audio detector.
# https://trac.ffmpeg.org/wiki/AudioVolume

# but first how to get the audio duration?
# for video we have caer. but for audio?

import audioread

def getAudioDuration(audioFilePath):
    with audioread.audio_open(audioFilePath)