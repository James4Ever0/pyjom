from pyjom.commons import *

# from pyjom.modules.contentProducing.videoProcessing import *
# it is like a game designed by you, played by everyone.

# maybe you need to render this into ffmpeg arguments or mltframework arguments.
import random
import pylrc
import math

import audioowl
from MediaInfo import MediaInfo
from pyjom.medialang.core import *


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


def getMusicCutSpansCandidates(
    music, lyric_path, maxtime, mintime, mbeat_time_tolerance=0.8
):
    beats, bpm = audioOwlAnalysis(music["filepath"])
    lyric = read_lrc(lyric_path)
    # print(lyric)
    # breakpoint()
    lyric_times = [x["time"] for x in lyric]
    lyric_times.sort()
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


def getFileCuts(
    filtered_info, meta_info, standard_bpm_spans, policy_names, mbeat_time_tolerance=0.8
):
    total_cuts_dict = {}
    for (
        file_path,
        cuts,
    ) in (
        filtered_info.items()
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
                    framework_candidates.sort(key=lambda x: -(x[1][1] - x[1][0]))
                    if len(framework_candidates) > 0:
                        framework_candidate = framework_candidates[0]
                        modifiers.update(framework_candidate)
                        # add that modifier.
            compiled_file_cuts.append(new_cut)
        total_cuts_dict.update({file_path: compiled_file_cuts.copy()})
    return total_cuts_dict


def getRenderList(
    total_cuts,
    demanded_cut_spans,
    noRepeat=False,
    noRepeatFileName=False,
    total_trials=100000,
):
    trial_count = 0
    file_access_list = [x for x in total_cuts.keys()]
    FAL_generator = infiniteShuffle(
        file_access_list
    )  # infinite generator! may cause serious problems.
    TC_generators = {
        key: infiniteShuffle(total_cuts[key]) for key in total_cuts.keys()
    }  # again infinite generator!
    render_list = []
    if noRepeat:
        usedCuts = []
    for span in demanded_cut_spans:
        start, end = span
        span_length = end - start
        tolerance = 0.8
        tolerance_decrease = lambda x: max(0.1, x - 0.1)
        for filename in FAL_generator:
            if filename is None:
                tolerance = tolerance_decrease(tolerance)
                continue
            file_cuts = TC_generators[filename]
            # random.shuffle(file_cuts)
            selected_cut = None
            for cut in file_cuts:
                trial_count += 1
                if trial_count % 1000 == 0 and trial_count > 0:
                    print(
                        "%d trial quota used remaining: %d"
                        % (trial_count, total_trials - trial_count)
                    )
                if trial_count > total_trials:
                    raise Exception(
                        "Trial Limit Reached.\nCurrent RenderList: %s\nCurrent Limit: %d trials\nCurrent Config: noRepeat=%s noRepeatFileName=%s"
                        % (
                            str(render_list),
                            total_trials,
                            str(noRepeat),
                            str(noRepeatFileName),
                        )
                    )
                if cut is None:  # break if the infinite generator is taking a break.
                    break
                    # continue # really continue?
                cut_span = cut["span"]
                cut_duration = cut_span[1] - cut_span[0]
                if inRange(
                    cut_duration, [span_length, span_length * 1.5], tolerance=tolerance
                ):  # increase this tolerance gradually.
                    if noRepeat:
                        cut_str = str(cut) + filename
                        if noRepeatFileName:
                            sameSourceOfLastClip = False
                            if len(usedCuts) > 1:
                                lastClip = usedCuts[
                                    -1
                                ]  # this was wrong. usedCuts could have length == 1
                                if filename in lastClip:
                                    sameSourceOfLastClip = True  # this will detect if the next clip is of the same source of last clip
                            isRepeat = (cut_str in usedCuts) or sameSourceOfLastClip
                        else:
                            isRepeat = cut_str in usedCuts
                        if isRepeat:
                            continue  # repeated cuts!
                        usedCuts.append(cut_str)
                    selected_cut = cut
                    break
            if not selected_cut is None:
                # append the data right here.
                render_list.append({"span": span, "cut": cut, "source": filename})
                break
    return render_list


def renderList2MediaLang(
    renderList,
    slient=True,
    fast: bool = True,
    bgm=None,
    backend="ffmpeg",  # wtf is this ffmpeg?
):  # this is just a primitive. need to improve in many ways.
    # producer = ""
    scriptBase = [
        '(".mp4",backend = "%s", bgm = "%s", fast=%s)'
        % (backend, bgm, str(fast).lower())
    ]  # set default resolution to 1920x1080

    def getSpanDuration(span):
        return span[1] - span[0]

    for item in renderList:
        # print("ITEM:", item)
        span = item["span"]
        cut_span = item["cut"]["span"]
        source = item["source"]
        span_duration = getSpanDuration(span)
        cut_span_duration = getSpanDuration(cut_span)
        speed = cut_span_duration / span_duration
        # breakpoint()
        name = source
        line = '("%s", video=true, slient=%s, speed=%f, cutFrom=%f,cutTo=%f)' % (
            name,
            str(slient).lower(),
            speed,
            cut_span[0],
            cut_span[1],
        )
        scriptBase.append(line)
    # print(scriptBase)
    # now return the medialang object.
    medialangScript = "\n\n".join(scriptBase)  # forced to double return. is it?
    medialangObject = Medialang(script=medialangScript)
    return medialangObject


# fix long loading time.
@redisLRUCache()
def getMusicInfoParsed(config):
    music = config["music"]
    # check if music is corrupted?
    font = config.get("font",None)
    policy = config.get("policy",{})
    policy_names = [x for x in policy.keys()]
    # get music duration here.
    music_metadata = get_media_info(music["filepath"])
    music_duration = music_metadata["duration"]
    maxtime = config["maxtime"]
    mintime = config["mintime"]
    lyric_path = music.get("lyric_path", None)
    if not os.path.exists(lyric_path):
        lyric_path = None
    demanded_cut_spans, standard_bpm_spans = getMusicCutSpans(
        music, music_duration, lyric_path, maxtime, mintime
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


def petsWithMusicProducer(filtered_info, meta_info, config={}):
    # what is this config? how the fuck we can arrange it?
    # config = {"music":{"filepath":"","lyric_path":""},"font":{"filepath":"","fontsize":30}, "policy":{"some_policy_name":{}},"meta":{"maxtime":3, "mintime":1}}
    # how to auto-warp the AAS subtitle?
    (
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
    ) = getMusicInfoParsed(config)
    # do you fill timegap with a loop?
    total_cuts = {}
    # print("DEMANDED CUT SPANS: " , demanded_cut_spans) # test passed.
    # breakpoint()
    # demanded_cut_spans is empty!
    # total_cuts
    total_cuts = getFileCuts(
        filtered_info, meta_info, standard_bpm_spans, policy_names
    )  # is this shit empty?
    # this can be infinity loop.
    # sample: [{'span': (0, 3.9300226757369616), 'cut': {'span': (13.4, 18.0), 'modifiers': {}}, 'source': '/root/Desktop/works/pyjom/samples/video/LiGGLhv4E.mp4'}]
    # print(total_cuts)
    # breakpoint()

    # now generate the freaking video.
    # if "one_clip_per_file" in policy_names:
    #     used_files = [] # may raise exception.
    # total_cuts {} and demanded_cut_spans [] are both empty
    render_list = getRenderList(
        total_cuts, demanded_cut_spans
    )  # this might be an infinity loop.
    # but why the fuck we got 10 minutes long of the freaking video?
    print(render_list)  # empty render list! wtf?
    # why the fuck we have duplicated clips? why the fuck?
    breakpoint()  # WTF IS GOING ON? LEADING TO 10 MINS OF CRAP?
    medialangObject = renderList2MediaLang(
        render_list,
        slient=True,
        bgm=music["filepath"],
        producer="editly",  # 在这里你可以分离人声 如果想热闹的话 原视频的音乐就不需要了 可能吧
    )  # what is the backend?

    # print(medialangObject)
    # breakpoint()
    medialangCode = medialangObject.prettify()
    # print("_________________MEDIALANG CODE_________________")
    # print(medialangCode) # should you write it to somewhere?
    import uuid

    randomName = str(uuid.uuid4())
    medialangCodeSavePath = os.path.join(
        "/root/Desktop/works/pyjom/tests/medialang_tests", "{}.mdl".format(randomName)
    )
    with open(medialangCodeSavePath, "w+") as f:
        f.write(medialangCode)
    print("MEDIALANG CODE SAVED TO:", medialangCodeSavePath)
    # why use medialang? probably because these render language are not "fully automated" or "automated enough" to express some abstract ideas? or just to leave some blanks for redundent low-level implementations?
    # print("_________________MEDIALANG CODE_________________")
    medialangObject.execute()  ## shit will happen.
    # next time you could test medialang directly.

    # medialangObject.eval() # is something like that?

    # slient all things? despite its config.
    # now render the file. how to make it happen?


# first, we state the format of the input.
# [{'span': (296.4719954648526, 302.915), 'cut': {'span': (50.8, 57.2), 'modifiers': {}}, 'source': '/root/Desktop/works/pyjom/samples/video/LiGfl6lvf.mp4'}, {..},...]
# avaliable_cuts = content
# shall we generate medialang for it?

from pyjom.commons import checkMinMaxDict
from pyjom.lyrictoolbox import lrcToAnimatedAss
from lazero.filesystem import tmpdir

from lazero.network.progressbar.client import netProgressbar


def petsWithMusicOnlineProducer(
    dataGenerator,
    configs,
    tempdir="/dev/shm/medialang/pets_with_music_online",
    remove_unused=True,
    fast: bool = True,
):
    import uuid

    NetProgressbar = netProgressbar()
    with tmpdir(path=tempdir) as TD:
        getRandomFileName = lambda extension: os.path.join(
            tempdir, ".".join([str(uuid.uuid4()), extension])
        )
        for config in configs:
            musicPath = config.get('music',"")
            if os.path.exists(musicPath):
                from pyjom.commons import corruptMediaFilter
                report = corruptMediaFilter(musicPath)
                if not report:
                    print("music file corrputed")
                    sprint("music path:",musicPath)
                    return False
            else:
                print('music file does not exist')
                sprint("music path:",musicPath)
                return False
            return True
            report = corrputMedia
            if not report:
                continue

            render_ass = config.get('render_ass', False)
            parsed_result = getMusicInfoParsed(config)
            # print(parsed_result)
            # breakpoint()
            # we only have one song here. you fucking know that?
            (
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
            ) = parsed_result  # this is taking long time.
            # check for 'demanded_cut_spans' now!

            render_list = []  # what is this freaking render_list?
            # [{'span':(start,end),'cut':{'span':(start,end)},'source':videoSource},...]
            # if lyric_path:
            if render_ass:
                ass_file_path = getRandomFileName("ass")
                # print("lrc path:", lyric_path)
                # print('ass file path:',ass_file_path)
                # breakpoint()
                lrcToAnimatedAss(music["filepath"], lyric_path, ass_file_path)
            data_ids = []
            # from tqdm.gui import tqdm

            total_pops = len(demanded_cut_spans)
            # for _ in tqdm(range(total_pops)):
            NetProgressbar.reset(total=total_pops)

            for data in dataGenerator:
                # what is the format of the data?
                data_id = data["item_id"]
                if data_id not in data_ids:
                    dataDuration = data["meta"]["duration"]
                    videoSource = data["location"]
                    data_ids.append(data_id)
                    demanded_cut_spans.sort(
                        key=lambda span: abs((span[1] - span[0]) - dataDuration)
                    )
                    closest_span = demanded_cut_spans[0]
                    closest_span_duration = closest_span[1] - closest_span[0]
                    speed_delta = dataDuration / closest_span_duration
                    # for time duration of 0.6 seconds, how the fuck you can fit in?
                    span = closest_span
                    candidate = {
                        "span": span,
                        "cut": {"span": (0, dataDuration)},
                        "source": videoSource,
                    }
                    append_render_list = False
                    case = None

                    if checkMinMaxDict(speed_delta, {"min": 0.8, "max": 1.2}):
                        case = "nearby"
                        append_render_list = True
                        # break
                    elif checkMinMaxDict(speed_delta, {"min": 1.2, "max": 3}):
                        case = "trim"
                        append_render_list = True
                        from pyjom.videotoolbox import motionVectorEstimation

                        dataDict = motionVectorEstimation(videoSource)
                        referenceData = dataDict[
                            "average_global_weighted_motion_vectors_filtered_cartesian_distance"
                        ]
                        from pyjom.mathlib import getCursorOfMaxAverageInWindow

                        cursor = getCursorOfMaxAverageInWindow(
                            referenceData, closest_span_duration * 1.2, dataDuration
                        )
                        # cursor = random.uniform(0,dataDuration-closest_span_duration*1.2) # this is not exactly right. not even good.
                        # you should utilize the 'motion vector' stuff.
                        mStart, mEnd = 0 + cursor, min(
                            closest_span_duration * 1.2 + cursor, dataDuration
                        )
                        candidate["cut"]["span"] = (mStart, mEnd)

                    if append_render_list:
                        demanded_cut_spans.pop(0)
                        NetProgressbar.update(
                            info={
                                "remainings": len(demanded_cut_spans),
                                "case": case,
                                "data": candidate,
                            }
                        )
                        render_list.append(candidate)
                    else:
                        if remove_unused:
                            videoPath = videoSource
                            if os.path.exists(videoPath):
                                os.remove(videoPath)
                complete = len(demanded_cut_spans) == 0
                if complete:
                    break
            # the main shit will fuck up again, maybe.
            # so i wrapped it a little bit.
            try:
                medialangObject = renderList2MediaLang(
                    render_list,
                    slient=True,
                    fast=fast,
                    bgm=music["filepath"],
                    backend="editly",  # 在这里你可以分离人声 如果想热闹的话 原视频的音乐就不需要了 可能吧
                )  # what is the backend?
                rendered_media_location = (
                    medialangObject.execute()
                )  # how to control its 'fast' parameter?
                # maybe we need render the lyric file separately.
                # using a ffmpeg filter.
                print('RENDERED MEDIA LOCATION:',rendered_media_location)
                breakpoint()

                final_output_location = getRandomFileName("mp4")
                if render_ass:
                    import ffmpeg
                    ffmpeg.input(rendered_media_location).filter("ass", ass_file_path).output(
                        final_output_location
                    ).run(overwrite_output=True)
                else:
                    import shutil
                    shutil.move(rendered_media_location, final_output_location)
                yield final_output_location  # another generator?
            except:
                from lazero.utils.logger import traceError
                traceError("error while rendering medialang script",_breakpoint=True)


def getProducerTemplate(template: str):
    producer_mapping = {
        "pets_with_music": petsWithMusicProducer,
        "pets_with_music_online": petsWithMusicOnlineProducer,
    }
    return producer_mapping[template]
