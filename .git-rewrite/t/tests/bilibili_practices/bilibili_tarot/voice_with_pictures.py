import os
from test_common import *

def split_sentences(sent):
    spliters = "\n，。、"
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
    with open("temp.txt", "w+",encoding="utf-8") as f:
        f.write(sent)
    os.system("cat temp.txt | paddlespeech tts --output {}".format(output))

from pydub import AudioSegment
from functional_gen_typo_video_seq import gen_video

def merge_audio(asegs):
    audio_3 = AudioSegment.empty() #shit
    for seg in asegs:
        try:
            audio_3 = audio_3.append(seg,crossfade=100) # also shit.
        except:
            audio_3 = audio_3.append(seg,crossfade=0) # also shit.
    return audio_3
    # audio_3.export("audio_3.wav", format="wav")

if __name__ == "__main__":
    sents = split_sentences(demo_text)
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
        seg = AudioSegment.from_wav(aname)
        duration = seg.duration_seconds
        voice_clips.append(seg)
        # get the duration you fuck.
        # breakpoint()
        lsent = len(sent)
        current_indexs = list(range(index,index+lsent))
        index += lsent
        # you can generate video for it.
        vname = "{}/{}.mp4".format(video_dir,i)
        gen_video(vname,current_indexs,duration)
        video_names.append(vname)
    # and finally?
    final_video = "{}/final_video.mp4".format(video_dir)
    final_audio = "{}/final_audio.wav".format(voice_dir)
    audio_merged = merge_audio(voice_clips)
    bgm_path = "/root/Desktop/works/bilibili_tarot/some_bgm.mp3"
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
    os.system("ffmpeg -i {} -i {} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {}".format(final_video,final_audio,final_video2))
    