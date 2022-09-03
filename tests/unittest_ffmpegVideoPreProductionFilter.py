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
    from MediaInfo import MediaInfo
    info = MediaInfo(filename = videoPath)
    infoData = info.getInfo()
    # print(infoData)
    # breakpoint()
    defaultWidth = infoData["videoWidth"]
    defaultHeight = infoData["videoHeight"]
    # print(infoData)
    # print(infoData.keys())
    # breakpoint()
    start = 0
    end = float(infoData['videoDuration'])

    maxPixel = 200

    ffmpegVideoPreProductionFilter(videoPath, cachePath = cachePath, start=start, end=end, filters=filters, preview=True) # resolution? make it sufficiently low!