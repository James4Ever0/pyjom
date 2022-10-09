from bilibili_api.user import get_self_info
# from bilibili_api import settings
# how to load credential from our stored things?

from lazero.search.api import getHomeDirectory
import os

home = getHomeDirectory()
dbPath = os.path.join(home, ".bilibili_api.json")
import tinydb
credential = Credential()
from bilibili_api import sync
name = sync(get_self_info(credential))['name']
