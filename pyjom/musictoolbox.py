# you will have a better name for other toolboxs.

# for now, the musictoolbox is responsible for music/lyric retrieval/download, track separation, bpm, music recognition

# pitch shift, speedup/slowdown is for audiotoolbox

# voice change/synthesis is for voicetoolbox.

# diffusion based painter, ai colorization, video editing is for artworktoolbox. maybe the naming is not right/necessary.

# check AmadeusCore, /root/Desktop/works/pyjom/tests/music_recognization/AmadeusCore/src/components/app/models/

from types import FunctionType
from typing import Union
import audioowl
import math
from pyjom.commons import *
from pyjom.lyrictoolbox import read_lrc, getLyricNearbyBpmCandidates
from pyjom.audiotoolbox import getAudioDuration
import ffmpeg

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
        from lazero.utils.mathlib import getTruncatedNormalDistribution

        std, mean = gaussian_args["std"], gaussian_args["mean"]
        # scale, loc = std, mean
        myStart, myEnd = mintime, maxtime
        randomFunction = getTruncatedNormalDistribution(std, mean, myStart, myEnd)
        # myclip_a, myclip_b = mintime, maxtime
        # from scipy.stats import truncnorm

        # a, b = (myclip_a - loc) / scale, (myclip_b - loc) / scale
        # randVar = truncnorm(a, b)
        # randomFunction = lambda: randVar.rvs(1)[0] * scale + loc

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
import subprocess
import traceback

from lazero.program.subprocess import runCommandGetJson


def runCommandAndProcessSongRecognizationJson(
    commandLine: list[str],
    processMethod: FunctionType,
    raw_data: bool = False,
    debug: bool = False,
    timeout: int = 5,
    workingDirectory: Union[None, str] = None,
):
    success, data = runCommandGetJson(
        commandLine, debug=debug, timeout=timeout, workingDirectory=workingDirectory
    )
    if success:
        if not raw_data:
            # more processing. may alter the success flag.
            try:
                data = processMethod(data)
            except:
                success = False
                if debug:
                    traceback.print_exc()
    return success, data


def shazamSongRecognizationResultProcessMethod(data):
    artist = data["track"]["subtitle"]
    trackName = data["track"]["title"]
    data = {"artist": artist, "trackName": trackName}
    return data


# you can choose to return raw data or not. which is the raw json data.
def recognizeMusicFromFileSongrec(filepath, raw_data=False, timeout=6, debug=False):
    commandLine = ["songrec", "audio-file-to-recognized-song", filepath]
    return runCommandAndProcessSongRecognizationJson(
        commandLine,
        shazamSongRecognizationResultProcessMethod,
        raw_data=raw_data,
        debug=debug,
        timeout=timeout,
    )


def recognizeMusicFromFileShazamIO(
    filepath, raw_data=False, timeout=20, debug: bool = False
):
    # how to timeout this shit? use subprocess again?
    # maybe yes.
    commandLine = [
        "python3",
        "/root/Desktop/works/pyjom/tests/soundhound_houndify_midomi_sound_recognize_music/shazamio_recognize_music.py",
        "--file",
        filepath,
    ]
    return runCommandAndProcessSongRecognizationJson(
        commandLine,
        shazamSongRecognizationResultProcessMethod,
        raw_data=raw_data,
        debug=debug,
        timeout=timeout,
    )


def midomiSongRecognizationResultProcessMethod(data):
    trackData = data["AllResults"][0]["NativeData"]["Tracks"][0]
    artist = trackData["ArtistName"]
    trackName = trackData["TrackName"]
    data = {"artist": artist, "trackName": trackName}
    return data


# what is the correct timeout for this one?
from lazero.filesystem.temp import tmpfile, getRandomFileNameUnderDirectoryWithExtension


