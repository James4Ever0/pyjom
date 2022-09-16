from .mediaDetector import *
# assume you not to run many instances at once?
# how to identify same video in a sequence?

def yolov5_Identifier(frame, threshold=0.4,model = "yolov5s"):
    model = configYolov5(model=model)
    # assert to be read from opencv2
    img = cv2_HWC2CHW(frame)

    results = model(img) # pass the image through our model

    df = results.pandas().xyxy[0]
    # print(df)
    data = []
    for _, line in df.iterrows():
        left = (line["xmin"],line["ymin"])
        right = (line["xmax"],line["ymax"])
        confidence = line["confidence"]
        if confidence < threshold:
            continue # skipping threshold too low.
        class_ = line["class"]
        name = line["name"]
        data.append({"location":[left,right],"confidence":confidence,"identity":{"class":class_,"name":name}})
    return data


def yolov5_Detector(mediapaths, model="yolov5s", threshold=0.4, timestep=0.2):
    # any better detectors? deeplearning?
    results = []
    data_key = "yolov5"
    assert model in ["yolov5n","yolov5s","yolov5m","yolov5l","yolov5x","yolov5n6","yolov5s6","yolov5m6","yolov5l6","yolov5x6"] # increase the parameters does not sufficiently improve accuracy.
    keyword = "{}_detector".format(data_key)
    for mediapath in mediapaths:
        print("mediapath:", mediapath)
        mediatype = getFileType(mediapath)
        print("subtitle of mediatype:", mediatype)
        assert mediatype in ["video", "image"]  # gif? anything like that?
        result = {"type": mediatype, data_key: {}}
        config = {"threshold": threshold,"model":model}

        if mediatype == "image":
            data = cv2.imread(mediapath)
            data = keywordDecorator(yolov5_Identifier, **config)(data)
            result[data_key].update({keyword: data})
            result[data_key].update({"config": config})
            # results.append(result)
        else:
            mdata, metadata = videoFrameIterator(
                mediapath,
                data_producer=keywordDecorator(yolov5_Identifier, **config),
                framebatch=1,
                timestep=timestep,
                keyword=keyword,
            )
            metadata.update({"config": config})
            result[data_key][keyword] = mdata
            result[data_key].update(metadata)
        results.append(result)
    return results
