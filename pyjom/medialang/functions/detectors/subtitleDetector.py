from .mediaDetector import *
from .entityDetector import ocrEntityDetector

def getPaddleOCR(mediapath, lang="ch",use_angle_cls=True,cls=True,rec=True):
    ocr = configOCR(use_angle_cls=use_angle_cls,cls=cls,rec=rec, lang=lang)
    # print(mediapath)
    # breakpoint()
    result = ocr.ocr(mediapath,cls=cls,rec=rec)
    # print(result)
    # breakpoint()
    return result


def stablePaddleOCR(mediapath, lang="ch"):
    data = getPaddleOCR(mediapath, lang=lang)
    for ind, element in enumerate(data):
        certainty = element[1][1]
        # print("certainty:",certainty)
        data[ind][1] = (element[1][0], float(certainty))  # fix the float32 error.
        # what is the fetched shit anyway?
    return data


def mediaSubtitleDetector(
    mediapaths,
    videocr=False,
    timestep=0.5,
    videocr_config={"lang": "chi_sim+eng", "sim_threshold": 70, "conf_threshold": 65},
):
    # it must be video/image.
    # we detect shit not to remove shit.
    # this is separated.
    results = []
    data_key = "subtitle_result"
    for mediapath in mediapaths:
        print("mediapath:", mediapath)
        mediatype = getFileType(mediapath)
        print("subtitle of mediatype:", mediatype)
        assert mediatype in ["video", "image"]
        result = {"type": mediatype, data_key: {}}
        if mediatype == "image":
            data = getPaddleOCR(mediapath)
            result[data_key].update({"paddleocr": data})
            # each line per sentence, coordinates.
        else:
            if videocr:
                config = videocr_config
                data = get_subtitles(
                    mediapath, **config
                )  # what is the speed of this? also the quality?
                data = srt.parse(data)
                data = [serializeSRT(x) for x in data]
                result[data_key].update({"videocr": data})
                result[data_key]["config"] = config
            else:
                keyword = "paddleocr" # we will try to merge alike ones.
                mdata, metadata = videoFrameIterator(
                    mediapath,
                    data_producer=stablePaddleOCR, 
                    timestep=timestep,
                    keyword=keyword,
                )
                # we should process the mdata. alter it and change it.
                # mdata = ocrEntityDetector(mdata) # we enable this step later.
                result[data_key][keyword] = mdata
                result[data_key].update(metadata)
                # what is this frame?
            # use traditional things.
        results.append(result)
    return results
