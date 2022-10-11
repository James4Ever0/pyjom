from test_commons import *
from pyjom.musictoolbox import recognizeMusicFromFile
from lazero.utils.logger import sprint

filepath = (
    # "/root/Desktop/works/pyjom/tests/music_recognization/exciting_bgm_cut_10seconds.mp3"
    "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3"
)
# methods = ["midomi"]
methods = ["songrec", "shazamio", "midomi"]
import time

for method in methods:
    result = recognizeMusicFromFile(filepath, backend=method, debug=True)
    sprint("RESULT:", result)
    time.sleep(3)
