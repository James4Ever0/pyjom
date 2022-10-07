from pyjom.commons import *
from pyjom.modules.contentProducing.producerTemplates import getProducerTemplate


def FilesystemInfoFilter(processed_info, filters={}):
    # this is just standard filter logic...
    filtered_info = {}
    # print(processed_info)
    # print("PROCESSED_INFO")
    # breakpoint()
    for file_path, file_info in processed_info.items():
        # abandon_flag = False
        # ensure all filter names must be inside
        abandon_flag = [
            filter_name in file_info.keys() for filter_name in filters.keys()
        ]
        # print(file_info.keys(), filters.keys(), abandon_flag)
        # breakpoint()
        abandon_flag = not all(abandon_flag)  # what is this?
        metadata = file_info[
            "meta"
        ]  # is that necessary? do we want to make any filter with it?
        if abandon_flag:
            continue  # abandon those without qualificaton info.
        cuts = {}
        for filter_name, filter_content in filters.items():
            if filter_name == "meta":
                required_type = filter_content.get("type")
                media_type = metadata["type"]
                abandon_flag = not required_type == media_type
                # breakpoint()
                if abandon_flag:
                    break
            elif filter_name == "labels":
                required, at_leasts = filter_content.get(
                    "required", []
                ), filter_content.get("at_leasts", [])
                required_flag = all([x in file_info[filter_name] for x in required])
                if required_flag:
                    # check all at_leasts.
                    for at_least_number, elements in at_leasts:
                        assert at_least_number > 0
                        assert type(at_least_number) == int
                        assert type(elements) == list
                        assert len(elements) > 0
                        hit_count = sum(
                            [int(x in file_info[filter_name]) for x in elements]
                        )
                        if hit_count < at_least_number:
                            abandon_flag = True
                            break
                    if abandon_flag:
                        break
                else:
                    abandon_flag = True
                    break
            elif filter_name == "yolov5":
                # if type(filter_content) == list:
                #     breakpoint()
                objects, min_time = filter_content.get(
                    "objects", None
                ), filter_content.get("min_time", 2)
                assert objects != None
                assert min_time > 0
                DOT = file_info[filter_name]["detected_objects_timespan"]
                detected_objects = list(DOT.keys())
                abandon_flag = any([x in objects for x in detected_objects])
                # what is this?
                # breakpoint()
                if not abandon_flag:
                    break
                avaliable_cuts = {}
                for detected_object, timespans in DOT.items():
                    if detected_object not in objects:
                        continue
                    for timespan in timespans:
                        stop, start = timespan[1], timespan[0]
                        if stop == "FINAL":
                            stop = metadata[
                                "duration"
                            ]  # do we need to modify the "FINAL" into acturally digits?
                            timespan = (start, stop)  # do this anyway.
                        timespan_length = stop - start
                        if timespan_length < min_time:
                            continue
                        avaliable_cuts.update(
                            {
                                detected_object: avaliable_cuts.get(detected_object, [])
                                + [timespan]
                            }
                        )
                # collect avaliable cuts.
                cuts.update({filter_name: avaliable_cuts})
                # filter out required durations.
            elif filter_name == "framedifference_talib_detector":
                size_limit, ratio_limit, duration_limit = (
                    filter_content.get("size_limit", 0.2),
                    filter_content.get("ratio_limit", 0.3),
                    filter_content.get("duration_limit", 3),
                )
                avaliable_cuts = []
                for framework in file_info[filter_name]:
                    [[up_x, up_y], [down_x, down_y]] = framework["coords"]
                    frame_width, frame_height = down_x - up_x, down_y - up_y
                    area = (down_x - up_x) * (down_y - up_y)
                    height, width = (
                        metadata["resolution"]["height"],
                        metadata["resolution"]["width"],
                    )
                    total_area = height * width
                    size = area / total_area
                    if size < size_limit:
                        continue
                    ratio = min(frame_width, frame_height) / max(
                        frame_width, frame_height
                    )
                    if ratio < ratio_limit:
                        continue
                    start, end = framework["start"], framework["end"]
                    if end == "FINAL":
                        end = metadata["duration"]
                    duration = end - start
                    if duration < duration_limit:
                        continue
                    # now append your cuts. are they overlapping?
                    framework2 = {
                        "coords": framework["coords"],
                        "timespan": (start, end),
                    }
                    avaliable_cuts.append(framework2)
                cuts.update({filter_name: avaliable_cuts})
            if abandon_flag: # is this duplicated?
                break
        # print(cuts)
        # print("CUTS:")
        filtered_info.update({file_path: cuts})
        # breakpoint()
        # # what the fuck? # #
        # if abandon_flag:
        #     continue  # abandon those without qualification info.
        # # what the fuck? # #
        # breakpoint()
    return filtered_info


@decorator
def FilesystemProducer(
    processed_info,
    filters={},
    template=None,
    template_config={},
):
    # print(processed_info) # why we only have one single goddamn path?
    # breakpoint()
    filtered_info = FilesystemInfoFilter(processed_info, filters=filters)

    template_function = getProducerTemplate(template)

    meta_info = {
        k: processed_info[k]["meta"] for k in processed_info.keys()
    }  # so there is no additional "meta" key.
    # print(filtered_info)  # empty! shit.
    # print(meta_info)
    # breakpoint()

    output = template_function(filtered_info, meta_info, config=template_config)
    # you need to handle the title and something all over this freaking place.
    # must be ready for posting.
    return output
