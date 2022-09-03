from test_commons import *
from pyjom.medialang.processors.dotProcessor import ffmpegVideoPreProductionFilter
import tempfile

tempDir = '/dev/shm/medialang' # 
with tempfile.TemporaryDirectory()