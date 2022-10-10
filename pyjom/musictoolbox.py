# you will have a better name for other toolboxs.

# for now, the musictoolbox is responsible for music/lyric retrieval/download, track separation, bpm, music recognition

# pitch shift, speedup/slowdown is for audiotoolbox

# voice change/synthesis is for voicetoolbox.

# diffusion based painter, ai colorization, video editing is for artworktoolbox. maybe the naming is not right/necessary.


# musictoolbox
def audioOwlAnalysis(myMusic):
    # get sample rate
    # info = MediaInfo(filename = myMusic)
    # info = info.getInfo()
    info = get_media_info(myMusic)
    audioSampleRate = info["audioSamplingRate"]
    audioSampleRate = int(audioSampleRate)

    waveform = audioowl.get_waveform(myMusic, sr=audioSampleRate)
    data = audioowl.analyze_file(myMusic, sr=audioSampleRate)  # how fucking long?

    a, b, c, d = [
        data[k] for k in ["beat_samples", "duration", "sample_rate", "tempo_float"]
    ]
    bpm = data["tempo_float"]
    # single_bpm_time = 60/d

    beat_times = [x / c for x in a]
    return beat_times, bpm

