from test_commons import *
from pyjom.primitives import *  # this is capitalized.

autoArgs = {
    "subtitle_detector": {"timestep": 0.2}
}  # what is this? should't you detect all before production?
# autoArgs = {"subtitle_detector": {"timestep": 0.2},"yolov5_detector":{"model":"yolov5x"}}
template_names = ["subtitle_detector.mdl.j2"] # test ocr entities first.
# template_names = ["yolov5_detector.mdl.j2"]

# template_names = ["framediff_detector.mdl.j2"]

# seems cudnn is causing trouble?
# CuDNN Version 降到7.6试试，这个问题是环境问题引起的
# https://pypi.tuna.tsinghua.edu.cn/packages/a4/1f/56dddeb4794137e3f824476ead29806d60a5d5fc20adba9f4d7ca5899900/paddlepaddle_gpu-2.2.2-cp39-cp39-manylinux1_x86_64.whl
# from pip._internal.cli.main
# we have modified the pip downloader.

wbRev = FilesystemAutoContentProducer(
    dirpath="./samples/video/",
    reviewerLogs=[
        "/root/Desktop/works/pyjom/logs/local/1648576077_705094.log",  # this is the paddleocr result.
        "/root/Desktop/works/pyjom/logs/local/1652502047_091761.json",  # yolov5
        "/root/Desktop/works/pyjom/logs/local/1652856912_480332.json",  # framedifference_talib
    ],
    producer_filters={
        "yolov5": {"objects": ["dog", "cat"], "min_time": 2},
        "meta": {
            "type": "video",
            "timelimit": {
                "min": 1,
            },
        },
    },
    path_replacers=[
        [
            [
                "/media/root/help/pyjom/samples/",
                "/media/root/parrot/pyjom/samples/",
                "/media/root/parrot1/pyjom/samples/", # new location of sample media files.
                "/root/Desktop/works/pyjom/src/samples/",
                "/media/root/help1/pyjom/samples/",
            ],
            "/root/Desktop/works/pyjom/samples/",
        ]
    ],
    template="pets_with_music",
    template_config={
        "music": {
            "filepath": "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3", # these things were not right.
            "lyric_path": "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.lrc",
        },
        "font": "/root/.local/share/fonts/simhei.ttf",
        # "font": "/root/.local/share/fonts/simyou.ttf", # 幼圆可能打不出来
        "policy": {},
        "maxtime": 3,
        "mintime": 1,
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
    medialangObject.execute()

def PMRT_0(scriptFilePath = "", verbose=True):
    with open(scriptFilePath,"r") as f:
        medialangScript = f.read()
    partialMedialangRenderTest(medialangScript, verbose=verbose)

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
        pass

    def __exit__(self, exctype, excinst, exctb):
        # try not to handle exceptions?
        tempdir = self._tmpdir
        print("cleaning tempdir: %s" % tempdir)
        shutil.rmtree(tempdir)
        
if __name__ == "__main__":
    # completeTest()
    # so we don't have to run it all the time. really?
    scriptFilePath = "/root/Desktop/works/pyjom/tests/medialang_tests/aef2ab90-6414-4b55-a40e-63014e5648a8.mdl"
    # a special hack
    import tempfile
    with tmpdir(path="/dev/shm/medialang") as medialangTmpDir:
        print("MEDIALANG SUPER TMPDIR:", medialangTmpDir)
        result = PMRT_0(scriptFilePath, verbose=False)
        data, data_array = result
        # data -> editly json
        # data_array -> input of dot processor? check it out.
        breakpoint()