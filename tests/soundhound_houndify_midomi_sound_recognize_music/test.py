# url = "wss://houndify.midomi.com/"

# import asyncio
# import websockets

# async def hello():
#     async with websockets.connect(url) as websocket:
#         await websocket.send({ "version": "1.0" })
#         await websocket.recv()

# asyncio.run(hello())
# the nodejs works for soundhound right now.
# move upon other platforms: shazam (2 tools), netease.
# shazam works for our chinese songs. one problem: it has traditional chinese.
# better convert traditional chinese to simplified chinese, for better searching experience.
# or you bet it. maybe another way of censorship circumvention?
# apt-get install opencc

# you need to filter out those parts without singing voice, if download music from kugou/qq music

audioFile = "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3"

import asyncio
from shazamio import Shazam


async def main():
    shazam = Shazam()
    out = await shazam.recognize_song(audioFile)
    print(out)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
