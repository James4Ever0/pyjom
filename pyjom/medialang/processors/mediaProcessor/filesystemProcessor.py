from pyjom.medialang.commons import *
import ffmpeg

def videoFsProcessor(videoPath,args={},previous = None):
    if args == {}:
        return videoPath
    newVideoPath = getTmpMediaName()
    return newVideoPath

def audioFsProcessor(audioPath,args={},previous = None):
    if args == {}:
        return audioPath
    newAudioPath = getTmpMediaName()
    return newAudioPath

def imageFsProcessor(imagePath,args={},previous = None):
    if args == {}:
        return imagePath
    newImagePath = getTmpMediaName()
    return newImagePath

def fsProcessor(item,previous=None, verbose=True):
    path = item.path # it exists!
    fbase = os.path.basename(path)
    args = item.args
    mediatype = getFileType(fbase) # mediatype not sure yet.
        print("media path:",path)
        print("media type:",mediatype)
    # handle to ffmpeg.
    mediaFunctions = {"video":videoFsProcessor,"audio":audioFsProcessor,"image":imageFsProcessor}
    data = mediaFunctions[mediatype](path,args=args,previous=previous)
    return data