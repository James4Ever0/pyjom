# you will have a better name for other toolboxs.

# for now, the musictoolbox is responsible for music/lyric retrieval/download, track separation, bpm, music recognition

# pitch shift, speedup/slowdown is for audiotoolbox

# voice change/synthesis is for voicetoolbox.

# diffusion based painter, ai colorization, video editing is for artworktoolbox. maybe the naming is not right/necessary.

# check AmadeusCore, /root/Desktop/works/pyjom/tests/music_recognization/AmadeusCore/src/components/app/models/

import audioowl
import math
from pyjom.commons import *
from pyjom.lyrictoolbox import read_lrc, getLyricNearbyBpmCandidates
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


# musictoolbox
def getMusicCutSpansCandidates(
    music, lyric_path, maxtime, mintime, mbeat_time_tolerance=0.8
):
    beats, bpm = audioOwlAnalysis(music["filepath"])
    if (
        lyric_path is not None
        and type(lyric_path) == str
        and os.path.exists(lyric_path)
    ):
        lyric = read_lrc(lyric_path)
        # print(lyric)
        # breakpoint()
        lyric_times = [x["time"] for x in lyric]
        lyric_times.sort()
    else:
        lyric_times = []
    new_lyric_times = []
    last_time = 0
    for mtime in lyric_times:
        if mtime - last_time > mintime:
            new_lyric_times.append(mtime)
            last_time = mtime
    lyric_times = new_lyric_times
    beat_duration = 60 / bpm

    # this is static, not dynamic.
    # we can make this 'standard bpm spans' into a generator instead.
    standard_bpm_spans = [
        x * beat_duration
        for x in range(0, math.ceil(maxtime / beat_duration) + 1)
        if x * beat_duration >= mintime * mbeat_time_tolerance
        and x * beat_duration <= maxtime / mbeat_time_tolerance
    ]

    (
        sorted_lyrics_nearby_bpm_candidates,
        sorted_remained_bpm_candidates,
    ) = getLyricNearbyBpmCandidates(lyric_times, beats)

    candidates = sorted_lyrics_nearby_bpm_candidates + sorted_remained_bpm_candidates
    return candidates, standard_bpm_spans

