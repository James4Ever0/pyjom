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


# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=stow&duration=1
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=stow&duration=2
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=stow&duration=3
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=stow&duration=4


# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&order=stow&duration=4&tids=1

# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&order=stow&duration=4&tids=24


# https://search.bilibili.com/article?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24&order=attention
# https://search.bilibili.com/article?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24&order=scores


# https://search.bilibili.com/live?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24
# https://search.bilibili.com/live?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24&search_type=live_user
# https://search.bilibili.com/live?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24&search_type=live_room


class bilibiliSearchParams:
    class _path:
        综合 = "all"
        视频 = "video" # for now you only search for video, recommend it to qq. remember do not use message post by yourself. or maybe you can make a switch for that?
        番剧 = "bangumi"
        影视 = "pgc"
        直播 = "live"
        专栏 = "article"
        话题 = "topic"
        用户 = "upuser"

    class all:
        class order:
            综合排序 = None
            最多点击 = "click"
            最新发布 = "pubdate"
            最多弹幕 = "dm"
            最多收藏 = "stow"

        class duration:
            全部时长 = None
            _10分钟以下 = 1
            _10_30分钟 = 2
            _30_60分钟 = 3
            _60分钟以上 = 4

        class tids:
            全部分区 = None
            ########################

            class 番剧:
                tid = 13
                连载动画 = 33
                完结动画 = 32
                资讯 = 51
                官方延伸 = 152

            class 国创:
                tid = 167
                国产动画 = 153
                国产原创相关 = 168
                布袋戏 = 169
                动态漫·广播剧 = 195
                资讯 = 170

            class 动画:
                tid = 1
                MAD_AMV = 24
                MMD_3D = 25
                短片·手书·配音 = 47
                手办·模玩 = 210
                特摄 = 86
                综合 = 27

            class 游戏:
                tid = 4
                单机游戏 = 17
                电子竞技 = 171
                手机游戏 = 172
                网络游戏 = 65
                桌游棋牌 = 173
                GMV = 121
                音游 = 136
                Mugen = 19

            class 鬼畜:
                tid = 119
                鬼畜调教 = 22
                音MAD = 26
                人力VOCALOID = 126
                鬼畜剧场 = 216
                教程演示 = 127

            class 音乐:
                tid = 3
                原创音乐 = 28
                翻唱 = 31
                演奏 = 59
                VOCALOID·UTAU = 30
                音乐现场 = 29
                MV = 193
                乐评盘点 = 243
                音乐教学 = 244
                音乐综合 = 130

            class 舞蹈:
                tid = 129
                宅舞 = 20
                街舞 = 198
                明星舞蹈 = 199
                中国舞 = 200
                舞蹈综合 = 154
                舞蹈教程 = 156

            class 影视:
                tid = 181
                影视杂谈 = 182
                影视剪辑 = 183
                小剧场 = 85
                预告·资讯 = 184

            class 娱乐:
                tid = 5
                综艺 = 71
                娱乐杂谈 = 241
                粉丝创作 = 242
                明星综合 = 137

            class 知识:
                tid = 36
                科学科普 = 201
                社科·法律·心理 = 124
                人文历史 = 228
                财经商业 = 207
                校园学习 = 208
                职业职场 = 209
                设计·创意 = 229
                野生技能协会 = 122

            class 科技:
                tid = 188
                数码 = 95
                软件应用 = 230
                计算机技术 = 231
                科工机械 = 232

            class 资讯:
                tid = 202
                热点 = 203
                环球 = 204
                社会 = 205
                综合 = 206

            class 美食:
                tid = 211
                美食制作 = 76
                美食侦探 = 212
                美食测评 = 213
                田园美食 = 214
                美食记录 = 215

            class 生活:
                tid = 160
                搞笑 = 138
                出行 = 250
                三农 = 251
                家居房产 = 239
                手工 = 161
                绘画 = 162
                日常 = 21

            class 汽车:
                tid = 223
                赛车 = 245
                改装玩车 = 246
                新能源车 = 246
                房车 = 248
                摩托车 = 240
                购车攻略 = 227
                汽车生活 = 176

            class 时尚:
                tid = 155
                美妆护肤 = 157
                仿妆cos = 252
                穿搭 = 158
                时尚潮流 = 159

            class 运动:
                tid = 234
                篮球 = 235
                足球 = 249
                健身 = 164
                竞技体育 = 236
                运动文化 = 237
                运动综合 = 238

            class 动物圈:
                tid = 217
                喵星人 = 218
                汪星人 = 219
                大熊猫 = 220
                野生动物 = 221
                爬宠 = 222
                动物综合 = 75

            ########################

    video = all

    class article:
        class order:
            综合排序 = None
            最多点击 = "click"
            最新发布 = "pubdate"
            最多喜欢 = "attention"
            最多评论 = "scores"

    class live:
        class search_type:
            全部 = None
            主播 = "live_user"
            直播间 = "live_room"

    class upuser:
        class order:
            默认排序 = None
            粉丝数由高到低 = "fans"
            Lv等级由高到低 = "level"

        class order_sort:
            正序 = None
            倒序 = 1


# https://search.bilibili.com/upuser?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24&order=fans
# https://search.bilibili.com/upuser?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24&order=fans&order_sort=1
# https://search.bilibili.com/upuser?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&duration=4&tids=24&order=level

# bilibiliSearchParams.order.最多弹幕
print(bilibiliSearchParams.video.tids)
