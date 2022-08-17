from pyjom.medialang.functions import *
from pyjom.medialang.commons import *
import tempfile

def dotVideoProcessor(item, previous, format=None, verbose=True):
    # print("DOTVIDEO ARGS:", item, previous, format)
    # this item is the video output config, medialang item.
    itemArgs = item.args
    if format is None:
        format = item.path.split(".")[-1]
    backend = itemArgs.get(
        "backend", "editly"
    )  # so all things will be assumed to put directly into editly render json, unless explicitly specified under other medialang or other backend and need to be resolved into media file format before rendering. sure?
    fast = itemArgs.get("fast", True)
    bgm = itemArgs.get("bgm", None)
    print(format, backend, fast, bgm)

    # the "previous" is the clips, was fucked, filled with non-existant intermediate mpegts files, but no source was out there.
    # this is initially decided to output mp4, however you might want to decorate it.
    if verbose:
        print("_________INSIDE DOT VIDEO PROCESSOR_________")
        print("ITEM:", item)
        print("PREVIOUS:", previous)
        print("_________INSIDE DOT VIDEO PROCESSOR_________")
    with tempfile.TemporaryDirectory(prefix="/dev/shm/medialang") as tmpdirname: # maybe you should take care of the directory prefix?
        tmpdirname = os.path.abspath(tmpdirname)
        print('created temporary directory', tmpdirname)
        randomUUID = str(uuid.uuid4())
        output_path = os.path.join(tmpdirname,randomUUID+"."+format)
        if backend == "editly":
            # iterate through all items.
            template = {
                "width": 1920,
                "height": 1080,
                "fps": 60,
                "outPath": output_path,
                "defaults": {"transition": None},
                "clips": [],
            }
            if bgm is not None:
                template.update({"audioFilePath": bgm})
            for elem in previous:
                duration = 3 # default duration
                clip = {
                    "duration": duration,
                    "layers": [
                    ],
                }
                for layerElem in elem:
                    layer = None
                    # print(layerElem)
                    # breakpoint()
                    filepath = layerElem.path
                    # what type is this damn media?
                    filetype = getFileType(filepath)
                    if filetype == "video":
                        videoFilePath = filepath
                        cutFrom = layerElem.args.get("cutFrom",None)
                        cutTo = layerElem.args.get("cutTo",None)
                        layer= {
                                "type": "video",
                                "path": videoFilePath,
                                "resizeMode": "contain",
                                "cutFrom": cutFrom,
                                "cutTo": cutTo,
                            }
                        removeKeys = []
                        for key, elem in layer.items():
                            if elem is None:
                                removeKeys.append(key)
                        for key in removeKeys: del layer[key]
                    if layer is not None:
                        clip.append(layer)
                    else: raise Exception("NOT IMPLEMENTED LAYER FORMAT:", layerElem)
                template.clips.append(clip)
                # then just execute this template, or let's just view it.