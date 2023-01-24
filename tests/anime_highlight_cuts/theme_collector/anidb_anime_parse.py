url = "https://anidb.net/anime/9310"


import requests
import fake_useragent
ua = fake_useragent.UserAgent()
r = requests.get(url, headers={"User-Agent":ua.random}) 

text = r.text
with open("anidb_info.html", 'w+') as f:
    f.write(text)

text = f.read()

from bs4 import BeautifulSoup
soup = BeautifulSoup(text, 'html.parser')
# must be non-empty.
similarAnime = str(soup.select("#similaranime")[0])
indirectRelated = str(soup.select('#relations_indirect')[0])
directRelated = str(soup.select('#relations_direct')[0])

tables = soup.find_all('table') # shit.

import pandas
SAData = pandas.read_html(similarAnime)
print(SAData)
breakpoint()