# find our target video.
# you may find uploaders, keywords, tags, recommended videos, video collections/playlists and filter by analyzers (check if is in the target format)

# how did vscode recommend this shit to me?
# from sklearn.semi_supervised import LabelSpreading

# 其他标签就是和视频主题有关的 属于小分类
tags = {  # select 1 for each.
    "static": [
        ["二次元", "动画", "动漫"],
        [
            "综合",
            "多素材",
            "动漫杂谈",
            "动画嘉年华",
            "综漫",
        ],
    ],
    "optional": [  # select one or not select any.
        ["动漫推荐", "补番推荐", "动漫盘点", "盘点排行", "盘点推荐", "新番推荐"],
        ["名场", "名场面", "万恶之源"],
    ],
    # these are seeds. you may have different tags added along the way.
}
