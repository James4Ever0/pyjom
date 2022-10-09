from bilibili_api.user import get_self_info
# from bilibili_api import settings
# how to load credential from our stored things?
credential = Credential()
from bilibili_api import sync
name = sync(get_self_info(credential))['name']
