url = "wss://houndify.midomi.com/"

import asyncio
import websockets

async def hello():
    async with websockets.connect(url) as websocket:
        await websocket.send({})
        await websocket.recv()

asyncio.run(hello())