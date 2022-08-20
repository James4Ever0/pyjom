# lrc2ass_py3
A simple Python 3.x script is used for changing your LRC file into ASS subtitle with karaoke effect tags

一个用于将LRC歌词文件转换为ASS字幕文件的简单Python脚本。

The first full python script written by myself.

我自己编写的第一个完整的Python脚本

Copyright(c) 2020 yyfll (MIT)

# WON'T UPDATE IN THE FUTURE

# Dependent
* chardet (lrc2ass_py3 >= 1.0.0c)

# Update
## 1.0.0c
* Support chardet character encoding detector.
* A few improvements
## 1.0.0b
* Support LRC offset tag.
* Default LRC offset can be set.
* Simplify program.

# English Readme
Poor English.
## What can lrc2ass_py3 do?
* Change your LRC script to ASS script.
* Very easy to use.
* Support Multi timing tags in a single line.
* Support auto choose end timing if can't find timing in the end of the line.
* Support LRC offset tag.

## What will cause error?
* A lrc file in wrong text coding (such as use utf-8 read gbk file.)
* A lrc line without the timing tag in the line ahead. (haven't tested)

## WARNING
* Only CHINESE are supported.
> All the information show in console and the annotations in python script are written in CHINESE,
>
> It doesn't mean lrc2ass_py3 can't work on your LRC in English.
>
> So it doesn't have any influence on output a correct ASS script if you use English or any other language.

# 简体中文 Readme
## lrc2ass_py3可以做什么？
* 将你的LRC歌词文件转换为ASS字幕文件
* 使用起来非常简单
* 支持一个歌词行多个时间标签（即卡拉OK效果）
* 支持在找不到歌词行的结束时间时，自动选择结束时间
* 支持时间偏移标签（offset）

## 有什么可能会导致错误的？
* 读取了非指定文本编码的LRC歌词文件（比如像用utf-8编码读取gbk编码的文件）
* 歌词行开头没有指定起始时间的时间标签（这还没有经过测试）

## 警告
* 只支持中文
> 所有的控制台输出及文件内注释都是用中文写的
>
> 这并不意味着lrc2ass_py3不能处理非中文的LRC文件
>
> 所以这并不会对输出一个正确ASS字幕文件产生任何影响

# To do
* Full English supported
* Full Chinese annotation
* File list input
* Reusable
* Endless debugging
