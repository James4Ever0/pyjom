from pyjom.medialang.functions import *
from pyjom.medialang.commons import *
from pyjom.mathlib import *
from pyjom.videotoolbox import *
import tempfile
import ffmpeg


def executeEditlyScript(medialangTmpDir, editly_json):
    editlyJsonSavePath = os.path.join(medialangTmpDir, "editly.json")
    with open(editlyJsonSavePath, "w+", encoding="utf8") as f:
        f.write(json.dumps(editly_json, ensure_ascii=False))
    print("EXECUTING EDITLY JSON AT %s" % editlyJsonSavePath)
    commandline = ["xvfb-run", "editly", "--json", editlyJsonSavePath]
    print(commandline)
    status = subprocess.run(commandline)  # is it even successful?
    returncode = status.returncode
    assert returncode == 0
    print("RENDER SUCCESSFUL")


def ffmpegVideoPreProductionFilter(
    filepath,  # this is actually a video path. must be video here.
    start=None,
    end=None,
    cachePath=None,
    filters=["pipCrop", "textRemoval", "logoRemoval"],
    preview=True,
    # padding=True,
    paddingBlur=True,
    output_width=1920,
    output_height=1080,
):  # what is the type of this shit?
    # enable that 'fast' flag? or we use low_resolution ones? not good since that will ruin our detection system!
    # anyway it will get processed? or not?
    # uncertain. very uncertain.
    def paddingBlurFilter(stream, mWidth=1920, mHeight=1080):
        video_stream = stream.video
        output_width = mWidth
        output_height = mHeight
        layer_0 = video_stream.filter("scale", w=output_width, h=output_height).filter(
            "gblur", sigma=9
        )
        layer_1 = video_stream.filter(
            "scale",
            w="min(floor(iw*{}/ih),{})".format(output_height, output_width),
            h="min(floor(ih*{}/iw),{})".format(output_width, output_height),
        )
        output_stream = layer_0.overlay(layer_1, x="floor((W-w)/2)", y="floor((H-h)/2)")
        return output_stream

    def paddingFilter(stream, mWidth=1920, mHeight=1080):
        width = "max(iw, ceil(ih*max({}/{}, iw/ih)))".format(mWidth, mHeight)
        height = "max(ih, ceil(iw*max({}/{}, ih/iw)))".format(mHeight, mWidth)
        x = "max(0,floor(({}-iw)/2))".format(width)
        y = "max(0,floor(({}-ih)/2))".format(height)
        return (
            stream.filter(
                "pad", width=width, height=height, x=x, y=y, color="black"
            )  # here to control the padding logic, decide how to 'blur' the thing!
            .filter("scale", w=mWidth, h=mHeight)
            .filter("setsar", 1)
        )

    assert cachePath is not None
    assert start is not None
    assert end is not None
    # from 4 to 10 seconds?
    defaultWidth, defaultHeight = getVideoWidthHeight(filepath)
    previewRatio = 1
    if preview:
        previewWidth, previewHeight = getVideoPreviewPixels(filepath)
        previewRatio = previewWidth / defaultWidth

        def previewFilter(stream):
            # maintain original ratio?
            return stream.filter(
                "scale",
                "ceil((iw*{})/4)*4".format(previewRatio),
                "ceil((ih*{})/4)*4".format(previewRatio),
            )

    # stream = ffmpeg.hflip(stream)
    # this fliping may be useful for copyright evasion, but not very useful for filtering. it just adds more computational burden.
    # we just need to crop this.
    # stream = ffmpeg.output(stream, cachePath)
    # ffmpeg.run(stream, overwrite_output=True)

    # procedureList = []
    # stream = ffmpeg.input
    # no_processing = True # change this flag if anything need to change in original video according to filter results.

    # logo removal/text removal first, pipCrop last.
    # if overlap, we sort things.
    # if not, no sorting is needed.
    mDict = {}

    def delogoFilter(stream, commandParams):
        return stream.filter(
            "delogo",
            x=commandParams["x"],
            y=commandParams["y"],
            w=commandParams["w"],
            h=commandParams["h"],
        )

    def cropFilter(stream, commandParams):
        return stream.filter(
            "crop",
            x=commandParams["x"],
            y=commandParams["y"],
            w=commandParams["w"],
            h=commandParams["h"],
        )

    def filterCommandStringParser(filterCommandString):
        args_with_kwargs = filterCommandString.split(":")
        args = []
        kwargs = {}
        for elem in args_with_kwargs:
            if "=" in elem:
                key, value = elem.split("=")
                kwargs.update({key: value})
            else:
                args.append(elem)
        return args, kwargs

    def ffmpegStringFilter(stream, commandString):
        filterName = commandString.split("_")[0]
        filterPrefix = "{}_".format(filterName)
        filterCommandString = commandString[len(filterPrefix) :]
        args, kwargs = filterCommandStringParser(filterCommandString)
        return stream.filter("scale", *args, **kwargs)

    # TODO: FIX THIS SHIT!
    # raise Exception("TODO: FIX THIS SHIT!")

    # these things are ordered to be the last ones. just flags.
    from caer.video.frames_and_fps import get_duration

    video_start = 0
    video_end = get_duration(filepath)
    if "randomFlip" in filters:
        if random.random() > 0.5:
            mDict.update({"hflip": [(start, end)]})
    if "superResolution" in filters:
        mDict.update({"scale_w=iw*2:h=ih*2:flags=lanczos": [(start, end)]})
        # how to parse this shit?
    simpleFilters = ["minterpolate", "removegrain", "bilateral"]
    for filterName in simpleFilters:
        if filterName in filters:
            mDict.update({filterName: [(start, end)]})

    pipCropDicts = None
    if "pipCrop" in filters:
        # remember: if pip crop makes any of our logoRemoval or textRemoval filters invalid, we do not execute them.
        # also it will affect parameters of logoRemoval.
        pipCropDicts = detectPipRegionOverTime(filepath, start, end)
        mDict.update(pipCropDicts)  # using default settings?
        # pass
    if "textRemoval" in filters:
        # process the video, during that duration. fast seek avaliable?
        mDict.update(detectTextRegionOverTime(filepath, start, end))
        # pass
    if "logoRemoval" in filters:
        # dual safe? no?
        stationaryLogoDicts = detectStationaryLogoOverTime(
            filepath, start, end, pipCropDicts=pipCropDicts
        )  # this need to be improvised. if it is long, we need to do another check.
        if video_end > 30:
            stationaryLogoDicts.update(
                detectStationaryLogoOverTime(
                    filepath, video_start, video_end, cornersOnly=False, top_k=5
                )  # are you sure? wtf?
                # i mean area size similar than one of the corners.
            )
        # reprocess these things. really?
        mDict.update(stationaryLogoDicts)  # output logo mask. or not.
        # estimate the shape with multiple rectangles? packing algorithm?
        # polygon to rectangle? decomposition?
        # pass
    MAX_INT = 999999
    commandValueMap = {
        "empty": -1,
        "delogo": 0,
        "crop": 1,
        "removegrain": 2,
        "bilateral": 2,
        "scale": 3, ## wtf?
        "minterpolate": 4,
        "hflip": MAX_INT,
        "vflip": MAX_INT,
    }  # no scale filter shall present. we do not provide such creep. editly will handle it.
    # commandValueMap.update(simpleFiltersValueMap)
    renderDict = getContinualMappedNonSympyMergeResultWithRangedEmpty(mDict, start, end)

    # now we consider the rendering process. how?
    # shall we line it up?
    if (
        list(renderDict.keys()) == ["empty"] and not preview
    ):  # not preview! so we need not to downscale this thing.
        # nothing happens. just return the original shit.
        return filepath
    renderList = mergedRangesToSequential(renderDict)
    renderVideoStreamList = []
    renderAudioStream = ffmpeg.input(filepath, ss=start, to=end).audio
    # for elem in renderList:
    #     print(elem)
    # breakpoint()
    # videoDuration = getVideoDuration(videoPath)

    for renderCommandIndex, (renderCommandString, commandTimeSpan) in enumerate(
        renderList
    ):
        print("#{}".format(renderCommandIndex), renderCommandString, commandTimeSpan)
        mStart, mEnd = commandTimeSpan
        mStart = max(start, mStart)
        mEnd = min(mEnd, end)
        clipDuration = mEnd - mStart
        if clipDuration <= 0:
            continue  # if so, this clip is shit.
        # print("CLIP TIMESPAN:", mStart, mEnd)
        stream = ffmpeg.input(
            filepath, ss=mStart, to=mEnd
        ).video  # no audio? seriously?
        if renderCommandString == "empty":
            pass  # do not continue since maybe we have preview filter below?
            # still need to append shit below. we cannot skip this loop.
        # do nothing.
        else:
            renderCommands = renderCommandString.split("|")
            # sort all commands?
            renderCommands.sort(
                key=lambda command: commandValueMap[command.split("_")[0]]
            )
            from pyjom.mathlib import uniq

            for renderCommand in uniq(renderCommands):
                # print('RENDER COMMAND:',renderCommand, "SPAN", mStart, mEnd)
                # breakpoint()
                if renderCommand == "empty":
                    # yeah we have failsafe.
                    continue
                if "_" not in renderCommand:
                    stream = stream.filter(renderCommand)
                elif "=" in renderCommand:
                    stream = ffmpegStringFilter(
                        stream, renderCommand
                    )  # do not check for validity!
                else:
                    # non standard filter formats below. be warned.
                    for prefix, keyword in [
                        ("{}_".format(k), k) for k in ["delogo", "crop"]
                    ]:
                        if renderCommand.startswith(prefix):
                            import parse

                            commandParams = parse.parse(
                                keyword + "_{x:d}_{y:d}_{w:d}_{h:d}", renderCommand
                            )
                            # print(defaultWidth, defaultHeight)
                            mX, mY, mW, mH = (
                                commandParams["x"],
                                commandParams["y"],
                                commandParams["w"],
                                commandParams["h"],
                            )
                            status, XYWH = checkXYWH(
                                (mX, mY, mW, mH), (defaultWidth, defaultHeight)
                            )
                            if not status:
                                # cannot process this delogo filter since its parameters are outraged.
                                # shall we warn you?
                                # print("SOMEHOW DELOGO IS NOT WORKING PROPERLY")
                                # breakpoint()
                                # maybe it's not because of out of bounds error
                                print("_" * 30)
                                print(
                                    "ABNORMAL {} FILTER PARAMS:".format(
                                        keyword.upper()
                                    ),
                                    commandParams,
                                )
                                print(
                                    "maxX: {} maxY: {}".format(
                                        commandParams["x"] + commandParams["w"],
                                        commandParams["y"] + commandParams["h"],
                                    )
                                )
                                print("VALID BOUNDARIES:", defaultWidth, defaultHeight)
                                print("_" * 30)
                                continue
                            else:
                                (mX, mY, mW, mH) = XYWH
                                commandParams = {"x": mX, "y": mY, "w": mW, "h": mH}
                            # mX1, mY1 = mX+mW, mY+mH
                            # if mX1>defaultWidth or mY1>defaultHeight: # opecv to be blamed?
                            #     print("DELOGO ERROR:")
                            #     print(mX1,defaultWidth,mY1,defaultHeight)
                            #     breakpoint()
                            # we also need to consider if this is necessary.
                            if keyword == "delogo":
                                stream = delogoFilter(stream, commandParams)
                            elif keyword == "crop":
                                stream = cropFilter(stream, commandParams)
                                # TODO: the main shit happens here is that if pip region is detected, it (the crop region) will not maintain the width to height ratio. you might need padding, and that's what we about to do here. you may also extract that clip as standalone material.
                                # more inspection is needed for comprehensive reasoning.
        if paddingBlur:
            stream = paddingBlurFilter(
                stream, mWidth=output_width, mHeight=output_height
            )
        else:
            stream = paddingFilter(stream, mWidth=output_width, mHeight=output_height)
        if preview:  # final filter? need us to crop this?
            stream = previewFilter(
                stream
            )  # just preview, no need to set output width/height!
            # do nothing here! (no fx.)
        # and?
        # we need to concat these shit!
        # print(stream)
        # print(dir(stream))
        # breakpoint()
        # import copy
        # print(stream)
        renderVideoStreamList.append(stream)
    # for x in renderVideoStreamList:
    #     print(x)
    # print(len(renderVideoStreamList))
    # breakpoint()
    # breakpoint()
    renderVideoStream = ffmpeg.concat(*renderVideoStreamList)
    renderStream = ffmpeg.output(renderVideoStream, renderAudioStream, cachePath)
    args = renderStream.get_args()
    # print(args)
    # breakpoint()
    renderStream.run(overwrite_output=True)
    return cachePath


