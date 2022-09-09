# this is the complete process.
from lyrictoolbox import *
from .lyrictoolbox import getTextListTranslated

def lrcToAnimatedAss(musicPath, lrcPath, assPath): # will be moved to lyrictoolbox, and more styles incoming
    textArray = lrcToTextArray(musicPath, lrcPath)
    textList = [elem['text'] for elem in textArray]
    translatedList = getTextListTranslated(textList)
    # so we pass both arguments to the ass generator.
    

if __name__ == "__main__":
    musicPath= "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3"
    lrcPath = '/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.lrc'
    import os
    assPath = os.path.abspath('test.ass')
    lrcToAnimatedAss(musicPath, lrcPath,assPath)