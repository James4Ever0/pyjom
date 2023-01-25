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
similarAnime = soup.find(attrs={"id":"similaranime"})
indirectRelated = soup.find(attrs={"id":"relations_indirect"})
directRelated = soup.find(attrs={"id":"relations_direct"}) # it could be none.

tables = soup.find_all('table') # shit.

videoInfo = 

# i think monad is good.

import pandas
SAData = pandas.read_html(similarAnime)
print(SAData)
breakpoint()