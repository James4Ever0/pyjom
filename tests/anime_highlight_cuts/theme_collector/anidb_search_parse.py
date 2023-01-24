url = "https://anidb.net/anime/"
query = "Yahari Ore no Seishun Lovecome wa Machigatte Iru."
params = {"adb.search": query, "do.update": "Search", "noalias": 1}

import requests

r = requests.get(url, params=params)
text = r.text
from bs4 import BeautifulSoup
soup = BeautifulSoup(text, "html.parser")

print(soup)
breakpoint()