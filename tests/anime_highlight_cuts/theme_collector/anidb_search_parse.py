url = "https://anidb.net/anime/"
query = "Yahari Ore no Seishun Lovecome wa Machigatte Iru."
params = {"adb.search": query, "do.update": "Search", "noalias": 1}

import requests
import fake_useragent
ua = fake_useragent.UserAgent()
r = requests.get(url, params=params, headers={"User-Agent":ua.random})
text = r.text
from bs4 import BeautifulSoup
soup = BeautifulSoup(text, "html.parser")

print(soup) # forbidden? wtf?
breakpoint()