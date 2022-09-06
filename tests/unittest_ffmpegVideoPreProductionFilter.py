from test_commons import *
from pyjom.medialang.processors.dotProcessor import ffmpegVideoPreProductionFilter
import tempfile
# import MediaInfo
videoPaths = {
    "text":"/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4",
    "logo":"/root/Desktop/works/pyjom/samples/video/LkS8UkiLL.mp4",
    # "pip":"/root/Desktop/works/pyjom/samples/video/LiGlReJ4i.mp4", # najie
    'pip':'/root/Desktop/works/pyjom/samples/video/LiEIfnsvn.mp4' # double pip
    'complete'
}
tempDir = '/dev/shm/medialang' # anyway we just want something else...


test_ffmpeg = True
test_text_detector = False

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

testSubject = 'pip'

with tempfile.TemporaryDirectory(prefix = tempDir) as allocatedTmpDir:
    print("Allocated tmpDir:", allocatedTmpDir)
    if testSubject == 'logo':
        videoPath = videoPaths['logo']
        filters = ['logoRemoval'] # how the fuck?
    elif testSubject == 'text':
        videoPath = videoPaths['text']
        filters = ['textRemoval']
    elif testSubject == 'pip':
        videoPath = videoPaths['pip']
        filters = ['pipCrop']
    else:
        raise Exception("Unknown testSubject: %s" % testSubject)
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
    # if testSubject == 'pip':
    #     start=5
    #     end=10

    if test_text_detector:
        from pyjom.medialang.processors.dotProcessor import detectTextRegionOverTime
        
        # regions = detectTextRegionOverTime(videoPath, start, end)
        regions = detectTextRegionOverTime(videoPath, 10, 20) # now we change the start and end.
        
        for key, item in regions.items():
            # could be empty here.
            print("KEY:",key)
            print("ITEM:",item)
            # how to merge continual shits?

        # pretty much None currently.
        breakpoint()

    if test_ffmpeg:
        output = ffmpegVideoPreProductionFilter(videoPath, cachePath = cachePath, start=start, end=end, filters=filters, preview=True) # resolution? make it sufficiently low!
        print("ffmpeg pre production filter processing done.")
        print("output location:", output)
        breakpoint()