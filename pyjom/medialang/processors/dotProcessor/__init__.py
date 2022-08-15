from pyjom.medialang.processors.dotProcessor.jsonProcessor import *
from pyjom.medialang.processors.dotProcessor.videoProcessor import *
from pyjom.commons import keywordDecorator

dotProcessors = {".json":dotJsonProcessor, ".mp4": keywordDecorator(dotVideoProcessor,format="mp4")}