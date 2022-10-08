import aiohttp
import asyncio

async def get(url):
    async with aiohttp.ClientSession() as session:
          async with session.get(url) as response:
                return response
loop = asyncio.get_event_loop()

multiple_requests = [get("http://your-website.com") for _ in range(10)]

results = loop.run_until_complete(asyncio.gather(*multiple_requests))

print("Results: %s" % results)