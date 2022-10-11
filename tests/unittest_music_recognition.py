from test_commons import *
from pyjom.musictoolbox import recognizeMusicFromFile

filepath = 
methods = ["songrec", "shazamio", "midomi"]
for method in methods:
    result = recognizeMusicFromFile(filepath, backend = method)