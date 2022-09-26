from bilibili_api import user, sync

u = user.User(660303135)

# data = sync(u.get_relation_info())
# ["follower"]
# {'mid': 660303135, 'following': 34, 'whisper': 0, 'black': 0, 'follower': 1158}
# get followers less than 200 but view greater than 3000.
# also get that damn publish date!
# print(data)
# print(data.keys())
# print(dir(u))
# you can also get followings to get the 'target video'
potentialMethods = [
    "credential",#TypeError: 'Credential' object is not callable
error executing u.credential()
    "get_all_followings",
    "get_article_list",
    "get_articles",
    "get_audios",
    "get_channel_list",
    "get_channel_videos_season",#TypeError: get_channel_videos_season() missing 1 required positional argument: 'sid'
error executing u.get_channel_videos_season()
Traceback (most recent call last):
    "get_channel_videos_series",
    "get_channels",
    "get_cheese",
    "get_dynamics", # has offset parameter.
    "get_followers",
    "get_followings",
    "get_live_info",
    "get_overview_stat",
    "get_relation_info",
    "get_subscribed_bangumi",
    "get_uid",
    "get_up_stat",
    "get_user_info",
    "get_videos",
    "modify_relation",
    "top_followers",
]
# breakpoint()
# get_overview_stat()
import json

mdata = {}
import progressbar
for key in progressbar.progressbar(potentialMethods):
    command = "u.{}()".format(key)
    try:
        result = sync(eval(command))
        mdata.update({key:result})
        import time
        time.sleep(3)
    except:
        import traceback
        traceback.print_exc()
        print('error executing {}'.format(command))

mString = json.dumps(mdata, indent=4, ensure_ascii=False)
with open('user_data_api.json','w+') as f:
    f.write(mString)
print("DUMP COMPLETE")