def dotVideoProcessor(
    item, previous, format=None, verbose=True, medialangTmpDir="/dev/shm/medialang/"
):
    # print("DOTVIDEO ARGS:", item, previous, format)
    # this item is the video output config, medialang item.
    itemArgs = item.args
    if format is None:
        format = item.path.split(".")[-1]
    backend = itemArgs.get(
        "backend", "editly"  # this is mere assumption!
    )  # so all things will be assumed to put directly into editly render json, unless explicitly specified under other medialang or other backend and need to be resolved into media file format before rendering. sure?
    fast = itemArgs.get("fast", True)
    bgm = itemArgs.get("bgm", None)
    # outputPath = itemArgs.get("",None)
    randomUUID = str(uuid.uuid4())
    outputPath = os.path.join(
        medialangTmpDir, randomUUID + "." + format
    )  # this is temporary!
    # usually we choose to use something under medialang tempdir as the storage place.
    print(format, backend, fast, bgm)

    # the "previous" is the clips, was fucked, filled with non-existant intermediate mpegts files, but no source was out there.
    # this is initially decided to output mp4, however you might want to decorate it.
    if verbose:
        print("_________INSIDE DOT VIDEO PROCESSOR_________")
        print("ITEM:", item)
        print("PREVIOUS:", previous)
        print("_________INSIDE DOT VIDEO PROCESSOR_________")
    with tempfile.TemporaryDirectory(
        dir=medialangTmpDir
    ) as tmpdirname:  # maybe you should take care of the directory prefix?
        # wtf are you doing over here?
        # find out where our cache leads to!
        # maybe the final product is one move away.
        tmpdirname = os.path.abspath(tmpdirname)
        print("created temporary directory", tmpdirname)

        output_path = os.path.join(
            tmpdirname, randomUUID + "." + format
        )  # this is temporary!
        # that is the tweak. we have successfully changed the directory!
        if backend == "editly":
            # iterate through all items.
            template = {
                "width": 1920,
                "height": 1080,
                "fast": fast,
                "fps": 60,
                "outPath": output_path,
                "defaults": {"transition": None},
                "clips": [],
            }
            if bgm is not None:
                template.update({"audioFilePath": bgm})
            for elem in previous:
                duration = 3  # default duration
                clip = {
                    "duration": duration,
                    "layers": [],
                }
                layer_durations = []
                for layerElem in elem:
                    layer = None
                    # print(layerElem) # {"item":<item>, "cache": <cache_path>}
                    cachePath = layerElem["cache"]
                    # breakpoint()
                    layerElemItem = layerElem["item"]
                    filepath = layerElemItem.path
                    # what type is this damn media?
                    filetype = getFileType(filepath)
                    if layerElemItem.args.get("backend", "editly") == "editly":
                        if filetype == "video":
                            videoInfo = get_media_info(filepath)
                            endOfVideo = videoInfo["duration"]

                            cutFrom = layerElemItem.args.get("cutFrom", 0)
                            cutTo = layerElemItem.args.get("cutTo", endOfVideo)
                            layerOriginalDuration = cutTo - cutFrom

                            processedFilePath = ffmpegVideoPreProductionFilter(
                                filepath, start=cutFrom, end=cutTo, cachePath=cachePath
                            )
                            # what is this filepath? man how do i handle this?
                            videoFilePath = processedFilePath
                            # get video information!
                            # if processed:
                            # this must be true now.
                            cutFrom = 0
                            cutTo = layerOriginalDuration

                            speed = layerElemItem.args.get("speed", 1)
                            # was wrong.
                            layerDuration = (cutTo - cutFrom) / speed
                            layer_durations.append(layerDuration)
                            mute = layerElemItem.args.get("slient", False)
                            layer = {
                                "type": "video",
                                "path": videoFilePath,
                                "resizeMode": "contain",
                                "cutFrom": cutFrom,
                                "cutTo": cutTo,
                                # that's how we mute it.
                                "mixVolume": 1 - int(mute),
                            }
                            removeKeys = []
                            for key, elem in layer.items():
                                if elem is None:
                                    removeKeys.append(key)
                            for key in removeKeys:
                                del layer[key]
                    if layer is not None:
                        clip["layers"].append(layer)
                    else:
                        raise Exception("NOT IMPLEMENTED LAYER FORMAT:", layerElem)
                maxDuration = max(layer_durations)
                clip["duration"] = maxDuration
                template["clips"].append(clip)
                # then just execute this template, or let's just view it.
            if verbose:
                print("________________editly template________________")
                print(
                    json.dumps(template, ensure_ascii=False, indent=4)
                )  # let's view it elsewhere? or in `less`?
                print("________________editly template________________")
            # breakpoint()
            # return template
            executeEditlyScript(medialangTmpDir, template)
            os.rename(output_path, outputPath)
            return outputPath
