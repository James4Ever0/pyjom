url = "https://anidb.net/anime/"
# query = "Yahari Ore no Seishun Lovecome wa Machigatte Iru."
query = "Yahari Ore no Seishun Love Come wa Machigatteiru."
params = {"adb.search": query, "do.update": "Search", "noalias": 1}

import pandas
import requests
import fake_useragent
ua = fake_useragent.UserAgent()
r = requests.get(url, params=params, headers={"User-Agent":ua.random}) # beautiful. really?

text = r.text
from bs4 import BeautifulSoup
soup = BeautifulSoup(text, "html.parser")

# print(soup) # forbidden? wtf?
# breakpoint()
import pandas
table = soup.find('table')

if not table:
    print('table not found.')
    breakpoint()
else:
    table_str = str(table)
    data = pandas.read_html(table_str)[0] # must be the first table.
    # now you have it. sorted?
    # print(data)
    # breakpoint()
    for index, videoDataFrame in data.iterrows():
        videoData = videoDataFrame.to_dict()
        title = videoData['Title']
        # where's the damn link? we don't need such thing.
        aired, ended = videoData['Aired'], videoData['Ended']
        print(f'[{index}] - {title}')