from bilibili_api import user, sync

u = user.User(660303135)

data = sync(u.get_relation_info())
# ["follower"]
print(data)
print(data.keys())
print(dir(u))
breakpoint()