def recognizeMusicFromFileMidomi(
    filepath,
    raw_data=False,
    timeout=10,
    debug: bool = False,
    maxRetry=3,
    segmentLength: int = 10,
    extension: Union[str, None] = None,
):  # this one is different. maybe we can wait.
    success, data = False, {}
    if extension == None:
        extension = ""
        splitedFilePath = os.path.basename(filepath).split(".")
        if len(splitedFilePath) > 1:
            extension = splitedFilePath[-1]
    if len(extension) == 0:
        extension = "mp3"
    musicLength = getAudioDuration(filepath)
    needSegment = musicLength > segmentLength
    if not needSegment:
        maxRetry = 1
    for index in range(maxRetry):
        if debug:
            print("trial {} for midomi".format(index + 1))
        segmentName = getRandomFileNameUnderDirectoryWithExtension(
            extension, "/dev/shm"
        )

        with tmpfile(segmentName):
            if needSegment:
                start = random.uniform(0, musicLength - segmentLength)
                end = start + segmentLength
                ffmpeg.input(filepath, ss=start, to=end).output(segmentName).run(
                    overwrite_output=True
                )
            else:
                pathlib.Path(segmentName).touch()
                segmentName = filepath
            # you will change to given directory, will you?
            commandLine = ["npx", "ts-node", "midomi_music_recognize.ts", segmentName]
            success, data = runCommandAndProcessSongRecognizationJson(
                commandLine,
                midomiSongRecognizationResultProcessMethod,
                raw_data=raw_data,
                debug=debug,
                timeout=timeout,
                workingDirectory="/root/Desktop/works/pyjom/tests/music_recognization/AmadeusCore",
            )
        if success:
            break
    return success, data


def recognizeMusicFromFile(
    filepath,
    backend: Literal["songrec", "shazamio", "midomi", None] = None,
    raw_data=False,
    debug=False,
):  # if not returning raw_data, only track data and artist data are returned.
    assert os.path.exists(filepath)
    # if returning raw_data, must also return the provider name, for easy parsing.
    # you can try all methods. but if all three methods fails, you know what to do. what indicates the recognizer has failed?
    # you can try something erotic.
    if backend is None:  # auto
        musicDuration = getAudioDuration(filepath)
        if musicDuration <= 15:
            backend = "midomi"
        else:
            backend = "songrec"
    methods = {
        "midomi": recognizeMusicFromFileMidomi,
        "songrec": recognizeMusicFromFileSongrec,
        "shazamio": recognizeMusicFromFileShazamIO,
    }
    keys = list(methods.keys())
    keys.sort(key=lambda x: -int(x == backend))
    for key in keys:
        method = methods[key]
        success, data = method(filepath, debug=debug)
        if debug:
            print("DATA:")
            print(data)
            print("RETURN FROM MUSIC RECOGNIZE METHOD: %s" % key)
            print("SUCCESS:", success)
        if success:
            if raw_data:
                return success, data, key
            else:
                return success, data
        if debug:
            break  # no retry then.
    if raw_data:
        return False, {}, ""
    return False, {}


############ SEARCH NETEASE MUSIC, GET SIMILAR MUSIC BY ID, DOWNLOAD MUSIC AND LYRICS ############

import requests
from lazero.program.functools import suppressException


