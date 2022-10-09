
from bilibili_api import favourite_list, s
# that favourite list is public. i just want that.
dedeuserid = "397424026"
favourite_list = favourite_list.get_video_favorite_list(int(dedeuserid))
print(favourite_list)