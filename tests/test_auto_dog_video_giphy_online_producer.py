# ld_library_path is handled externally using env
from test_commons import *
from pyjom.primitives import *
autoArgs = {
    "subtitle_detector": {"timestep": 0.2}
} 
template_names = ["subtitle_detector.mdl.j2"] 

wbRev = OnlineAutoContentProducer(
    producer_filters={
        "yolov5": {"objects": ["dog", "cat"], "min_time": 2}, # what is this min_time?
        "meta": {
            "type": "video",
            "timelimit": {
                "min": 1,
            },
        },
    },
    template="pets_with_music",
    template_config={
        "music": {
            "filepath": "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3", # these things were not right.
            "lyric_path": "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.lrc",
        },
        "font": "/root/.local/share/fonts/simhei.ttf",
        # "font": "/root/.local/share/fonts/simyou.ttf", # 幼圆可能打不出来
        "policy": {},
        "maxtime": 4,
        "mintime": 2,
        "fast":True, # pass this flag to medialang export engine
    },
    processor_filters={
        "yolov5": ["dog", "cat"],
        "labels": ["dog", "cat"],
        "framedifference_talib_detector": 30,
        "ensure": ["yolov5"],
    }
    # you can also translate funny videos from youtube.
    # dummy_auto=False,
    # args=autoArgs,
    # semiauto=False # i do not want to comment shit.
)

def completeTest():
    wbRev.main()

def partialMedialangRenderTest(medialangScript, verbose=True):
    # copy that script to my dear clipboard please?
    medialangObject = Medialang(script=medialangScript, verbose=verbose)
    result = medialangObject.execute()
    return result

def PMRT_0(scriptFilePath = "", verbose=True):
    with open(scriptFilePath,"r") as f:
        medialangScript = f.read()
    return partialMedialangRenderTest(medialangScript, verbose=verbose)

from contextlib import AbstractContextManager

class tmpdir(AbstractContextManager):
    """Context manager to suppress specified exceptions

    After the exception is suppressed, execution proceeds with the next
    statement following the with statement.

         with suppress(FileNotFoundError):
             os.remove(somefile)
         # Execution still resumes here if the file was already removed
    """

    def __init__(self, path=None):
        assert os.path.isabs(path)
        self._tmpdir = path

    def __enter__(self):
        print("temporary directory: %s" % self._tmpdir)
        if os.path.exists(self._tmpdir): shutil.rmtree(self._tmpdir)
        os.makedirs(self._tmpdir)
        return self._tmpdir

    def __exit__(self, exctype, excinst, exctb):
        # try not to handle exceptions?
        tempdir = self._tmpdir
        print("cleaning tempdir: %s" % tempdir)
        shutil.rmtree(tempdir)
        return False
        
if __name__ == "__main__":
    COMPLETE_TEST = False
    if COMPLETE_TEST:
        completeTest()
    # so we don't have to run it all the time. really?
    else:
        scriptFilePath = "/root/Desktop/works/pyjom/tests/medialang_tests/aef2ab90-6414-4b55-a40e-63014e5648a8.mdl"
        # a special hack
        # import tempfile
        with tmpdir(path="/dev/shm/medialang") as medialangTmpDir:
            print("MEDIALANG SUPER TMPDIR:", medialangTmpDir)
            result = PMRT_0(scriptFilePath, verbose=False)
            editly_outputPath, medialang_item_list = result # this just return none!
            # data -> editly json
            # this output path is modified. we shall change this.
            outPath = editly_outputPath # WE SHALL MUTE IT!
            # print(editly_json.keys())

            print("MEDIA SAVE PATH (MAYBE YOU CAN PLAY IT?):",outPath)
            breakpoint()
            # import json
            # data_array -> input of dot processor? check it out.
            # breakpoint() # what is this?