class neteaseMusic:
    def __init__(self, port: int = 4042):
        self.baseUrl = "http://localhost:{}".format(port)

    def verifyResponseCodeAndGetJson(
        self, response, debug: bool = False, success_codes: list[int] = [200]
    ):
        response_json = response.json()  # check search_result.json
        if success_codes != []:
            code = response_json["code"]
            if not code in success_codes:
                if debug:
                    print(response_json)
                import traceback

                traceback.print_exc()
                raise Exception("ERROR CODE IN NETEASE API RESPONSE:", code)
        return response_json

    def requestWithParamsGetJson(
        self,
        suffix: str,
        params: dict = {},
        debug: bool = False,
        success_codes: list[int] = [200],
        refresh: bool = False,
    ):
        if refresh:
            params.update({"timestamp": getJSTimeStamp()})
        suffix = suffix.strip()
        if not suffix.startswith("/"):
            suffix = "/" + suffix
        link = self.baseUrl + suffix
        result = requests.get(link, params=params)
        result_json = self.verifyResponseCodeAndGetJson(
            result, debug=debug, success_codes=success_codes
        )
        return result_json

    @suppressException(tries=2, defaultReturn={})
    def searchNeteaseMusicByQuery(
        self, query: Union[list, str], debug: bool = False, refresh: bool = False
    ):
        if type(query) == str:
            query = query.strip()
        else:
            query = [elem.strip() for elem in query]
            query = " ".join([elem for elem in query if len(elem) > 0])
        assert len(query) > 0
        search_result_json = self.requestWithParamsGetJson(
            "/search",
            params={"keywords": query},
            debug=debug,
            refresh=refresh,
        )
        return search_result_json

    @suppressException(defaultReturn=[])
    def getSimilarMusicByIdFromNetease(
        self, music_id: int, debug: bool = False, refresh: bool = False
    ):
        r_json = self.requestWithParamsGetJson(
            "/simi/song", params={"id": music_id}, debug=debug, refresh=refresh
        )
        song_ids = []
        for song in r_json["songs"]:
            name = song["name"]
            song_id = song["id"]
            song_ids.append(song_id)
            # what you want?
        return song_ids

    @suppressException()
    def getMusicUrlFromNetease(
        self, music_id: int, debug: bool = False, refresh: bool = False
    ):
        r_json = self.requestWithParamsGetJson(
            "/song/url", params={"id": music_id}, debug=debug, refresh=refresh
        )  # this song might expire. warning!
        # expire in a few seconds.
        url = r_json["data"][0].get("url", None)
        return url  # you may test this url. later.

    @suppressException(defaultReturn=False)
    def checkMusicFromNetEase(
        self, music_id: int, debug: bool = False, refresh: bool = False
    ):
        # {
        #   "success": true,
        #   "message": "ok"
        # }
        # no need to check the return code.
        r_json = self.requestWithParamsGetJson(
            "check/music",
            params={"id": music_id},
            debug=debug,
            refresh=refresh,
            success_codes=[],
        )
        assert r_json["success"] == True
        assert r_json["message"] == "ok"
        return True

    @suppressException()
    def getMusicLyricFromNetease(
        self,
        music_id: int,
        debug: bool = False,
        refresh: bool = False,
        minLyricStringLength: int = 50,
    ):
        r_json = self.requestWithParamsGetJson(
            "/lyric",
            params={"id": music_id},
            debug=debug,
            refresh=refresh,
        )
        # warning: the fetched lrc could be not so clean. clean it somehow!
        lyric_string = r_json["lrc"]["lyric"]
        if lyric_string != None and type(lyric_string) == str:
            if len(lyric_string) > minLyricStringLength:
                return lyric_string

    @suppressException(tries=2, defaultReturn=((None, None), None))
    def getMusicAndLyricWithKeywords(
        self,
        keywords: str,
        similar: bool = False,
        debug: bool = False,
        min_audio_length: float = 2 * 60,
        max_audio_length: float = 5 * 60
    ):  # minimum 2.5 minutes of music.
        import pyjq

        # store the downloaded file in some place please?
        search_data_json = self.searchNeteaseMusicByQuery(keywords, debug=debug)
        # print(search_data_json)
        song_ids = pyjq.all(
            ".result.songs[] | select (.id !=null) | .id", search_data_json
        )  # incorrect. use pyjq.all
        # print(song_ids)
        # breakpoint()

        song_id = random.choice(song_ids)
        # how to parse this shit?
        if similar:
            similar_song_ids = self.getSimilarMusicByIdFromNetease(song_id, debug=debug)
            song_id = random.choice(similar_song_ids)
        # now download the music.
        music_url = self.getMusicUrlFromNetease(song_id, debug=debug, refresh=True)
        # download the music right now.
        r = requests.get(music_url)
        if debug:
            print("download music status code:", r.status_code)
        assert r.status_code == 200  # are you sure the code is ok?
        music_format = music_url.split(".")[-1]
        music_content = r.content
        # how to get song duration?
        import tempfile

        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".{}".format(music_format)
        ) as f:
            name = f.name
            name = os.path.abspath(name)
            f.write(music_content)
            song_duration = getAudioDuration(name)
        if song_duration < min_audio_length:
            raise Exception("audio too short, total {} seconds".format(song_duration))
        elif song_duration > max_audio_length:
            raise Exception("audio too long, total {} seconds".format(song_duration))
        lyric_string = self.getMusicLyricFromNetease(song_id)
        if debug:
            print("LYRICS:", lyric_string)
        if type(lyric_string) ==str and lyric_string.strip() !="":
            from pyjom.lyrictoolbox import (
                cleanLrcFromWeb,
            )  # cleaning needs song duration.

            lyric_string = cleanLrcFromWeb(lyric_string, song_duration)
        return (music_content, music_format), lyric_string


############ SEARCH NETEASE MUSIC, GET SIMILAR MUSIC BY ID, DOWNLOAD MUSIC AND LYRICS ############
