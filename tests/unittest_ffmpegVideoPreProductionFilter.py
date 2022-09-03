from test_commons import *
from pyjom.medialang.processors.dotProcessor import ffmpegVideoPreProductionFilter
import tempfile
videoPaths = {
    "text":"/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4",
    "logo":"/root/Desktop/works/pyjom/samples/video/LkS8UkiLL.mp4",
    "pip":"/root/Desktop/works/pyjom/samples/video/LiGlReJ4i.mp4",
}
tempDir = '/dev/shm/medialang' # anyway we just want something else...
with tempfile.TemporaryDirectory(prefix = tempDir) as allocatedTmpDir:
    print("Allocated tmpDir:", allocatedTmpDir)
    videoPath
    videoFile = os.path.join(allocatedTmpDir,videoFileName)
    import uuid
    