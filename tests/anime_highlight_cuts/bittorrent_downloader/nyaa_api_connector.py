#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

url = "https://nyaa.si"

query = "oniichan"
s = "seeders"
category='1_0' # anime
params = dict(f=0,c=category,q=query,s=sort_term, o="desc")

# better parse it yourself first huh?
