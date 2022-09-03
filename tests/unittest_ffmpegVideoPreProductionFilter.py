from test_commons import *
from pyjom.medialang.processors.dotProcessor import ffmpegVideoPreProductionFilter
import tempfile
# import MediaInfo
videoPaths = {
    "text":"/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4",
    "logo":"/root/Desktop/works/pyjom/samples/video/LkS8UkiLL.mp4",
    "pip":"/root/Desktop/works/pyjom/samples/video/LiGlReJ4i.mp4",
}
tempDir = '/dev/shm/medialang' # anyway we just want something else...

def getPreviewPixels(defaultWidth, defaultHeight, maxPixel):
    mList = [defaultWidth, defaultHeight]
    # if defaultWidth < defaultHeight:
    #     reverseFlag = True
    maxDim = max(mList)
    shrinkRatio = maxPixel/maxDim
    getRounded = lambda num, rounder: (num//rounder)*rounder
    newFrameWork = [getRounded(x*shrinkRatio,4) for x in mList]
    return newFrameWork[0], newFrameWork[1]

with tempfile.TemporaryDirectory(prefix = tempDir) as allocatedTmpDir:
    print("Allocated tmpDir:", allocatedTmpDir)
    videoPath = videoPaths['text']
    filters = ['textRemoval']
    videoFileName = os.path.basename(videoPath)
    # we use the full video here? to check if this shit really works?
    # videoFile = os.path.join(allocatedTmpDir,videoFileName)
    import uuid
    cacheId = str(uuid.uuid4())
    fileExtension = videoFileName.split(".")[-1]
    cacheFileName = ".".join([cacheId,fileExtension])
    cachePath = os.path.join(allocatedTmpDir,cacheFileName)


    ffmpegVideoPreProductionFilter(videoPath, cachePath = cachePath, start=start, end=end, filters=filters, preview=True) # resolution? make it sufficiently low!