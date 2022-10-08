import asyncio
from contextlib import closing

import aiohttp


async def download_file(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        assert response.status == 200
        # For large files use response.content.read(chunk_size) instead.
        return url, await response.read()


@asyncio.coroutine
def download_multiple(session: aiohttp.ClientSession):
    urls = (
        'http://cnn.com',
        'http://nytimes.com',
        'http://google.com',
        'http://leagueoflegends.com',
        'http://python.org',
    )
    download_futures = [download_file(session, url) for url in urls]
    print('Results')
    for download_future in asyncio.as_completed(download_futures):
        result = yield from download_future
        print('finished:', result)
    return urls

async def main():
    with closing(asyncio.get_event_loop()) as loop:
        async with aiohttp.ClientSession() as session:
            result = loop.run_until_complete(download_multiple(session))
            print('finished:', result)
