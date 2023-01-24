#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

url = "https://nyaa.si"

query = "oniichan wa oshimai! 01"
s = "seeders"
category='1_0' # anime
params = dict(f=0,c=category,q=query,s=sort_term, o="desc")

# better parse it yourself first huh?

r = requests.get(url, params=params)
text = r.text

from bs4 import BeautifulSoup
with open("output.html",)
soup = BeautifulSoup(text, )
