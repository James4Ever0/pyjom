url = "https://nyaa.si/view/1627038"

import requests

from NyaaPy import utils
json_data = utils.parse_single(request_text=r.text, site=self.SITE)

return torrent.json_to_class(json_data)