# musictoolbox
def getMusicCutSpans(
    music,
    music_duration,
    lyric_path,
    maxtime,
    mintime,
    mbeat_time_tolerance=0.8,
    gaussian=False,
    gaussian_args={"std": 1.6674874515595588, "mean": 2.839698412698412},
):
    assert mintime > 0
    assert maxtime > mintime
    candidates, standard_bpm_spans = getMusicCutSpansCandidates(
        music,
        lyric_path,
        maxtime,
        mintime,
        mbeat_time_tolerance=mbeat_time_tolerance,
    )
    assert len(standard_bpm_spans) >= 1
    if gaussian:
        std, mean = gaussian_args["std"], gaussian_args["mean"]
        scale, loc = std, mean
        myclip_a, myclip_b = mintime, maxtime
        from scipy.stats import truncnorm

        a, b = (myclip_a - loc) / scale, (myclip_b - loc) / scale
        randVar = truncnorm(a, b)
        randomFunction = lambda: randVar.rvs(1)[0] * scale + loc

    # now we engage with the cue points.

    demanded_cut_points = [0]
    # startingPoint=0
    remaining_time = music_duration
    counter = 0
    oldCandidateLength = None
    while True:
        if gaussian:
            standard_bpm_span_min_selected = randomFunction()
            doubleRate = max(min(2, maxtime / standard_bpm_span_min_selected), 1)
        elif len(standard_bpm_spans) == 1:
            standard_bpm_span_min_selected = standard_bpm_spans[0]
            doubleRate = 1.2
        else:
            standard_bpm_span_min_selected = random.choice(standard_bpm_spans[:-1])
            doubleRate = max(1, min(2, maxtime / standard_bpm_span_min_selected))
        if counter > 10000:  # some dangerous deadloop.
            breakpoint()
            print("LOOPCOUNT", counter)
            print(len(demanded_cut_points), remaining_time, standard_bpm_spans[0])
        counter += 1
        startingPoint = demanded_cut_points[-1]
        # try:
        selected_candidates = [
            x for x in candidates if x > startingPoint
        ]  # unsupported comparation between 'float' and 'list'?
        # except:
        #     import traceback
        #     traceback.print_exc()
        #     breakpoint()
        newCandidateLength = len(selected_candidates)
        if newCandidateLength == 0:
            # nothing left.
            break
        if oldCandidateLength is None:
            oldCandidateLength = newCandidateLength
        else:
            if (
                oldCandidateLength == newCandidateLength
            ):  # force append those points without progress
                # demanded_cut_points.append(selected_candidates) # this is wrong.
                demanded_cut_points.append(selected_candidates[0])
                # no need to update the oldCandidateLength since it is the same as the new
                continue
            else:
                oldCandidateLength = newCandidateLength

        for elem in selected_candidates:
            timespan_length = elem - startingPoint
            if inRange(
                timespan_length,
                (
                    standard_bpm_span_min_selected,
                    standard_bpm_span_min_selected * doubleRate,
                ),
                tolerance=mbeat_time_tolerance,
            ):
                # select this element.
                demanded_cut_points.append(elem)
                break
        remaining_time = music_duration - demanded_cut_points[-1]
        if remaining_time < standard_bpm_span_min_selected:
            break
    demanded_cut_points = list(set(demanded_cut_points))
    demanded_cut_points.sort()
    for elem in demanded_cut_points.copy()[::-1]:
        if music_duration - elem < standard_bpm_spans[0]:
            demanded_cut_points.remove(elem)
    demanded_cut_points.append(music_duration)
    demanded_cut_spans = list(zip(demanded_cut_points[0:-1], demanded_cut_points[1:]))
    # somehow it was wrong.
    # print("DEMANDED MUSIC CUT SPANS GENERATED")
    # breakpoint()
    return demanded_cut_spans, standard_bpm_spans


# musictoolbox
# fix long loading time.
@redisLRUCache()
def getMusicInfoParsed(config, mintime=2, maxtime=7.8):  # these are defaults.
    music = config["music"]
    gaussian = config.get(
        "gaussian", True
    )  # this is different. default to use gaussian instead.

    # check if music is corrupted?
    font = config.get("font", None)
    policy = config.get("policy", {})
    policy_names = [x for x in policy.keys()]
    # get music duration here.
    music_metadata = get_media_info(music["filepath"])
    music_duration = music_metadata["duration"]
    maxtime = config.get("maxtime", maxtime)
    mintime = config.get("mintime", mintime)
    lyric_path = music.get("lyric_path", None)
    if type(lyric_path) == str:
        if not os.path.exists(lyric_path):
            lyric_path = None
    elif lyric_path is not None:
        lyric_path = None
    demanded_cut_spans, standard_bpm_spans = getMusicCutSpans(
        music, music_duration, lyric_path, maxtime, mintime, gaussian=gaussian
    )
    return (
        music,
        font,
        policy,
        policy_names,
        music_metadata,
        music_duration,
        maxtime,
        mintime,
        lyric_path,
        demanded_cut_spans,
        standard_bpm_spans,
    )

# for midomi we need to chop music apart.
# for shazam, nope.
# shazamio needs event loop. be careful!
from typing import Literal
def recognizeMusicFromFileSongrec(filepath):
def recognizeMusicFromFileShazamIO(filepath):
def recognizeMusicFromFileMidomi(filepath):
def recognizeMusicFromFile(filepath, backend:Literal['songrec','shazamio','midomi']='midomi'):
    # you can try all methods. but if all three methods fails, you know what to do. what indicates the recognizer has failed?
    # you can try something erotic.