import aiohttp
import asyncio

# clearly it is not clean enough.
# also i worry about the memory leakage, open file limit exceeding.
async def get(url):
    async with aiohttp.ClientSession() as session:
          async with session.get(url) as response:
                return response

def concurrentGet(url_list):
loop = asyncio.get_event_loop()
    multiple_requests = [get(url) for url in url_list]

    results = loop.run_until_complete(asyncio.gather(*multiple_requests))

    print("Results: %s" % results)