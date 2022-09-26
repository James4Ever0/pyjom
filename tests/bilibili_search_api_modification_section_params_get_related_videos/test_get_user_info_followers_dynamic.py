from bilibili_api import user, sync

u = user.User(660303135)

data = sync(u.get_relation_info())
# ["follower"]
# {'mid': 660303135, 'following': 34, 'whisper': 0, 'black': 0, 'follower': 1158}
# get followers less than 200 but view greater than 3000.
# also get that damn publish date!
print(data)
print(data.keys())
print(dir(u))
# you can also get followings to get the 'target video'
# ['credential', 'get_all_followings', 'get_article_list', 'get_articles', 'get_audios', 'get_channel_list', 'get_channel_videos_season', 'get_channel_videos_series', 'get_channels', 'get_cheese', 'get_dynamics', 'get_followers', 'get_followings', 'get_live_info', 'get_overview_stat', 'get_relation_info', 'get_subscribed_bangumi', 'get_uid', 'get_up_stat', 'get_user_info', 'get_videos', 'modify_relation', 'top_followers']
breakpoint()
# {'video': 79, 'bangumi': 15, 'cinema': 4, 'channel': {'master': 2, 'guest': 2}, 'favourite': {'master': 7, 'guest': 7}, 'tag': 0, 'article': 0, 'playlist': 0, 'album': 3, 'audio': 0, 'pugv': 0, 'season_num': 1}