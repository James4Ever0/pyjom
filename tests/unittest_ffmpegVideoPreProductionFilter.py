from test_commons import *
from pyjom.medialang.processors.dotProcessor import ffmpegVideoPreProductionFilter
import tempfile
videoPaths = {
    "text":
    "logo":
    "pip":
}
tempDir = '/dev/shm/medialang' # anyway we just want something else...
with tempfile.TemporaryDirectory(prefix = tempDir) as allocatedTmpDir:
    print("Allocated tmpDir:", allocatedTmpDir)
    videoPath
    videoFile = os.path.join(allocatedTmpDir,videoFileName)