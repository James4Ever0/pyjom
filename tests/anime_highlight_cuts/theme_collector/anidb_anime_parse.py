from black import NothingChanged


url = "https://anidb.net/anime/9310"
from pymonad.maybe import Nothing, Just

def checkNothing(value):
    if value in [None, 0, -1, [], {},()]:
        return Nothing
    return Just(value)

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

videoInfo = checkNothing(soup.find("div", attrs={"class":["pane", "info"]})).
if videoInfo:
    videoInfo = videoInfo.find('table')
videoTitles = checkNothing(soup.find("div", attrs={"class":["pane", "titles"]})).
if videoTitles:
    videoTitles = videoTitles.find('table')

# i think monad is good.

import pandas
SAData = pandas.read_html(similarAnime)
print(SAData)
breakpoint()