import pylrc
from MediaInfo import MediaInfo

def getMusicDuration(musicPath):
    info = MediaInfo(filename = musicPath)
    info = info.getInfo()
    # print(info)
    # breakpoint()
    length = info['duration']
    length = float(length)
    return length

def lrcCleaner()