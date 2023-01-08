# this is the complete process.
from lyrictoolbox import *

# from .lyrictoolbox import previewAssWithVideo
# from .lyrictoolbox import getTextListTranslated

if __name__ == "__main__":
    musicPath = "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3"
    lrcPath = "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.lrc"
    sample_video = "/root/Desktop/works/pyjom/samples/video/karaoke_effects_source.mp4"
    import os

    assPath = os.path.abspath("test.ass")
    lrcToAnimatedAss(musicPath, lrcPath, assPath)
    previewAssWithVideo(sample_video, assPath)
