# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36
# 综合排序
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=click
# 最多点击
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=pubdate
# 最新发布
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=dm
# 最多弹幕
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=stow
# 最多收藏


class order:
    综合排序 = None
    最多点击 = "click"
    最新发布 = "pubdate"
    最多弹幕 = "dm"
    最多收藏 = "stow"


# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=stow&duration=1
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=stow&duration=2
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=stow&duration=3
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=stow&duration=4
class duration:
    全部时长 = None
    _10分钟以下 = 1
    _10_30分钟 = 2
    _30_60分钟 = 3
    _60分钟以上 = 4


# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&order=stow&duration=4&tids=1

# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&order=stow&duration=4&tids=24
class tids:
    全部分区 = None

# https://search.bilibili.com/article?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24&order=attention
# https://search.bilibili.com/article?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24&order=scores

class articleOrder:
    综合排序 = None
    最多点击 = "click"
    最新发布 = "pubdate"
    最多喜欢 = "attention"
    最多评论 = "scores"

# https://search.bilibili.com/live?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24
# https://search.bilibili.com/live?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24&search_type=live_user
# https://search.bilibili.com/live?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24&search_type=live_room

class liveSearchParams:
    全部 = None
    主播 = "live_user"
    直播间 = "live_room"

class searchEntry:
    综合"all"
    视频"video"
    番剧"bangumi"
    影视"pgc"
    直播"live"
    专栏"article"
    话题"topic"
    用户"upuser"
class bilibiliSearchParams:
    order = order
    duration = duration
    tids = tids
    searchEntry = searchEntry

class bilibiliArticleSearchParams:
    order = articleOrder

# bilibiliSearchParams.order.最多弹幕
print(bilibiliSearchParams.tids())