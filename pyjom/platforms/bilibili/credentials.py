# you need to manage login/logout and credential storage.
# first you need to get 'home' directory
from lazero.search.api import getHomeDirectory
import os

home = getHomeDirectory()
dbPath = os.path.join(home, ".bilibili_api.json")
import tinydb
db= 