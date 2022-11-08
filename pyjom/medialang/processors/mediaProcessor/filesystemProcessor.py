from reloading import reloading
from pyjom.medialang.commons import *
import ffmpeg

@reloading
def videoFsProcessor(videoPath,args={},previous = None, medialangTmpDir = medialangTmpDir):
    if args == {}:
        return videoPath
    newVideoPath = getTmpMediaName(medialangTmpDir = medialangTmpDir)
    return newVideoPath

@reloading
def audioFsProcessor(audioPath,args={},previous = None, medialangTmpDir = medialangTmpDir):
    if args == {}:
        return audioPath
    newAudioPath = getTmpMediaName(medialangTmpDir = medialangTmpDir)
    return newAudioPath

@reloading
def imageFsProcessor(imagePath,args={},previous = None, medialangTmpDir = medialangTmpDir):
    if args == {}:
        return imagePath
    newImagePath = getTmpMediaName(medialangTmpDir = medialangTmpDir)
    return newImagePath

@reloading
def fsProcessor(item,previous=None, verbose=True, medialangTmpDir = medialangTmpDir):
    path = item.path # it exists!
    fbase = os.path.basename(path)
    args = item.args
    mediatype = getFileType(fbase) # mediatype not sure yet.
    if verbose:
        print("media path:",path)
        print("media type:",mediatype)
    # handle to ffmpeg.
    mediaFunctions = {"video":videoFsProcessor,"audio":audioFsProcessor,"image":imageFsProcessor}
    data = mediaFunctions[mediatype](path,args=args,previous=previous, medialangTmpDir = medialangTmpDir)
    return data