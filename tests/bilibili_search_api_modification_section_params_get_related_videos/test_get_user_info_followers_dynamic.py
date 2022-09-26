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
[
    "credential",
    "get_all_followings",
    "get_article_list",
    "get_articles",
    "get_audios",
    # "get_channel_list",{'items_lists': {'page': {'page_num': 1, 'page_size': 3, 'total': 3}, 'seasons_list': [{'archives': [{'aid': 809029632, 'bvid': 'BV1P34y1C7UN', 'ctime': 1644811376, 'duration': 91, 'interactive_video': False, 'pic': 'http://i2.hdslb.com/bfs/archive/8757aa3ddf0cdda61c056d8af33378bebb321e35.jpg', 'pubdate': 1644811376, 'stat': {'view': 3456}, 'state': 0, 'title': '【管弦乐】小 白 兔 乐 团（《小白兔电商》OP《爱打工的小动物》）', 'ugc_pay': 0}, {'aid': 636597351, 'bvid': 'BV1vb4y147Ap', 'ctime': 1644811525, 'duration': 96, 'interactive_video': False, 'pic': 'http://i2.hdslb.com/bfs/archive/a801e070c121cb3be83be5888086efa5c4e06662.jpg', 'pubdate': 1644811525, 'stat': {'view': 658}, 'state': 0, 'title': '管弦乐工程展示-爱打工的小动物（《小白兔电商》OP）', 'ugc_pay': 0}], 'meta': {'category': 0, 'cover': 'https://archive.biliimg.com/bfs/archive/a801e070c121cb3be83be5888086efa5c4e06662.jpg', 'description': '', 'mid': 660303135, 'name': '合集·小白兔电商音乐', 'ptime': 1644811525, 'season_id': 193515, 'total': 2}, 'recent_aids': [809029632, 636597351]}], 'series_list': [{'archives': [{'aid': 769633755, 'bvid': 'BV1Dr4y1x7NQ', 'ctime': 1654418312, 'duration': 105, 'interactive_video': False, 'pic': 'http://i1.hdslb.com/bfs/archive/5813cf75dc28844957d4e307d0b258376a8ce5ee.jpg', 'pubdate': 1655481599, 'stat': {'view': 3165}, 'state': 0, 'title': '高性能亚托莉演奏管弦乐（Galgame《ATRI》OP《光放て！》Orchestra Ver.）', 'ugc_pay': 0}, {'aid': 939938164, 'bvid': 'BV13W4y1k7fc', 'ctime': 1654849965, 'duration': 175, 'interactive_video': False, 'pic': 'http://i2.hdslb.com/bfs/archive/4f0c69f69ad39bc577998aa1b89da568656a9957.jpg', 'pubdate': 1655028000, 'stat': {'view': 1609}, 'state': 0, 'title': '⭐🎂演“奏”管弦乐（《想要传达给你的爱恋》ED 管弦乐版《東の空から始まる世界》）', 'ugc_pay': 0}, {'aid': 636597351, 'bvid': 'BV1vb4y147Ap', 'ctime': 1644811525, 'duration': 96, 'interactive_video': False, 'pic': 'http://i2.hdslb.com/bfs/archive/a801e070c121cb3be83be5888086efa5c4e06662.jpg', 'pubdate': 1644811525, 'stat': {'view': 658}, 'state': 0, 'title': '管弦乐工程展示-爱打工的小动物（《小白兔电商》OP）', 'ugc_pay': 0}, {'aid': 809029632, 'bvid': 'BV1P34y1C7UN', 'ctime': 1644811376, 'duration': 91, 'interactive_video': False, 'pic': 'http://i2.hdslb.com/bfs/archive/8757aa3ddf0cdda61c056d8af33378bebb321e35.jpg', 'pubdate': 1644811376, 'stat': {'view': 3456}, 'state': 0, 'title': '【管弦乐】小 白 兔 乐 团（《小白兔电商》OP《爱打工的小动物》）', 'ugc_pay': 0}, {'aid': 976880770, 'bvid': 'BV1h44y1Y7uW', 'ctime': 1638108112, 'duration': 288, 'interactive_video': False, 'pic': 'http://i0.hdslb.com/bfs/archive/9e96581a2daaa478bb70196ebeacb43fffaab31d.jpg', 'pubdate': 1638108112, 'stat': {'view': 124}, 'state': 0, 'title': '【Nekopara】猫 猫 拉 提 琴（ED 陽だまりの香り 管弦乐）', 'ugc_pay': 0}, {'aid': 805381915, 'bvid': 'BV1s34y1Q7Kq', 'ctime': 1631195062, 'duration': 260, 'interactive_video': False, 'pic': 'http://i1.hdslb.com/bfs/archive/6d96ae0729d42957928bfe00b1ea695ab333657e.png', 'pubdate': 1631195062, 'stat': {'view': 1680}, 'state': 0, 'title': '管弦乐·魔卡少女樱OP - CLEAR', 'ugc_pay': 0}], 'meta': {'category': 1, 'cover': 'http://i1.hdslb.com/bfs/archive/5813cf75dc28844957d4e307d0b258376a8ce5ee.jpg', 'creator': '', 'ctime': 1639237729, 'description': '', 'keywords': ['管弦乐'], 'last_update_ts': 1655481602, 'mid': 660303135, 'mtime': 1655481602, 'name': 'ACG管弦', 'raw_keywords': '管弦乐', 'series_id': 589023, 'state': 2, 'total': 9}, 'recent_aids': [769633755, 939938164, 636597351, 809029632, 976880770, 805381915]}, {'archives': [{'aid': 338253248, 'bvid': 'BV1hR4y1M74L', 'ctime': 1642603095, 'duration': 130, 'interactive_video': False, 'pic': 'http://i1.hdslb.com/bfs/archive/d3c87feb9a51d6c4271f5ed6a63dae94dbf4ce1f.jpg', 'pubdate': 1642603095, 'stat': {'view': 70}, 'state': 0, 'title': 'osu 摆烂 19/20（算错了，其实已经够了）', 'ugc_pay': 0}, {'aid': 253342116, 'bvid': 'BV1qY411b7fB', 'ctime': 1642595967, 'duration': 161, 'interactive_video': False, 'pic': 'http://i1.hdslb.com/bfs/archive/a1a7402b1fa6623da181a1270e5ead25752ce81b.jpg', 'pubdate': 1642595967, 'stat': {'view': 20}, 'state': 0, 'title': '摆烂 osu18/20', 'ugc_pay': 0}, {'aid': 893366309, 'bvid': 'BV1dP4y177V1', 'ctime': 1642502942, 'duration': 276, 'interactive_video': False, 'pic': 'http://i2.hdslb.com/bfs/archive/6c3c0b3e3fd1474b09ab13c5d3299de08f876076.jpg', 'pubdate': 1642502942, 'stat': {'view': 22}, 'state': 0, 'title': '摆烂 osu17/20', 'ugc_pay': 0}, {'aid': 978220671, 'bvid': 'BV1w44y1L7Pb', 'ctime': 1642419143, 'duration': 260, 'interactive_video': False, 'pic': 'http://i2.hdslb.com/bfs/archive/bd9fe94a04631baaf7350ea9e8a6dda85142b3b0.jpg', 'pubdate': 1642419143, 'stat': {'view': 33}, 'state': 0, 'title': '摆烂 osu16/20', 'ugc_pay': 0}, {'aid': 247985745, 'bvid': 'BV16v411j7gC', 'ctime': 1620147165, 'duration': 262, 'interactive_video': False, 'pic': 'http://i2.hdslb.com/bfs/archive/bfaf8ac589331c27ad28c36bfe851baaa69a7173.jpg', 'pubdate': 1620147164, 'stat': {'view': 738}, 'state': 0, 'title': '智 乃 弹 钢 琴（VR Chat）', 'ugc_pay': 0}, {'aid': 375398879, 'bvid': 'BV14o4y127o5', 'ctime': 1620490555, 'duration': 999, 'interactive_video': False, 'pic': 'http://i0.hdslb.com/bfs/archive/24218a0d0eab8d81e31b94e08501149a518d9b5f.jpg', 'pubdate': 1620490555, 'stat': {'view': 160}, 'state': 0, 'title': '【节奏光剑自制谱】Candy a Mine（Galgame 《しゅがてん》 OP Full Size）', 'ugc_pay': 0}], 'meta': {'category': 1, 'cover': 'http://i1.hdslb.com/bfs/archive/d3c87feb9a51d6c4271f5ed6a63dae94dbf4ce1f.jpg', 'creator': '', 'ctime': 1639237729, 'description': '', 'keywords': ['游戏'], 'last_update_ts': 1642859245, 'mid': 660303135, 'mtime': 1642859245, 'name': '打电动', 'raw_keywords': '游戏', 'series_id': 589020, 'state': 2, 'total': 41}, 'recent_aids': [338253248, 253342116, 893366309, 978220671, 247985745, 375398879]}]}}
    "get_channel_videos_season",
    "get_channel_videos_series",
    "get_channels",
    "get_cheese",
    "get_dynamics",
    "get_followers",
    "get_followings",
    "get_live_info",
    "get_overview_stat",# {'video': 79, 'bangumi': 15, 'cinema': 4, 'channel': {'master': 2, 'guest': 2}, 'favourite': {'master': 7, 'guest': 7}, 'tag': 0, 'article': 0, 'playlist': 0, 'album': 3, 'audio': 0, 'pugv': 0, 'season_num': 1}
    "get_relation_info",
    "get_subscribed_bangumi",
    "get_uid",
    "get_up_stat",
    "get_user_info",
    "get_videos",
    "modify_relation",
    "top_followers",
]
breakpoint()
# get_overview_stat()
