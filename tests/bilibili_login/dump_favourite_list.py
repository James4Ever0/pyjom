
from bilibili_api import favorite_list, sync
# that favourite list is public. i just want that.
dedeuserid = "397424026"
favourite_list = sync(favorite_list.get_video_favorite_list(int(dedeuserid)))
print(favourite_list) # None? wtf?