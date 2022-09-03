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

test_ffmpeg = False
test_text_detector = True

def getVideoDuration(filePath):

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
    return end


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
    start = 0
    end = getVideoDuration(videoPath)

    if test_text_detector:
        from pyjom.medialang.processors.dotProcessor import detectTextRegionOverTime
        
        regions = detectTextRegionOverTime(videoPath, start, end)
        for region in regions:
            # could be empty here.
            print(region)
            # how to merge continual shits?
            
        # pretty much None currently.
        breakpoint()

    if test_ffmpeg:
        output = ffmpegVideoPreProductionFilter(videoPath, cachePath = cachePath, start=start, end=end, filters=filters, preview=True) # resolution? make it sufficiently low!
        print("ffmpeg pre production filter processing done.")
        print("output location:", output)
        breakpoint()