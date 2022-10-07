import requests
from . import storage
from .components import load_components

DRIVE = True

class Core(object):
    def __init__(self):
        self.alive, self.isLogging = False, False
        self.storageClass = storage.Storage(self)
        self.memberList = self.storageClass.memberList
        self.mpList = self.storageClass.mpList
        self.chatroomList = self.storageClass.chatroomList
        self.msgList = self.storageClass.msgList
        self.loginInfo = {}
        self.changedrive = True if DRIVE else False
        self.s = requests.Session()
        self.uuid = None
        self.functionDict = {'FriendChat': {}, 'GroupChat': {}, 'MpChat': {}}
        self.useHotReload, self.hotReloadDir = False, 'linuxchat.pkl'
        self.receivingRetryCount = 5
    def login(self, enableCmdQR=False, picDir=None, qrCallback=None,
            loginCallback=None, exitCallback=None,overtime = 120):
        '''
        微信登陆入口：
        enableCmdQR:二维码显示方式，False:显示图片，True:命令行显示二维码
        picDir：二维码下载保存地址
        qrCallback:传入生成二维码时回调的函数,回调时自动传入（uuid，"stat",及二维码的二进制数据）三个数据
        loginCallback：传入登陆成功时回调的函数，无传参
        exitCallback：传入退出登陆时的回调函数，无传参
        overtime：扫码限制时长，单位（秒）
        '''
        raise NotImplementedError()
    def get_QRuuid(self):
        '''
        获取uuid
        登陆第一步，必须获取uuid
        返回：uuid
        '''
        raise NotImplementedError()
    def get_QR(self, uuid=None, enableCmdQR=False, picDir=None, qrCallback=None):
        '''
        获取二维码
        uuid:二维码标识
        enableCmdQR：二维码显示方式，False:显示图片，True:命令行显示二维码
        picDir：二维码下载保存地址
        qrCallback:传入生成二维码时回调的函数,回调时自动传入（uuid，"stat",及二维码的二进制数据）三个数据
        返回：二维码数据
        '''
        raise NotImplementedError()
    def check_login(self, uuid=None):
        '''
        检查登陆状态
        '''
        raise NotImplementedError()
    def web_init(self):
        '''
        登陆初始化
        登陆成功后调用，初始化微信数据
        '''
        raise NotImplementedError()
    def start_receiving(self, exitCallback=None, getReceivingFnOnly=False):
        '''
        初始化成功后调用，开始接收数据
        exitCallback：传入退出登陆时的回调函数，无传参
        getReceivingFnOnly：是否使用多线程接收数据
        '''
        raise NotImplementedError()
    def get_msg(self):
        '''
        获取消息内容
        返回：{'MsgId': '4707672142477593330', 'FromUserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'ToUserName': '@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa', 'MsgType': 1, 'Content': '个非寻', 'Status': 3, 'ImgStatus': 1, 'CreateTime': 1652707857, 'VoiceLength': 0, 'PlayLength': 0, 'FileName': '', 'FileSize': '', 'MediaId': '', 'Url': '', 'AppMsgType': 0, 'StatusNotifyCode': 0, 'StatusNotifyUserName': '', 'RecommendInfo': {'UserName': '', 'NickName': '', 'QQNum': 0, 'Province': '', 'City': '', 'Content': '', 'Signature': '', 'Alias': '', 'Scene': 0, 'VerifyFlag': 0, 'AttrStatus': 0, 'Sex': 0, 'Ticket': '', 'OpCode': 0}, 'ForwardFlag': 0, 'AppInfo': {'AppID': '', 'Type': 0}, 'HasProductId': 0, 'Ticket': '', 'ImgHeight': 0, 'ImgWidth': 0, 'SubMsgType': 0, 'NewMsgId': 4707672142477593330, 'OriContent': '', 'EncryFileName': '', 'ActualNickName': '小小将', 'IsAt': False, 'ActualUserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'User': <Chatroom: {'MemberList': <ContactList: [<ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': '', 'PYQuanPin': '', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': ''}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469', 'NickName': '革命小将', 'AttrStatus': 104829, 'PYInitial': '', 'PYQuanPin': '', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': ''}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840', 'NickName': '卢取', 'AttrStatus': 104485, 'PYInitial': '', 'PYQuanPin': '', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': ''}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d', 'NickName': '不知不道', 'AttrStatus': 17010789, 'PYInitial': '', 'PYQuanPin': '', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': ''}>]>, 'Uin': 0, 'UserName': '@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa', 'NickName': '哈哈哈拉', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=754697486&username=@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa&skey=', 'ContactFlag': 3, 'MemberCount': 4, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'HHHL', 'PYQuanPin': 'hahahala', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 1, 'AttrStatus': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 0, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 1, 'IsAdmin': None, 'Self': <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': '', 'PYQuanPin': '', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': ''}>}>, 'Type': 'Text', 'Text': '个非寻'}
        '''
        raise NotImplementedError()
    def logout(self):
        '''
        退出登陆
        '''
        raise NotImplementedError()
    def update_chatroom(self, userName, detailedMember=False):
        '''
        更新并返回群信息
        userName：群id
        detailedMember：是否更新群成员信息
        返回：{'MemberList': <ContactList: [<ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469', 'NickName': '革命小将', 'AttrStatus': 104829, 'PYInitial': 'GMXJ', 'PYQuanPin': 'gemingxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754689414&username=@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469&skey=', 'ContactFlag': 8388611, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 2, 'Signature': '健康   开心', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 1, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840', 'NickName': '༺初心༻', 'AttrStatus': 104485, 'PYInitial': '?CX?', 'PYQuanPin': '?chuxin?', 'RemarkPYInitial': 'LQ', 'RemarkPYQuanPin': 'luqu', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754694371&username=@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '卢取', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '命里有时终需有\n                              命里无时莫强求', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 257, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d', 'NickName': '不知不道', 'AttrStatus': 17010789, 'PYInitial': 'BZBD', 'PYQuanPin': 'buzhibudao', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=718660439&username=@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '甘肃', 'City': '金昌', 'Alias': '', 'SnsFlag': 273, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>]>, 'Uin': 0, 'UserName': '@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa', 'NickName': '哈哈哈拉', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=754697486&username=@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa&skey=', 'ContactFlag': 3, 'MemberCount': 4, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'HHHL', 'PYQuanPin': 'hahahala', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 1, 'AttrStatus': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 0, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 1, 'IsAdmin': None, 'Self': <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>}
        '''
        raise NotImplementedError()
    def update_friend(self, userName):
        '''
        更新好友信息
        userName：好友id
        返回：{'MemberList': <ContactList: [<ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469', 'NickName': '革命小将', 'AttrStatus': 104829, 'PYInitial': 'GMXJ', 'PYQuanPin': 'gemingxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754689414&username=@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469&skey=', 'ContactFlag': 8388611, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 2, 'Signature': '健康   开心', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 1, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840', 'NickName': '༺初心༻', 'AttrStatus': 104485, 'PYInitial': '?CX?', 'PYQuanPin': '?chuxin?', 'RemarkPYInitial': 'LQ', 'RemarkPYQuanPin': 'luqu', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754694371&username=@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '卢取', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '命里有时终需有\n                              命里无时莫强求', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 257, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d', 'NickName': '不知不道', 'AttrStatus': 17010789, 'PYInitial': 'BZBD', 'PYQuanPin': 'buzhibudao', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=718660439&username=@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '甘肃', 'City': '金昌', 'Alias': '', 'SnsFlag': 273, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>]>, 'Uin': 0, 'UserName': '@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa', 'NickName': '哈哈哈拉', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=754697486&username=@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa&skey=', 'ContactFlag': 3, 'MemberCount': 4, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'HHHL', 'PYQuanPin': 'hahahala', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 1, 'AttrStatus': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 0, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 1, 'IsAdmin': None, 'Self': <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>}
        '''
        raise NotImplementedError()
    def get_contact(self, update=False):
        '''
        获取通讯录信息（只有保存到通讯录的群才能获取到）
        update：True→返回本地通讯录信息，False→更新本地通讯录后再返回
        返回：{'MemberList': <ContactList: [<ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469', 'NickName': '革命小将', 'AttrStatus': 104829, 'PYInitial': 'GMXJ', 'PYQuanPin': 'gemingxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754689414&username=@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469&skey=', 'ContactFlag': 8388611, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 2, 'Signature': '健康   开心', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 1, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840', 'NickName': '༺初心༻', 'AttrStatus': 104485, 'PYInitial': '?CX?', 'PYQuanPin': '?chuxin?', 'RemarkPYInitial': 'LQ', 'RemarkPYQuanPin': 'luqu', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754694371&username=@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '卢取', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '命里有时终需有\n                              命里无时莫强求', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 257, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d', 'NickName': '不知不道', 'AttrStatus': 17010789, 'PYInitial': 'BZBD', 'PYQuanPin': 'buzhibudao', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=718660439&username=@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '甘肃', 'City': '金昌', 'Alias': '', 'SnsFlag': 273, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>]>, 'Uin': 0, 'UserName': '@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa', 'NickName': '哈哈哈拉', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=754697486&username=@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa&skey=', 'ContactFlag': 3, 'MemberCount': 4, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'HHHL', 'PYQuanPin': 'hahahala', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 1, 'AttrStatus': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 0, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 1, 'IsAdmin': None, 'Self': <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>}
        '''
        raise NotImplementedError()
    def get_friends(self, update=False):
        '''
        获取好友列表
        update：True→返回本地好友信息，False→更新本地好友后再返回
        返回：{'MemberList': <ContactList: [<ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469', 'NickName': '革命小将', 'AttrStatus': 104829, 'PYInitial': 'GMXJ', 'PYQuanPin': 'gemingxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754689414&username=@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469&skey=', 'ContactFlag': 8388611, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 2, 'Signature': '健康   开心', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 1, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840', 'NickName': '༺初心༻', 'AttrStatus': 104485, 'PYInitial': '?CX?', 'PYQuanPin': '?chuxin?', 'RemarkPYInitial': 'LQ', 'RemarkPYQuanPin': 'luqu', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754694371&username=@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '卢取', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '命里有时终需有\n                              命里无时莫强求', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 257, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d', 'NickName': '不知不道', 'AttrStatus': 17010789, 'PYInitial': 'BZBD', 'PYQuanPin': 'buzhibudao', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=718660439&username=@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '甘肃', 'City': '金昌', 'Alias': '', 'SnsFlag': 273, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>]>, 'Uin': 0, 'UserName': '@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa', 'NickName': '哈哈哈拉', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=754697486&username=@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa&skey=', 'ContactFlag': 3, 'MemberCount': 4, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'HHHL', 'PYQuanPin': 'hahahala', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 1, 'AttrStatus': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 0, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 1, 'IsAdmin': None, 'Self': <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>}
        '''
        raise NotImplementedError()
    def get_chatrooms(self, update=False, contactOnly=False):
        '''
        获取群列表（只有保存到通讯录的群才能获取到）
        update：True→返回本地群聊信息，False→更新本地群聊信息后再返回
        contactOnly：True→只返回聊天列表中的群信息，False→返回所有通讯录中的群信息
        返回：{'MemberList': <ContactList: [<ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469', 'NickName': '革命小将', 'AttrStatus': 104829, 'PYInitial': 'GMXJ', 'PYQuanPin': 'gemingxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754689414&username=@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469&skey=', 'ContactFlag': 8388611, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 2, 'Signature': '健康   开心', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 1, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840', 'NickName': '༺初心༻', 'AttrStatus': 104485, 'PYInitial': '?CX?', 'PYQuanPin': '?chuxin?', 'RemarkPYInitial': 'LQ', 'RemarkPYQuanPin': 'luqu', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754694371&username=@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '卢取', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '命里有时终需有\n                              命里无时莫强求', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 257, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d', 'NickName': '不知不道', 'AttrStatus': 17010789, 'PYInitial': 'BZBD', 'PYQuanPin': 'buzhibudao', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=718660439&username=@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '甘肃', 'City': '金昌', 'Alias': '', 'SnsFlag': 273, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>]>, 'Uin': 0, 'UserName': '@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa', 'NickName': '哈哈哈拉', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=754697486&username=@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa&skey=', 'ContactFlag': 3, 'MemberCount': 4, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'HHHL', 'PYQuanPin': 'hahahala', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 1, 'AttrStatus': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 0, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 1, 'IsAdmin': None, 'Self': <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>}
        '''
        raise NotImplementedError()
    def get_mps(self, update=False):
        '''
        获取公众号列表
        update：True→返回本地好友信息，False→更新本地好友后再返回
        返回：{'MemberList': <ContactList: [<ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469', 'NickName': '革命小将', 'AttrStatus': 104829, 'PYInitial': 'GMXJ', 'PYQuanPin': 'gemingxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754689414&username=@42da0222d811f0350bd49071a85ed5dfcaa2bb95b5ba7986eef1d56c5bd36469&skey=', 'ContactFlag': 8388611, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 2, 'Signature': '健康   开心', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 1, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840', 'NickName': '༺初心༻', 'AttrStatus': 104485, 'PYInitial': '?CX?', 'PYQuanPin': '?chuxin?', 'RemarkPYInitial': 'LQ', 'RemarkPYQuanPin': 'luqu', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=754694371&username=@fdada0992c758acfae1ec11a5d6bd011c717db502e25d9281379142d301e6840&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '卢取', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '命里有时终需有\n                              命里无时莫强求', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 257, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>, <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d', 'NickName': '不知不道', 'AttrStatus': 17010789, 'PYInitial': 'BZBD', 'PYQuanPin': 'buzhibudao', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=718660439&username=@75cea6c4f10890ed225f732aeb0d28b141a58d9e4f2414f4527a575594df5f8d&skey=', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '甘肃', 'City': '金昌', 'Alias': '', 'SnsFlag': 273, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>]>, 'Uin': 0, 'UserName': '@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa', 'NickName': '哈哈哈拉', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=754697486&username=@@2fa6b3e5bc2a3e5c18297db4e0ae41d5414337ea8bda26c51e5c8797246d73aa&skey=', 'ContactFlag': 3, 'MemberCount': 4, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'HHHL', 'PYQuanPin': 'hahahala', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 1, 'AttrStatus': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 0, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 1, 'IsAdmin': None, 'Self': <ChatroomMember: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06', 'NickName': '小小将', 'AttrStatus': 102437, 'PYInitial': 'XXJ', 'PYQuanPin': 'xiaoxiaojiang', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'MemberStatus': 0, 'DisplayName': '', 'KeyWord': '', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=0&username=@d14ba932290258d2a70fa43492e28b94c0ad57b0369434227ecf699389f4cb06&chatroomid=@e211d8401f1957a595de043a2efd1e59&skey=', 'ContactFlag': 0, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 0, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 256, 'UniFriend': 0, 'ChatRoomId': 0, 'EncryChatRoomId': '@e211d8401f1957a595de043a2efd1e59', 'IsOwner': 0}>}
        '''
        raise NotImplementedError()
    def set_alias(self, userName, alias):
        '''
        修改联系人备注
        userName：联系人id
        alias：修改后的备注
        '''
        raise NotImplementedError()
    def set_pinned(self, userName, isPinned=True):
        '''
        将联系人或群置顶
        userName：联系人或群id
        isPinned:是否设置手机同步置顶
        '''
        raise NotImplementedError()
    def accept_friend(self, userName, v4,autoUpdate=True):
        '''
        自动同意添加好友请求
        userName：对方微信id
        v4：v4数据，可在收到添加好友消息时获取
        autoUpdate：是否自动更新本地好友列表
        '''
        raise NotImplementedError()
    def get_head_img(self, userName=None, chatroomUserName=None, picDir=None):
        '''
        获取好友或群头像
        userName：联系人id
        chatroomUserName：群id
        picDir：头像保存地址，为空则返回头像的二进制数据
        '''
        raise NotImplementedError()
    def create_chatroom(self, memberList, topic=''):
        '''
        创建群
        memberList：初始群成员的id，多个成员用英文半角逗号隔开
        topic：群的昵称
        '''
        raise NotImplementedError()
    def set_chatroom_name(self, chatroomUserName, name):
        '''
        修改群昵称
        chatroomUserName：群id
        name：修改后的昵称
        '''
        raise NotImplementedError()
    def delete_member_from_chatroom(self, chatroomUserName, memberList):
        '''
        删除群成员
        chatroomUserName：群id
        memberList：删除群成员的id，多个成员用英文半角逗号隔开
        该接口可能失效
        '''
        raise NotImplementedError()
    def add_member_into_chatroom(self, chatroomUserName, memberList,
            useInvitation=False):
        '''
        添加/要求好友进群
        chatroomUserName：群id
        memberList：删除群成员的id，多个成员用英文半角逗号隔开
        useInvitation：True→以邀请的方式 False→直接添加
        '''
        raise NotImplementedError()
    def send_raw_msg(self, msgType,content, FromUserName,toUserName, MediaId=''):
        '''
        转发消息
        msgType：消息类型
        content：消息内容
        FromUserName：发给你消息的联系人或群id
        toUserName：你要转发的对象id
        MediaId：在收到的消息中获取
        '''
        raise NotImplementedError()
    def send_msg(self, msg='Hello world', toUserName=None):
        '''
        发送文本消息
        msg：消息内容
        toUserName：对方的id
        '''
        raise NotImplementedError()
    def upload_file(self, fileDir, isPicture=False, isVideo=False,toUserName='filehelper', file_=None, preparedFile=None):
        '''
        上传文件到微信服务器
        fileDir：文件路径
        isPicture：是否是图片
        isVideo：是否是视频
        toUserName：默认存储到文件助手下
        file_：文件检测，默认
        preparedFile：文件检测，默认
        返回：MediaId
        '''
        raise NotImplementedError()
    def send_file(self, fileDir, toUserName=None, mediaId=None, file_=None):
        '''
        发送文件
        fileDir：文件路径
        toUserName：对方id
        mediaId：如果已经上传文件到服务器可以直接传入该参数
        '''
        raise NotImplementedError()
    def send_image(self, fileDir=None, toUserName=None, mediaId=None, file_=None):
        '''
        发送图片消息
        fileDir：文件路径
        toUserName：对方id
        mediaId：如果已经上传文件到服务器可以直接传入该参数
        '''
        raise NotImplementedError()
    def send_video(self, fileDir=None, toUserName=None, mediaId=None, file_=None):
        '''
        发视频消息
        fileDir：文件路径
        toUserName：对方id
        mediaId：如果已经上传文件到服务器可以直接传入该参数
        '''
        raise NotImplementedError()
    def revoke(self, msgId, toUserName, localId=None):
        '''
        撤回消息
        msgId：消息id，发送消息时会返回该数据
        toUserName：对方联系人或群id
        localId：本地时间戳，留空即可
        '''
        raise NotImplementedError()
    def dump_login_status(self, fileDir=None):
        '''
        转存当前登陆状态到pkl文件
        fileDir：文件名，后缀必须是pkl
        '''
        raise NotImplementedError()
    def load_login_status(self, fileDir,loginCallback=None, exitCallback=None):
        '''
        使用pkl文件登陆
        fileDir：pkl文件路径
        loginCallback：传入登陆成功时回调的函数，无传参
        exitCallback：传入退出登陆时的回调函数，无传参
        '''
        raise NotImplementedError()
    def auto_login(self, hotReload=False, statusStorageDir='linuxchat.pkl',
            enableCmdQR=False, picDir=None, qrCallback=None,
            loginCallback=None, exitCallback=None,overtime = None):
        '''
        自动生成二维码，并监测扫码状态，扫码成功后自动初始化，建议使用该方式登陆
        hotReload：热启动，退出程序后，短时间内重启可以不需要扫码
        statusStorageDir：转存登陆状态到pkl文件的路劲
        enableCmdQR:二维码显示方式，False:显示图片，True:命令行显示二维码
        picDir：二维码下载保存地址
        qrCallback:传入生成二维码时回调的函数,回调时自动传入（uuid，"stat",及二维码的二进制数据）三个数据
        loginCallback：传入登陆成功时回调的函数，无传参
        exitCallback：传入退出登陆时的回调函数，无传参
        overtime：扫码限制时长，单位（秒）
        '''
        raise NotImplementedError()
    def configured_reply(self):
        '''
        自动回复
        需要在登陆之后调用，单独开启一个线程来运行，该方法主要是维持程序运行而已
        '''
        raise NotImplementedError()
    def msg_register(self, msgType,isFriendChat=False, isGroupChat=False, isMpChat=False):
        '''
        消息注册
        msg：注册消息的类型，list,[TEXT, MAP, CARD, NOTE, SHARING, PICTURE,RECORDING, VOICE, ATTACHMENT, VIDEO, FRIENDS, SYSTEM]
        isFriendChat：是否注册私聊消息
        isGroupChat：是否注册群聊消息
        isGroupChat：是否注册公众号消息
        使用消息注册器时，只有注册过的消息才会接收
        @linuxchat.msg_register(linuxchat.content.TEXT,isFriendChat=True,isGroupChat=True)
        def text_reply(msg):
            linuxchat.set_pinned(msg['ToUserName'],isPinned=True)
                return msg.text
        '''
        raise NotImplementedError()
    def run(self, debug=True, blockThread=True):
        '''
        登陆成功后保持运行
        debug:是否开启debug模式
        blockThread：是否开启多线程
        '''
        raise NotImplementedError()
    def search_friends(self, name=None, userName=None, remarkName=None, nickName=None,wechatAccount=None):
        return self.storageClass.search_friends(name, userName, remarkName,nickName, wechatAccount)
        #  查找本地联系人
        #  name:昵称，备注名或者id其中一个
        #  userName：微信id
        #  remarkName：备注名
        #  nickName：昵称
        #  wechatAccount：微信账号
    def search_chatrooms(self, name=None, userName=None):
        return self.storageClass.search_chatrooms(name, userName)
        #  查找本地群信息
        #  name:昵称，备注名或者id其中一个
        #  userName：微信id
    def search_mps(self, name=None, userName=None):
        return self.storageClass.search_mps(name, userName)
        #  查找本地群信息
        #  name:昵称，备注名或者id其中一个
        #  userName：微信id
load_components(Core)
