from base_opq import *

##########TEST 1###########

target_qq = 2704439515

guishou_qq = 1585783722

target_qq_group = 537384511 # 鬼手的逆向交流群 没啥人啊


genshin_groups = searchGroup("原神")

add_friend_result = addFriend(target_qq,reason="可以一起聊天吗")

join_group_result = action.joinGroup(target_qq_group, content="进群学习呀")

print("JOIN GROUP RESULT: ", join_group_result) # do not send shit too frequently.

"""
SEARCH GROUP RESULT:  [{'GroupData': '富强、民主、文明、自由、平等、公正、法治、爱国、敬业、诚信、友善 本群坚持良好的', 'GroupDes': '富强、民主、文明、自由、平等、公正、法治、爱国、敬业、诚信、友善 本群坚持良好的聊天环境!\n在在本群可以进行交流游戏的各种玩法等等', 'GroupID': 822037142, 'GroupMaxMembers': 2000, 'GroupName': '原神交易交流群', 'GroupNotice': '', 'GroupOwner': 2463247170, 'GroupQuestion': '', 'GroupTotalMembers': 1521}, {'GroupData': '这里是原神交流群，请遵守群规，文明和谐交流\n\n\n。。。。。。。。。。。。。。。。。。', 'GroupDes': '这里是原神交流群，请遵守群规，文明和谐交流\n\n\n。。。。。。。。。。。。。。。。。。。。。', 'GroupID': 863235150, 'GroupMaxMembers': 2000, 'GroupName': '原神锄大地交流交流群', 'GroupNotice': '', 'GroupOwner': 847732226, 'GroupQuestion': '八重神子的真身是什么', 'GroupTotalMembers': 1679}, {'GroupData': '', 'GroupDes': '', 'GroupID': 910591672, 'GroupMaxMembers': 3000, 'GroupName': '淘气游原神交易⑥群', 'GroupNotice': '', 'GroupOwner': 4759120, 'GroupQuestion': '你为什么要加群？', 'GroupTotalMembers': 2741}, {'GroupData': '欢迎萌新', 'GroupDes': '欢迎萌新', 'GroupID': 925308474, 'GroupMaxMembers': 3000, 'GroupName': '原神交易交流群', 'GroupNotice': '', 'GroupOwner': 568461601, 'GroupQuestion': '本期up五星角色是？', 'GroupTotalMembers': 2551}, {'GroupData': '', 'GroupDes': '', 'GroupID': 1056201886, 'GroupMaxMembers': 2000, 'GroupName': '原神私服', 'GroupNotice': '', 'GroupOwner': 3084704124, 'GroupQuestion': '哪里看到的', 'GroupTotalMembers': 1973}, {'GroupData': '旅行者当你重新踏上旅途之后，一定要记得旅途本身的意义。 提瓦特的飞鸟、诗和城邦，', 'GroupDes': '旅行者当你重新踏上旅途之后，一定要记得旅途本身的意义。 提瓦特的飞鸟、诗和城邦，女皇、愚人和怪物……都是你旅途的一部分。 终点并不意味着一切，在抵达终点之前，用你的眼睛，多多观察这个世界吧……', 'GroupID': 469645427, 'GroupMaxMembers': 2000, 'GroupName': '原神萌新交流群', 'GroupNotice': '', 'GroupOwner': 3117482885, 'GroupQuestion': '本期武器池武器是什么', 'GroupTotalMembers': 1738}, {'GroupData': '可交易可交流 提供角色美图第一大群 要践行社会主义核心价值观：富强，民主，文明，和', 'GroupDes': '', 'GroupID': 708428072, 'GroupMaxMembers': 2000, 'GroupName': '原神交易交流群☀', 'GroupNotice': '', 'GroupOwner': 1362667067, 'GroupQuestion': '本期up池角色是谁', 'GroupTotalMembers': 1506}]
ADD FRIEND RESULT:  {'AddUserUid': 2704439515, 'AddType': 1, 'FromGroupID': 0, 'AddFromSource': 2020, 'Content': '可以一起聊天吗'}
❌ 07-04 21:44:46 ERROR 请求发送成功, 但处理失败 => {'Msg': '', 'Ret': 1}
JOIN GROUP RESULT:  {'Msg': '', 'Ret': 1}
"""
