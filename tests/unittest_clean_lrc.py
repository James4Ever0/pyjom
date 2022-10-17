lyric_string = """[00:00.000] 作词 : 苏喜多/挡风玻璃\n[00:01.000] 作曲 : 苏喜多/陈恒冠\n[00:02.000] 编曲 : 陈恒冠/陈恒家\n[00:31.154]你戴上帽子遮住眼睛 轻轻地绕着我 总洋溢着暖\n[00:44.404]我…我只能唱\n[00:54.902]你像气泡水直接淘气 爱和星星眨眼睛 轻易抓住我\n[01:07.903]我…我只能唱\n[01:16.651]有一个岛屿 在北极冰川\n[01:23.403]那儿没有花朵 也没有失落\n[01:30.159]在那个岛屿 洒满了繁星\n[01:36.904]拥有我和你 再没有失落\n[02:15.903]你邀请流浪期待欢喜 惹我专心好奇 我看见了光\n[02:29.153]我…我只能唱\n[02:39.403]难免坏天气闪电暴雨 练就肩膀和勇气 只为你拥抱我\n[02:54.156]我…我只能唱\n[03:01.659]有一个岛屿 在北极冰川\n[03:08.154]那儿没有花朵 也没有失落\n[03:14.906]在那个岛屿 洒满了繁星\n[03:21.651]拥有我和你 再没有失落\n[03:28.656]有一个岛屿 在北极冰川\n[03:35.152]
那儿没有花朵 也没有失落\n[03:41.904]在那个岛屿 洒满了繁星\n[03:48.661]拥有我和你 再没有失落\n[03:59.159]有一个岛屿 在北极冰川\n[04:05.654]那儿没有花朵 也没有失落\n[04:12.659]在那个岛屿 洒满了繁星\n[04:19.152]拥有我和你 再没有失落\n[04:26.405]有一个岛屿
在北极冰川\n[04:33.658]那儿没有花朵 也没有失落…\n[04:40.401]吉他：陈恒家\n[04:42.654]钢琴：陈恒冠\n[04:47.407]混音：陈恒家\n[04:49.907]母带：陈恒家\n[04:53.907]监制：1991与她\n"""

import pylrc
# you'd better inspect the thing. what is really special about the lyric, which can never appear?

min_lines_of_lyrics = 10
potential_forbidden_chars = ["[","]","【","】","「","」","《","》","/","(",")"]
forbidden_chars = [":","：", "@"]+potential_forbidden_chars
# also get the total time covered by lyric.
# the time must be long enough, compared to the total time of the song.
lrc_parsed = pylrc.parse(lyric_string)
begin = False
end = False
line_counter = 0
new_lines = []
# lrc_parsed: pylrc.classes.Lyrics
for line in lrc_parsed:
    # print(line)
    text = line.text.strip()
    startTime = line.time
    # breakpoint()