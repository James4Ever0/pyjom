# ld_library_path is handled externally using env
from test_commons import *
from pyjom.primitives import *
from pyjom.medialang.core import *

autoArgs = {"subtitle_detector": {"timestep": 0.2}}
template_names = ["subtitle_detector.mdl.j2"]

# warning: if you want to post it, you must review, and you must not use 'fast' mode aka preview.

# you want musictoolbox? well shit...
# just because you want download music.
# also where are the places for 'video/audio/voice/artwork' generation?
# maybe it is not the time to use such kind of things... you know the ram best.
from pyjom.platforms.bilibili.postMetadata import 

wbRev = OnlineAutoContentProducer(
    source="giphy",
    template="pets_with_music_online",
    postMetadataGenerator=postMetadataGenerator,
    template_configs=[
        {
            "music": {
                "filepath": "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3",  # these things were not right.
                "lyric_path": "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.lrc",  ## you can choose not to pass the lyric_path anyway. also format different than .lrc is on the way?
            },
            "font": "/root/.local/share/fonts/simhei.ttf",
            # "font": "/root/.local/share/fonts/simyou.ttf", # 幼圆可能打不出来
            "policy": {},
            "maxtime": 7.8,
            "mintime": 2,  # we've write this shit!
            "fast": True,  # pass this flag to medialang export engine
            "render_ass": True,
            # also determine how to translate the lyrics, whether to translate or not.
            "translate": True,  # default: False
            # are you sure you want to use deepl? this is hard to configure. especially the goddamn proxy.
            # you can simply implement the method to cofigure and test ping for websites in lazero library so we can share the same code.
            # or you can borrow code from the web. some clash manager library for python.
            "translate_method": "deepl",  # default: baidu
            # damn cold for this mac!
        }
    ],
    # you can also translate funny videos from youtube.
    # dummy_auto=False,
    # args=autoArgs,
    # semiauto=False # i do not want to comment shit.
)


def completeTest():
    wbRev.main()


def partialMedialangRenderTest(medialangScript, medialangTmpdir, verbose=True):
    # copy that script to my dear clipboard please?
    medialangObject = Medialang(
        script=medialangScript, verbose=verbose, medialangTmpdir=medialangTmpdir
    )
    result = medialangObject.execute()
    return result


def PMRT_0(scriptFilePath, medialangTmpdir, verbose=True):
    with open(scriptFilePath, "r") as f:
        medialangScript = f.read()
    return partialMedialangRenderTest(medialangScript, medialangTmpdir, verbose=verbose)


from lazero.filesystem import tmpdir

# from contextlib import AbstractContextManager

# class tmpdir(AbstractContextManager):
#     """Context manager to suppress specified exceptions

#     After the exception is suppressed, execution proceeds with the next
#     statement following the with statement.

#          with suppress(FileNotFoundError):
#              os.remove(somefile)
#          # Execution still resumes here if the file was already removed
#     """

#     def __init__(self, path=None):
#         assert os.path.isabs(path)
#         self._tmpdir = path

#     def __enter__(self):
#         print("temporary directory: %s" % self._tmpdir)
#         if os.path.exists(self._tmpdir): shutil.rmtree(self._tmpdir)
#         os.makedirs(self._tmpdir)
#         return self._tmpdir

#     def __exit__(self, exctype, excinst, exctb):
#         # try not to handle exceptions?
#         tempdir = self._tmpdir
#         print("cleaning tempdir: %s" % tempdir)
#         shutil.rmtree(tempdir)
#         return False
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--partial", action="store_true", default=False)
    args = parser.parse_args()

    COMPLETE_TEST = not args.partial
    if COMPLETE_TEST:
        completeTest()
    # so we don't have to run it all the time. really?
    else:
        # scriptFilePath = "/root/Desktop/works/pyjom/tests/medialang_tests/aef2ab90-6414-4b55-a40e-63014e5648a8.mdl"
        # set this scriptFilePath to something else.
        scriptFilePath = "/root/Desktop/works/pyjom/samples/medialang/dog_cat_test.mdl"
        # a special hack
        # import tempfile
        with tmpdir(path="/dev/shm/medialang") as medialangTmpdir:
            print(
                "MEDIALANG SUPER TMPDIR:", medialangTmpdir
            )  # as some sort of protection.
            # /dev/shm/medialang/<randomString>/<randomUUID>.mp4 -> /dev/shm/medialang/<randomUUID>.mp4
            result = PMRT_0(scriptFilePath, medialangTmpdir, verbose=False)
            editly_outputPath, medialang_item_list = result  # this just return none!
            # data -> editly json
            # this output path is modified. we shall change this.
            outPath = editly_outputPath  # WE SHALL MUTE IT!
            # print(editly_json.keys())

            print("MEDIA SAVE PATH (MAYBE YOU CAN PLAY IT?):", outPath)
            breakpoint()
            # import json
            # data_array -> input of dot processor? check it out.
            # breakpoint() # what is this?
