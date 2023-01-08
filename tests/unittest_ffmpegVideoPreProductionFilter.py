from test_commons import *
from pyjom.medialang.processors.dotProcessor import ffmpegVideoPreProductionFilter
import tempfile

# import MediaInfo
videoPaths = {
    "text": "/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4",
    "logo": "/root/Desktop/works/pyjom/samples/video/LkS8UkiLL.mp4",
    # "pip":"/root/Desktop/works/pyjom/samples/video/LiGlReJ4i.mp4", # najie
    "pip": "/root/Desktop/works/pyjom/samples/video/LiEIfnsvn.mp4",  # double pip
    # 'complete':"/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4"
}
tempDir = "/dev/shm/medialang"  # anyway we just want something else...


test_ffmpeg = True
test_text_detector = False


def getVideoDuration(filePath):

    from MediaInfo import MediaInfo

    info = MediaInfo(filename=videoPath)
    infoData = info.getInfo()
    # print(infoData)
    # breakpoint()
    defaultWidth = infoData["videoWidth"]
    defaultHeight = infoData["videoHeight"]
    # print(infoData)
    # print(infoData.keys())
    # breakpoint()
    start = 0
    end = float(infoData["videoDuration"])
    return end


testSubject = "complete"

with tempfile.TemporaryDirectory(prefix=tempDir) as allocatedTmpDir:
    print("Allocated tmpDir:", allocatedTmpDir)
    if testSubject == "logo":
        videoPath = videoPaths["logo"]
        filters = ["logoRemoval"]  # how the fuck?
    elif testSubject == "text":
        videoPath = videoPaths["text"]
        filters = ["textRemoval"]
    elif testSubject == "pip":
        videoPath = videoPaths["pip"]
        filters = ["pipCrop"]
    elif testSubject == "complete":
        # videoPath = videoPaths['complete']
        # filters = ['pipCrop','textRemoval']
        filters = ["pipCrop", "textRemoval", "logoRemoval"]
    else:
        raise Exception("Unknown testSubject: %s" % testSubject)
    # videoFileName = os.path.basename(videoPath)
    # # we use the full video here? to check if this shit really works?
    # # videoFile = os.path.join(allocatedTmpDir,videoFileName)
    import uuid

    cacheId = str(uuid.uuid4())
    fileExtension = "mp4"
    cacheFileName = ".".join([cacheId, fileExtension])
    cachePath = os.path.join(allocatedTmpDir, cacheFileName)

    # if testSubject == 'pip':
    #     start=5
    #     end=10

    if test_text_detector:
        from pyjom.medialang.processors.dotProcessor import detectTextRegionOverTime

        for key, videoPath in videoPaths.items():
            if testSubject != "complete":
                if key != testSubject:
                    continue
            print("TESTING: %s" % key)

            start = 0
            end = getVideoDuration(videoPath)
            # regions = detectTextRegionOverTime(videoPath, start, end)
            regions = detectTextRegionOverTime(
                videoPath, 10, 20
            )  # now we change the start and end.

            for key, item in regions.items():
                # could be empty here.
                print("KEY:", key)
                print("ITEM:", item)
            # how to merge continual shits?

        # pretty much None currently.
        breakpoint()

    if test_ffmpeg:
        # the logoRemoval filter may make the video unwatchable if too many false positive areas were found.
        for key, videoPath in videoPaths.items():
            if testSubject != "complete":
                if key != testSubject:
                    continue
            print("TESTING: %s" % key)

            start = 0
            end = getVideoDuration(videoPath)

            output = ffmpegVideoPreProductionFilter(
                videoPath,
                cachePath=cachePath,
                start=start,
                end=end,
                filters=filters,
                preview=True,
            )  # resolution? make it sufficiently low!
            print("ffmpeg pre production filter processing done.")
            print("output location:", output)
            breakpoint()
