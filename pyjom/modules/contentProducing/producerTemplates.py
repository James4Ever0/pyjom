from pyjom.commons import *

# from pyjom.modules.contentProducing.videoProcessing import *
# it is like a game designed by you, played by everyone.

# maybe you need to render this into ffmpeg arguments or mltframework arguments.
import random
from pyjom.audiotoolbox import adjustVolumeInMedia
from pyjom.musictoolbox import getMusicInfoParsed

# from MediaInfo import MediaInfo
from pyjom.medialang.core import *


# local
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


# local
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


# local
def renderList2MediaLang(
    renderList,
    slient=True,
    fast: bool = True,
    bgm=None,
    backend="ffmpeg",  # wtf is this ffmpeg?
    medialangTmpdir="/dev/shm/medialang",
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
    medialangObject = Medialang(script=medialangScript, medialangTmpdir=medialangTmpdir)
    return medialangObject


# local
def petsWithMusicProducer(filtered_info, meta_info, config={}, fast=False):
    # what is this config? how the fuck we can arrange it?
    # config = {"music":{"filepath":"","lyric_path":""},"font":{"filepath":"","fontsize":30}, "policy":{"some_policy_name":{}},"meta":{"maxtime":3, "mintime":1}}
    # how to auto-warp the AAS subtitle?
    # musicPath = config.get('music',"")
    musicPath = config.get("music", {}).get("filepath", "")
    debug = config.get("debug", False)
    report = corruptMediaFilter(musicPath)
    if not report:
        return False

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
    if debug:
        print(render_list)  # empty render list! wtf?
    # why the fuck we have duplicated clips? why the fuck?
    # breakpoint()  # WTF IS GOING ON? LEADING TO 10 MINS OF CRAP?
    medialangObject = renderList2MediaLang(
        render_list,
        slient=True,
        bgm=music["filepath"],
        backend="editly",  # 在这里你可以分离人声 如果想热闹的话 原视频的音乐就不需要了 可能吧
        fast=fast,
    )  # what is the backend?

    # print(medialangObject)
    # breakpoint()
    medialangCode = medialangObject.prettify()
    # print("_________________MEDIALANG CODE_________________")
    # print(medialangCode) # should you write it to somewhere?
    if debug:
        import uuid

        randomName = str(uuid.uuid4())
        # or just use some temporary file instead?
        medialangCodeSavePath = os.path.join(
            "/root/Desktop/works/pyjom/tests/medialang_tests",
            "{}.mdl".format(randomName),
        )
        with open(medialangCodeSavePath, "w+") as f:
            f.write(medialangCode)
        print("MEDIALANG CODE SAVED TO:", medialangCodeSavePath)
    # why use medialang? probably because these render language are not "fully automated" or "automated enough" to express some abstract ideas? or just to leave some blanks for redundent low-level implementations?
    # print("_________________MEDIALANG CODE_________________")
    (
        editly_outputPath,
        medialang_item_list,
    ) = medialangObject.execute()  ## shit will happen.
    # next time you could test medialang directly.

    # medialangObject.eval() # is something like that?
    return editly_outputPath

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

# local
def petsWithMusicOnlineProducer(
    dataGenerator,
    configs,
    tempdir="/dev/shm/medialang/pets_with_music_online",
    remove_unused=True,
    fast: bool = True,
    medialangTmpdir="/dev/shm/medialang",
):
    import uuid

    NetProgressbar = netProgressbar()
    with tmpdir(path=tempdir) as TD:
        getRandomFileName = lambda extension: os.path.join(
            tempdir, ".".join([str(uuid.uuid4()), extension])
        )
        for config in configs:
            try:
                debug = config.get("debug", False)  # in config.
                musicPath = config.get("music", {}).get("filepath", "")
                translate = config.get("translate", False)
                # also how to translate?
                translate_method = config.get("translate_method", "baidu")
                # from pyjom.commons import corruptMediaFilter
                report = corruptMediaFilter(musicPath)
                if not report:
                    continue

                render_ass = config.get("render_ass", False)
                ass_template_configs = config.get("ass_template_configs", {})
                assStyleConfig = config.get("assStyleConfig", {})

                parsed_result = getMusicInfoParsed(config) # will raise exception. what to do?
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
                from pyjom.lyrictoolbox import remergeDemandedCutSpans
                
                demanded_cut_spans = remergeDemandedCutSpans(demanded_cut_spans)

                render_list = []  # what is this freaking render_list?
                # [{'span':(start,end),'cut':{'span':(start,end)},'source':videoSource},...]
                # if lyric_path:
                render_ass = render_ass and (lyric_path is not None)
                if render_ass:
                    ass_file_path = getRandomFileName("ass")
                    # print("lrc path:", lyric_path)
                    # print('ass file path:',ass_file_path)
                    # breakpoint()
                    lrcToAnimatedAss(
                        music["filepath"],
                        lyric_path,
                        ass_file_path,
                        translate=translate,
                        translate_method=translate_method,
                        ass_template_configs=ass_template_configs,
                        assStyleConfig=assStyleConfig,
                    )  # here's the 'no translation' flag.
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
                        elif checkMinMaxDict(speed_delta, {"min": 1.2, "max": 5}):
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
                        if not append_render_list:
                            print(f'fail to match. source: {dataDuration} target: {closest_span_duration}')
                            if remove_unused:
                                videoPath = videoSource
                                if os.path.exists(videoPath):
                                    os.remove(videoPath)
                        else:
                            demanded_cut_spans.pop(0)
                            NetProgressbar.update(
                                info={
                                    "remainings": len(demanded_cut_spans),
                                    "case": case,
                                    "data": candidate,
                                    'last_5_spans_time':[x[1]-x[0] for x in demanded_cut_spans[:5]]
                                } # this last cut must be seriously wrong.
                            )
                            render_list.append(candidate)
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
                        medialangTmpdir=medialangTmpdir,
                    )  # what is the backend?
                    # we first create a backup for this medialang script, please?
                    medialangScript = medialangObject.prettify()
                    if debug:
                        medialangScript_savedPath = getRandomFileName("mdl")
                        with open(
                            medialangScript_savedPath, "w+"
                        ) as f:  # will this shit work?
                            f.write(medialangScript)
                        print("MEDIALANG SCRIPT SAVED TO:", medialangScript_savedPath)

                    (
                        editly_outputPath,
                        medialang_item_list,
                    ) = medialangObject.execute()  # how to control its 'fast' parameter?
                    # maybe we need render the lyric file separately.
                    # normalization starts here.
                    rendered_media_location = getRandomFileName(
                        "mp4"
                    )  # so where exactly is the file?
                    print("___adjusting volume in media___")
                    adjustVolumeInMedia(editly_outputPath, rendered_media_location)
                    # using a ffmpeg filter.
                    print("RENDERED MEDIA LOCATION:", rendered_media_location)
                    if debug:  # where is this debug??
                        breakpoint()
                    # following process is non-destructive for audio.
                    # you need audio normalization before these process.
                    final_output_location = getRandomFileName("mp4")
                    if render_ass:
                        import ffmpeg
                        # [Parsed_ass_0 @ 0x5568c7a266c0] fontselect: (Migu 1P, 700, 0) -> /usr/share/fonts/truetype/ttf-bitstream-vera/VeraBd.ttf, 0, BitstreamVeraSans-Bold
                        # [Parsed_ass_0 @ 0x5568c7a266c0] Glyph 0x665A not found, selecting one more font for (Migu 1P, 700, 0)
                        # [Parsed_ass_0 @ 0x5568c7a266c0] fontselect: (Migu 1P, 700, 0) -> /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc, 0, WenQuanYiZenHei

                        videoInput = ffmpeg.input(rendered_media_location).video
                        audioInput = ffmpeg.input(rendered_media_location).audio
                        videoInput = videoInput.filter(
                            "ass", ass_file_path
                        )
                        ffmpeg.output(videoInput,audioInput,final_output_location,acodec='copy').run(overwrite_output=True)
                    else:
                        import shutil

                        shutil.move(rendered_media_location, final_output_location)
                    yield final_output_location  # another generator?
                except:
                    from lazero.utils.logger import traceError

                    traceError("error while rendering medialang script")
                    try:
                        print("MEDIALANG SCRIPT SAVED TO:", medialangScript_savedPath)
                    except:
                        pass
                    # if debug:
                    breakpoint()
                    # continue? let's see if you can post it?
            except:
                import traceback
                traceback.print_exc()
                # well it could be "unanalyzable" BGM, unable to retrieve 'standardBPM' or so on.
                print('Unknown error during production. Skipping.')
                continue


# local
def getProducerTemplate(template: str):
    producer_mapping = {
        "pets_with_music": petsWithMusicProducer,
        "pets_with_music_online": petsWithMusicOnlineProducer,
    }
    return producer_mapping[template]
