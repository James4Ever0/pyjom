import os
from test_common import *
import shutil

def split_sentences(sent):
    spliters = "\n，。、？： "
    cursent = ""
    results = []
    for elem in sent:
        cursent += elem
        if elem in spliters:
            results.append(cursent)
            cursent = ""
    if len(cursent) > 0:
        results.append(cursent)
    return results

def get_speech(sent,output):
    assert output.endswith(".wav")
    os.system("bash kill_pdspc.sh")
    with open("temp.txt", "w+",encoding="utf-8") as f:
        f.write(sent.replace("\n","")) # important.
    os.system("cat temp.txt | paddlespeech tts --output {}".format(output))

from pydub import AudioSegment
from functional_gen_typo_video_seq import gen_video
# import matplotlib # doing this before importing moviepy editor. or we will fail.
# matplotlib.use("TkAgg")
# from moviepy.editor import VideoFileClip
# cannot mix moviepy with vidpy or we get fucked.
from MediaInfo import MediaInfo

def merge_audio(asegs):
    audio_3 = AudioSegment.empty() #shit
    for seg in asegs:
        try:
            audio_3 = audio_3.append(seg,crossfade=100) # also shit.
        except:
            audio_3 = audio_3.append(seg,crossfade=0) # also shit.
    return audio_3
    # audio_3.export("audio_3.wav", format="wav")

def gen_typography_part2(intro_text, bgm_path,target_video):
    # intro_text = """塔罗牌，由“TAROT”一词音译而来，被称为“大自然的奥秘库”。抽取一张塔罗牌，今天的你会是怎样的呢？"""
    os.system("bash kill_pdspc.sh")
    sents = split_sentences(intro_text)
    # breakpoint()
    voice_dir = "voice"
    video_dir = "video"

    os.system("rm -rf {}".format(voice_dir))
    os.system("rm -rf {}".format(video_dir))
    os.mkdir("{}".format(voice_dir))
    os.mkdir("{}".format(video_dir))
    index = 0
    voice_clips = []
    video_names = []
    for i,sent in enumerate(sents):
        print("READING:",sent)
        aname = "{}/{}.wav".format(voice_dir,i)
        get_speech(sent,aname)
        lsent = len(sent)
        # if no audio then just skip.
        if not os.path.exists(aname):
            index += lsent
            continue
        seg = AudioSegment.from_wav(aname)
        duration = seg.duration_seconds
        voice_clips.append(seg)
        # get the duration you fuck.
        # breakpoint()
        current_indexs = list(range(index,index+lsent))
        # you can generate video for it.
        index += lsent

        vname = "{}/{}.mp4".format(video_dir,i)
        gen_video(vname,current_indexs,duration) # where from?
        video_names.append(vname)
    # and finally?
    final_video = "{}/final_video.mp4".format(video_dir)
    final_audio = "{}/final_audio.wav".format(voice_dir)
    audio_merged = merge_audio(voice_clips)
    # bgm_path = "/root/Desktop/works/bilibili_tarot/some_bgm.mp3"
    bgm = AudioSegment.from_mp3(bgm_path)
    # duration2 = audio_merged.duration_seconds
    # bgm = bgm[:duration2*1000] # really?
    # breakpoint()
    # audio_merged = audio_merged.overlay(audio_merged,bgm,loop=True)  #wtf?
    audio_merged = audio_merged.overlay(bgm,loop=True)
    # audio_merged = audio_merged.normalize()
    # is it needed?
    # shit.
    audio_merged.export(final_audio, format="wav")

    final_video2 = "{}/final_video2.mp4".format(video_dir)

    with open("mylist.txt","w+") as f:
        for n in video_names:
            f.write("file "+n+"\n")
    os.system("ffmpeg -f concat -safe 0 -i mylist.txt -c copy {}".format(final_video))
    # output_length = VideoFileClip(final_video).duration
    output_length = MediaInfo(filename=final_video).getInfo()["videoDuration"]
    output_length = float(output_length)
    input_length = AudioSegment.from_wav(final_audio).duration_seconds
    tempo = input_length/output_length
    t_a,t_b = tempo.as_integer_ratio()
    os.system('ffmpeg -i {} -i {} -c:v copy -c:a aac -filter:a "atempo={}/{}" -map 0:v:0 -map 1:a:0 {}'.format(final_video,final_audio,t_a,t_b,final_video2))
    shutil.move(final_video2,target_video)


def gen_typography_part3(intro_text, target_video): #slient
    # intro_text = """塔罗牌，由“TAROT”一词音译而来，被称为“大自然的奥秘库”。抽取一张塔罗牌，今天的你会是怎样的呢？"""
    os.system("bash kill_pdspc.sh")
    sents = split_sentences(intro_text)
    # breakpoint()
    voice_dir = "voice"
    video_dir = "video"

    os.system("rm -rf {}".format(voice_dir))
    os.system("rm -rf {}".format(video_dir))
    os.mkdir("{}".format(voice_dir))
    os.mkdir("{}".format(video_dir))
    index = 0
    voice_clips = []
    video_names = []
    for i,sent in enumerate(sents):
        print("READING:",sent)
        aname = "{}/{}.wav".format(voice_dir,i)
        get_speech(sent,aname)
        lsent = len(sent)
        # if no audio then just skip.
        if not os.path.exists(aname):
            index += lsent
            continue
        seg = AudioSegment.from_wav(aname)
        duration = seg.duration_seconds
        voice_clips.append(seg)
        # get the duration you fuck.
        # breakpoint()
        current_indexs = list(range(index,index+lsent))
        # you can generate video for it.
        index += lsent

        vname = "{}/{}.mp4".format(video_dir,i)
        gen_video(vname,current_indexs,duration) # where from?
        video_names.append(vname)
    # and finally?
    final_video = "{}/final_video.mp4".format(video_dir)
    final_audio = "{}/final_audio.wav".format(voice_dir)
    audio_merged = merge_audio(voice_clips)
    # bgm_path = "/root/Desktop/works/bilibili_tarot/some_bgm.mp3"
    # bgm = AudioSegment.from_mp3(bgm_path)
    # duration2 = audio_merged.duration_seconds
    # bgm = bgm[:duration2*1000] # really?
    # breakpoint()
    # audio_merged = audio_merged.overlay(audio_merged,bgm,loop=True)  #wtf?
    # audio_merged = audio_merged.overlay(bgm,loop=True)
    # audio_merged = audio_merged.normalize()
    # is it needed?
    # shit.
    audio_merged.export(final_audio, format="wav")

    final_video2 = "{}/final_video2.mp4".format(video_dir)

    with open("mylist.txt","w+") as f:
        for n in video_names:
            f.write("file "+n+"\n")
    os.system("ffmpeg -f concat -safe 0 -i mylist.txt -c copy {}".format(final_video))
    # output_length = VideoFileClip(final_video).duration
    output_length = MediaInfo(filename=final_video).getInfo()["videoDuration"]
    output_length = float(output_length)
    input_length = AudioSegment.from_wav(final_audio).duration_seconds
    tempo = input_length/output_length
    t_a,t_b = tempo.as_integer_ratio()
    os.system('ffmpeg -i {} -i {} -c:v copy -c:a aac -filter:a "atempo={}/{}" -map 0:v:0 -map 1:a:0 {}'.format(final_video,final_audio,t_a,t_b,final_video2))
    shutil.move(final_video2,target_video)