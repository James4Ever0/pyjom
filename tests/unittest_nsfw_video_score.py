# we take max for the concerned ones, and take mean for the unconcerned ones.

from test_commons import *
import requests

gateway = "localhost:8080/nsfw"
source = ""
from lazero.filesystem import tmpdir

r = requests.post(gateway,) # post gif?
# you can only post gif now, or you want to post some other formats?
# if you post shit, you know it will strentch your picture and produce unwanted shits.