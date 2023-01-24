#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

url = "https://nyaa.si"

query = "oniichan wa oshimai! 01"
sort_term = "seeders"
category='1_0' # anime
page = 1 # start page: 1
params = dict(f=0,c=category,q=query,s=sort_term, o="desc",p=page)

# better parse it yourself first huh?

r = requests.get(url, params=params)
text = r.text

from bs4 import BeautifulSoup
#with open("output.html",'w+') as f:
#    f.write(text)
soup = BeautifulSoup(text, 'html.parser')
#breakpoint()

import parse

template = "Displaying results {start:d}-{end:d} out of {total:d} results."

banner = soup.find("div",class_="pagination-page-info").text
pagniation_info = banner.split("\n")[0]

pagination_info_result = parse.parse(template, pagination_info)

if pagination_info_result
if pagniation_info_result['total'] == pagination_info_result['']
