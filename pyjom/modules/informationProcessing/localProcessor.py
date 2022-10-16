from pyjom.commons import (
    decorator,
    get_media_info,
    json_media_info,
    ffprobe_media_info,
    read_json,
    getTextFileLength,
    multi_replacer,
    append_sublist,
    extract_span,
    convoluted,
    update_subdict,
)

# you may want to remove text.


@decorator
def FilesystemProcessor(info, reviewerLogs, filters={}, path_replacers={}):
    # print("FILESYSTEM_PROCESSOR INTERCEPTED INFO",info)
    # print("REVIEWER LOGS:", reviewerLogs)
    # breakpoint()

    # do not handle meta filters here.
    protocol, files = info  # source paths.

    # print("FILES", files)
    # breakpoint()
    metainfo = {}
    for elem in files:
        _type, path = elem["type"], elem["path"]
        suffix = path.split(".")[-1]
        metaInfo = {"type": _type, "suffix": suffix, "filename": path.split("/")[-1]}
        if _type == "video":
            einfo = json_media_info(path)
            for e in einfo["media"]["track"]:  # might be gif. how to solve this?
                mtype = e["@type"]
                if mtype == "Video":
                    # breakpoint()
                    resolution = {"height": e["Height"], "width": e["Width"]}
                    # color = e["ColorSpace"] # YUV for common video
            info = get_media_info(path)
            # print("INFO OF %s", path)
            # print(info)
            # breakpoint()
            video_duration = info["videoDuration"]
            if "audioDuration" not in info.keys():
                audioInfo = None
            else:
                # audioInfo = {}
                audio_duration = info["audioDuration"]
                # print(info)
                # breakpoint()
                sampleRate = info["audioSamplingRate"]
                channels = info["audioChannel"]
                audioInfo = {
                    "sampleRate": sampleRate,
                    "channels": channels,
                    "duration": audio_duration,
                }
            resolution = {"height": info["videoHeight"], "width": info["videoWidth"]}
            _fps = info["videoFrameRate"]
            metaInfo.update(
                {
                    "fps": _fps,
                    "duration": video_duration,
                    "resolution": resolution,
                    "audio": audioInfo,
                }
            )
        elif _type == "audio":
            info = get_media_info(path)
            duration = info["duration"]
            sampleRate = info["audioSamplingRate"]
            channels = info["audioChannel"]
            metaInfo.update(
                {"sampleRate": sampleRate, "channels": channels, "duration": duration}
            )
        elif _type == "image":  # gif is image. check it out!
            info = json_media_info(path)
            for e in info["media"]["track"]:
                mtype = e["@type"]
                if mtype == "Image":
                    resolution = {"height": e["Height"], "width": e["Width"]}
                    # color = e["ColorSpace"]
            if metaInfo["suffix"].lower() == "gif":
                info = ffprobe_media_info(path)
                for e in info["streams"]:
                    codec_name = e["codec_name"]
                    if codec_name == "gif":
                        duration = e["duration"]
                        _fps = e["avg_frame_rate"]
                        metaInfo.update(
                            {"duration": float(duration), "fps": eval(_fps)}
                        )
            metaInfo.update({"resolution": resolution})
        elif _type == "text":  # are you sure about that?
            metaInfo.update({"length": getTextFileLength(path)})
        metainfo.update({multi_replacer(path, replacer_list=path_replacers): metaInfo})
    # breakpoint()# get meta information from here.
    fileinfo = {}
    for rlog in reviewerLogs:
        print("READING LOG: %s" % rlog)
        content_json = read_json(rlog)
        for elem in content_json:
            review_tuple = elem["review"]["review"]
            filename = review_tuple[0]
            filename = multi_replacer(filename, replacer_list=path_replacers)
            sample_review = review_tuple[1]  # convolution with removed text timespan.
            # print("KEYS DUMP:")
            primarykey = list(sample_review.keys())[0]  # CHECK THIS KEY FIRST.
            # print("PRIMARYKEY:",primarykey)
            primary_sample_content = sample_review[primarykey]
            # print(primary_sample_content) # hide this shit.
            if primarykey == "labels":
                discard = sample_review["discard"]
                if discard:
                    update_subdict(fileinfo, filename, {"discard": True})
                else:
                    if primarykey in filters.keys():
                        if not any(
                            [x in primary_sample_content for x in filters[primarykey]]
                        ):
                            # remove those without the label.
                            continue
                    update_subdict(
                        fileinfo, filename, {"labels": primary_sample_content}
                    )

                    # does it have any filters?
                # then we have a list of labels down here.
                # handle the filters.
            else:
                sample_content_type, secondary_key = primary_sample_content.keys()
                secondary_sample_content = primary_sample_content[secondary_key]
                third_keys = list(secondary_sample_content.keys())
                thirdkey = third_keys[0]
                # print("SecondaryKey:",secondary_key)
                # print("THIRD_KEYS:",third_keys)
                main_array_content = secondary_sample_content[thirdkey]
                if secondary_key == "yolov5":
                    # print("YOLOV5 DETECTED")
                    # get the time step first. or shall we?
                    # breakpoint()
                    identity_dict_array = {}
                    main_time_array = []
                    for frame in main_array_content:
                        _time, _frame, yolov5_detector = (
                            frame["time"],
                            frame["frame"],
                            frame["yolov5_detector"],
                        )
                        main_time_array.append(_time)
                        for detected in yolov5_detector:
                            # ignore the location. we do not need this shit till we somehow want to focus on the shit.
                            confidence = detected[
                                "confidence"
                            ]  # ignore the confidence.
                            confidence_threshold = 0.6
                            if confidence <= confidence_threshold:
                                continue
                            identity = detected["identity"]["name"]
                            append_sublist(identity_dict_array, identity, _time)
                    if secondary_key in filters.keys():
                        if not any(
                            [
                                x in identity_dict_array.keys()
                                for x in filters[secondary_key]
                            ]
                        ):
                            continue  # do not have the dogs.
                    # so check the timespan.
                    # get consecutive ranges of x == 1. use threshold function like int(x>0.5)
                    new_identity_array = {}
                    for t in main_time_array:
                        for k in identity_dict_array.keys():
                            if t in identity_dict_array[k]:
                                # print("APPENDING")
                                append_sublist(new_identity_array, k, 1)
                                # print(new_identity_array[k])
                                # breakpoint()
                            else:
                                append_sublist(new_identity_array, k, 0)
                    # convolution step:
                    # print("NEW IDEITITY ARRAY BEFORE PROCESSING:", new_identity_array)
                    main_time_array += ["FINAL"]  # add the final time
                    for k in new_identity_array.keys():
                        new_identity_array[k] = convoluted(
                            new_identity_array[k], pad=1, k=5
                        )
                        new_identity_array[k] = [
                            int(x > 0.2) for x in new_identity_array[k]
                        ]
                        new_identity_array[k] = extract_span(
                            new_identity_array[k], target=1
                        )  # this is span.
                        # print(new_identity_array[k])
                        # breakpoint()
                        new_identity_array[k] = [
                            (main_time_array[a], main_time_array[b])
                            for a, b in new_identity_array[k]
                        ]
                    # print("NEW IDENTITY SPAN ARRAY:", new_identity_array) # not so sure if the yolov5 detector is not working properly or the confidence threshold is too high.
                    if secondary_key in filters.keys():
                        if not any(
                            [
                                x in new_identity_array.keys()
                                for x in filters[secondary_key]
                            ]
                        ):
                            continue  # double check.
                    timestep = secondary_sample_content["timestep"]
                    result = {
                        "detected_objects_timespan": new_identity_array,
                        "timestep": timestep,
                    }
                    update_subdict(fileinfo, filename, {"yolov5": result})
                    # breakpoint()
                    # TODO: complete the convolutional span extractor.
                    # pass
                elif (
                    secondary_key == "framedifference_talib_detector"
                ):  # this one is detecting the pip. active region.
                    # print("{:*^30}".format("FRAMEDIFFERECE DETECTOR"))
                    # breakpoint()
                    min_frame_threshold = 30
                    if secondary_key in filters.keys():
                        min_frame_threshold = filters[secondary_key]
                    frameborders = []

                    for k in main_array_content.keys():
                        frameborder = main_array_content[k]
                        start, end = frameborder["start"], frameborder["end"]
                        frame_length = end - start
                        if frame_length < min_frame_threshold:
                            continue
                        frameborders.append(frameborder)
                    update_subdict(
                        fileinfo,
                        filename,
                        {"framedifference_talib_detector": frameborders},
                    )

    # finally remove those without filter keys.

    filterKeys = filters.get("ensure", [y for y in filters.keys() if y != "meta"])
    for k in list(fileinfo.keys()):
        # do metainfo extraction.
        # print("CORE PATH")
        fileinfo[k]["meta"] = metainfo[k]
        fileElemKeys = fileinfo[k].keys()
        if fileinfo[k].get("discard", False):
            fileinfo.pop(k)
            continue
        mbool_condition = all([x in fileElemKeys for x in filterKeys])
        # print("CHECKING:",k)
        # print("CONDITION:",mbool_condition)
        # breakpoint()
        if not mbool_condition:
            fileinfo.pop(k)  # why the fuck you pop all of them!
    # print(fileinfo)
    # print("____________FILEINFO DUMP____________")
    # breakpoint()
    return fileinfo
    # fileSystemUrl, fileList = info # I need the processed logs!
    # return {"husky": "cute husky check my youtube"} # this is dummy return!
