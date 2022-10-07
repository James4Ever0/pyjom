import test
from pyjom.audiotoolbox import getAudioDuration

audioPath = ""
audioDuration = getAudioDuration(audioPath)
print('audioDuration:', audioDuration)