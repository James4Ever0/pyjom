import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', type=str, default=None,required=True, help='music file to be recognized')
arguments = parser.parse_args()
# audioFile = "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3"
audioFile = arguments.file
import os
assert os.path.exists(audioFile)
import asyncio
from shazamio import Shazam

import json
async def main():
    shazam = Shazam()
    out = await shazam.recognize_song(audioFile)
    print(out)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
