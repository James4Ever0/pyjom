from bilibili_api import user, sync

u = user.User(660303135)

data = sync(u.get_relation_info())["follower"])