from bilibili_api import user, sync

u = user.User(660303135)

data = sync(u.get_relation_info())
# ["follower"]
# {'mid': 660303135, 'following': 34, 'whisper': 0, 'black': 0, 'follower': 1158}
# get 
print(data)
print(data.keys())
print(dir(u))
breakpoint()