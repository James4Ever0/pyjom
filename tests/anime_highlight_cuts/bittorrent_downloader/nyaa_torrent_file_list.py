url = "https://nyaa.si/view/1627038"

import requests

from NyaaPy import utils, torrent

r = requests.get(url)
SITE = utils.TorrentSite.NYAASI

json_data = utils.parse_single(request_text=r.text, site=SITE)

data_class = torrent.json_to_class(json_data)

breakpoint()