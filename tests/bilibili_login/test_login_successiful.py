from bilibili_api.user import get_self_info
# from bilibili_api import settings
credential = 
from bilibili_api import sync
name = sync(get_self_info(credential))['name']
