from pyjom.commons import *

# from pyjom.modules.contentProducing.videoProcessing import *
# it is like a game designed by you, played by everyone.

# maybe you need to render this into ffmpeg arguments or mltframework arguments.
import random
import pylrc
import math

import audioowl
from MediaInfo import MediaInfo


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


def getLyricNearbyBpmCandidates(lyric_times, beats):
    nearbys, remains = [], []
    mbeats = beats.copy()
    mbeats = list(set(mbeats))
    mbeats.sort()

    for ltime in lyric_times:
        mbeats.sort(key=lambda x: abs(x - ltime))
        nearby = mbeats[:2].copy()
        nearbys += nearby
        for elem in nearby:
            mbeats.remove(elem)
    remains = mbeats
    return nearbys, remains


def read_lrc(lrc_path):
    assert lrc_path.endswith(".lrc")
    with open(lrc_path, "r") as f:
        lrc_string = f.read()
        subs = pylrc.parse(lrc_string)
        sublist = []
        for sub in subs:
            time_in_secs = sub.time
            content = sub.text
            sublist.append({"time": time_in_secs, "content": content})
            # another square bracket that could kill me.
        return sublist


def getMusicCutSpans(
    music, music_duration, lyric_path, maxtime, mintime, mbeat_time_tolerance=0.8
):
    beats, bpm = audioOwlAnalysis(music["filepath"])
    lyric = read_lrc(lyric_path)
    # print(lyric)
    # breakpoint()
    lyric_times = [x["time"] for x in lyric]
    beat_duration = 60 / bpm
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

    # now we engage with the cue points.

    demanded_cut_points = [0]
    # startingPoint=0
    remaining_time = music_duration
    counter = 0
    oldCandidateLength = None
    while True:
        if counter > 10000: # some dangerous deadloop.
            breakpoint()
            print("LOOPCOUNT",counter)
            print(len(demanded_cut_points), remaining_time,standard_bpm_spans[0])
        counter += 1
        startingPoint = demanded_cut_points[-1]
        try:
            selected_candidates = [x for x in candidates if x > startingPoint]# unsupported comparation between 'float' and 'list'?
        except:
            import traceback
            traceback.print_exc()
            breakpoint()
        newCandidateLength = len(selected_candidates)
        if newCandidateLength == 0:
            # nothing left.
            break
        if oldCandidateLength is None:
            oldCandidateLength = newCandidateLength
        else:
            if oldCandidateLength == newCandidateLength: # force append those points without progress
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
                (standard_bpm_spans[0], standard_bpm_spans[-1]),
                tolerance=mbeat_time_tolerance,
            ):
                # select this element.
                demanded_cut_points.append(elem)
                break
        remaining_time = music_duration - demanded_cut_points[-1]
        if remaining_time < standard_bpm_spans[0]:
            break
    demanded_cut_points = list(set(demanded_cut_points))
    demanded_cut_points.sort()
    for elem in demanded_cut_points.copy()[::-1]:
        if music_duration - elem < standard_bpm_spans[0]:
            demanded_cut_points.remove(elem)
    demanded_cut_points.append(music_duration)
    demanded_cut_spans = list(zip(demanded_cut_points[0:-1], demanded_cut_points[1:0]))
    print("DEMANDED MUSIC CUT SPANS GENERATED")
    breakpoint()
    return demanded_cut_spans, standard_bpm_spans


