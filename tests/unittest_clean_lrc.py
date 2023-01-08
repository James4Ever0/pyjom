lyric_string = """[00:00.000] 作词 : 苏喜多/挡风玻璃\n[00:01.000] 作曲 : 苏喜多/陈恒冠\n[00:02.000] 编曲 : 陈恒冠/陈恒家\n[00:31.154]你戴上帽子遮住眼睛 轻轻地绕着我 总洋溢着暖\n[00:44.404]我…我只能唱\n[00:54.902]你像气泡水直接淘气 爱和星星眨眼睛 轻易抓住我\n[01:07.903]我…我只能唱\n[01:16.651]有一个岛屿 在北极冰川\n[01:23.403]那儿没有花朵 也没有失落\n[01:30.159]在那个岛屿 洒满了繁星\n[01:36.904]拥有我和你 再没有失落\n[02:15.903]你邀请流浪期待欢喜 惹我专心好奇 我看见了光\n[02:29.153]我…我只能唱\n[02:39.403]难免坏天气闪电暴雨 练就肩膀和勇气 只为你拥抱我\n[02:54.156]我…我只能唱\n[03:01.659]有一个岛屿 在北极冰川\n[03:08.154]那儿没有花朵 也没有失落\n[03:14.906]在那个岛屿 洒满了繁星\n[03:21.651]拥有我和你 再没有失落\n[03:28.656]有一个岛屿 在北极冰川\n[03:35.152]
那儿没有花朵 也没有失落\n[03:41.904]在那个岛屿 洒满了繁星\n[03:48.661]拥有我和你 再没有失落\n[03:59.159]有一个岛屿 在北极冰川\n[04:05.654]那儿没有花朵 也没有失落\n[04:12.659]在那个岛屿 洒满了繁星\n[04:19.152]拥有我和你 再没有失落\n[04:26.405]有一个岛屿
在北极冰川\n[04:33.658]那儿没有花朵 也没有失落…\n[04:40.401]吉他：陈恒家\n[04:42.654]钢琴：陈恒冠\n[04:47.407]混音：陈恒家\n[04:49.907]母带：陈恒家\n[04:53.907]监制：1991与她\n"""

# assume song duration here!
song_duration = 5 * 60

import pylrc

# you'd better inspect the thing. what is really special about the lyric, which can never appear?

min_lines_of_lyrics = 5
min_total_lines_of_lyrics = 10
potential_forbidden_chars = ["[", "]", "【", "】", "「", "」", "《", "》", "/", "(", ")"]
core_forbidden_chars = [":", "：", "@"]


def checkLyricText(text, core_only=False):
    if core_only:
        forbidden_chars = core_forbidden_chars
    else:
        forbidden_chars = core_forbidden_chars + potential_forbidden_chars
    return not any([char in text for char in forbidden_chars])


# also get the total time covered by lyric.
# the time must be long enough, compared to the total time of the song.
lrc_parsed = pylrc.parse(lyric_string)
lrc_parsed_list = [line for line in lrc_parsed]
lrc_parsed_list.sort(key=lambda line: line.time)
begin = False
# end = False
line_counter = 0
new_lines = []
# lrc_parsed: pylrc.classes.Lyrics
flags = []
for line in lrc_parsed_list:
    # print(line)
    text = line.text.strip()
    startTime = line.time
    if not begin:
        flag = checkLyricText(text, core_only=False)
        if not flag:
            begin = True
    else:
        flag = checkLyricText(text, core_only=True)
        if flag:
            begin = False
    flags.append(flag)
    # breakpoint()

# select consecutive spans.
from test_commons import *
from pyjom.mathlib import extract_span

int_flags = [int(flag) for flag in flags]

mySpans = extract_span(int_flags, target=1)
print(mySpans)  # this will work.
# this span is for the range function. no need to add one to the end.

total_length = 0

new_lyric_list = []
for mstart, mend in mySpans:
    length = mend - mstart
    total_length += length
    if length >= min_lines_of_lyrics:
        # process these lines.
        for index in range(mstart, mend):
            line_start_time = lrc_parsed_list[index].time
            line_text = lrc_parsed_list[index].text
            if line_start_time <= song_duration:
                line_end_time = song_duration
                if index + 1 < len(lrc_parsed_list):
                    line_end_time = lrc_parsed_list[index + 1].time
                    if line_end_time > song_duration:
                        line_end_time = song_duration
                new_lyric_list.append((line_text, line_start_time))
                if index == mend - 1:
                    # append one more thing.
                    new_lyric_list.append(("", line_end_time))
            else:
                continue
# for elem in new_lyric_list:
#     print(elem)
# exit()

if total_length >= min_total_lines_of_lyrics:
    print("LYRIC ACCEPTED.")
    new_lrc = pylrc.classes.Lyrics()
    for text, myTime in new_lyric_list:
        timecode_min, timecode_sec = divmod(myTime, 60)
        timecode = "[{:d}:{:.3f}]".format(int(timecode_min), timecode_sec)
        myLine = pylrc.classes.LyricLine(timecode, text)
        new_lrc.append(myLine)
    new_lrc_string = new_lrc.toLRC()
    print(new_lrc_string)