def getFileCuts(
    filtered_info, meta_info, standard_bpm_spans, policy_names, mbeat_time_tolerance=0.8
):
    total_cuts_dict = {}
    for (
        file_path,
        cuts,
    ) in (
        filtered_info
    ):  # sample these cuts, shuffle these samples. order these samples.
        file_cuts = []  # only for this single file.
        modifiers = {}
        if cuts == {}:  # no cuts specified. require metadata.
            # what is this synthed cuts? do you want to use some framedelta/audio volume based cutting methods, or not? or some scenedetect cuts?
            # we use scenedetect cuts here. maybe later you would sort these cuts with framedelta/audio based methods.
            # or you implement this in the reviewer. none of the freaking business.
            # synthed_cuts = scenedetect_cut(file_path)
            # we use evenly spaced cuts.
            duration = meta_info["duration"]
            if duration < standard_bpm_spans[0]:
                synthed_cuts = [(0, duration)]
            else:
                synthed_cuts = []
                start_time = 0
                while True:
                    remained_time = duration - start_time
                    mcandidates = [x for x in standard_bpm_spans if x < remained_time]
                    if len(mcandidates) > 0:
                        mc = random.choice(mcandidates)
                        synthed_cuts.append((start_time, mc))
                        start_time += mc
                    else:
                        break
            file_cuts = synthed_cuts
        else:  # get cuts from those keys.
            for key, content in cuts.items():
                # if key == "labels": continue # this cannot happen!
                if key == "yolov5":
                    for object_name, object_cuts in content.items():
                        file_cuts += [
                            x
                            for x in object_cuts
                            if (x[1] - x[0])
                            >= standard_bpm_spans[0] * mbeat_time_tolerance
                        ]  # we may choose only non-overlapping cuts.
                elif (
                    key == "framedifference_talib_detector"
                ):  # this is a modifier. modify all things in avaliable cuts. but it cannot work alone. is it?
                    modifiers.update({"framedifference_talib_detector": content})
        # rearrange all things.
        # after this is done, add this to the end.
        if "non_overlapping" in policy_names:
            file_cuts.sort()
            new_file_cuts = [file_cuts[0]]
            for cut in file_cuts[1:]:  # deterministic
                if cut[0] >= new_file_cuts[-1][1]:
                    new_file_cuts.append(cut)
            file_cuts = new_file_cuts
        compiled_file_cuts = []
        for cut in file_cuts:
            new_cut = {"span": cut, "modifiers": {}}
            for key, content in modifiers.items():
                if (
                    key == "framedifference_talib_detector"
                ):  # get the biggest span. best contain this range. no random selection.
                    framework_candidates = []
                    for framework2 in content:
                        coords = framework2["coords"]
                        f_timespan = framework2["timespan"]
                        mOverlapRange = overlapRange(cut, f_timespan)
                        if mOverlapRange:
                            framework_candidates.append((framework2, mOverlapRange))
                    framework_candidates.sort(lambda x: -(x[1][1] - x[1][0]))
                    if len(framework_candidates) > 0:
                        framework_candidate = framework_candidates[0]
                        modifiers.update(framework_candidate)
                        # add that modifier.
            compiled_file_cuts.append(new_cut)
        total_cuts_dict.update({file_path: compiled_file_cuts.copy()})
    return total_cuts_dict


def getRenderList(total_cuts, demanded_cut_spans):
    file_access_list = [x for x in total_cuts.keys()]
    FAL_generator = infiniteShuffle(
        file_access_list
    )  # infinite generator! may cause serious problems.
    TC_generators = {key: infiniteShuffle(total_cuts[key]) for key in total_cuts.keys()}
    render_list = []
    for span in demanded_cut_spans:
        start, end = span
        span_length = end - start
        for filename in FAL_generator:
            file_cuts = TC_generators[filename]
            # random.shuffle(file_cuts)
            selected_cut = None
            for cut in file_cuts:
                cut_span = cut["span"]
                cut_duration = cut_span[1] - cut_span[0]
                if inRange(
                    cut_duration, [span_length, span_length * 1.5], tolerance=0.8
                ):
                    selected_cut = cut
                    break
            if not selected_cut is None:
                # append the data right here.
                render_list.append({"span": span, "cut": cut, "source": filename})
                break
    return render_list


def petsWithMusicProducer(filtered_info, meta_info, config={}):
    # what is this config? how the fuck we can arrange it?
    # config = {"music":{"filepath":"","lyric_path":""},"font":{"filepath":"","fontsize":30}, "policy":{"some_policy_name":{}},"meta":{"maxtime":3, "mintime":1}}
    # how to auto-warp the AAS subtitle?
    # do you fill timegap with a loop?
    total_cuts = {}
    music = config["music"]
    font = config["font"]
    policy = config["policy"]
    policy_names = [x for x in policy.keys()]
    # bpm = music["bpm"]

    # what about watermarks? pass them within numpy arrays and
    # sure we have some ocr filters. but how to apply them?
    # what about those without any cuts? use them in even slices?
    # usually we switch scene in sync with lyric change. so what is the popular per sentence duration in lyrics?
    # get music duration here.
    music_metadata = get_media_info(music["filepath"])
    music_duration = music_metadata["duration"]

    maxtime = config["maxtime"]
    mintime = config["mintime"]

    lyric_path = music["lyric_path"]

    demanded_cut_spans, standard_bpm_spans = getMusicCutSpans(
        music, music_duration, lyric_path, maxtime, mintime
    )
    # demanded_cut_spans is empty!
    # total_cuts
    total_cuts = getFileCuts(filtered_info, meta_info, standard_bpm_spans, policy_names)

    # now generate the freaking video.
    # if "one_clip_per_file" in policy_names:
    #     used_files = [] # may raise exception.
    # total_cuts {} and demanded_cut_spans [] are both empty
    render_list = getRenderList(total_cuts, demanded_cut_spans)
    print(render_list) # empty render list! wtf?
    breakpoint()

    # now render the file. how to make it happen?

    # avaliable_cuts = content


def getProducerTemplate(template):
    producer_mapping = {"pets_with_music": petsWithMusicProducer}
    return producer_mapping[template]
