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
from pyjom.platforms.bilibili.postMetadata import getBilibiliPostMetadataForDogCat

# decide to do this in sync.
# preconfigure the dog_or_cat value.

dog_or_cat = random.choice(["dog", "cat"])  # strange.
# we need preconfigured things.
bgmCacheSetName = "bilibili_cached_bgm_set"
postMetadataGenerator = getBilibiliPostMetadataForDogCat(
    dog_or_cat=dog_or_cat,
    bgmCacheSetName=bgmCacheSetName,
    bgmCacheAutoPurge=True,  # autopurge bgm, not sure we are using the latest bgm!
)  # metadata you can fetch from database, maybe you can preprocess this.
postMetadataGenerator.__next__()  # for getting some bgm, just in case.
# really?
metaTopics = {
    "dog": {
        "static": [["dog", "puppy"]],
        "dynamic": [
            ["samoyed", "husky", "teddy", "chiwawa"],
            ["meme"],
            ["funny", "cute", "love"],
        ],
    },
    "cat": {
        "static": [["cat", "kitten"]],
        "dynamic": [["purr", "paws", "meme"], ["funny", "cute"]],
    },
}

# when use 'complete test' it stops iterating.
# maybe because the last one is a generator. goddamn it.
def cleanupMedialangTmpdir():
    tmpdirPath = "/dev/shm/medialang"
    files_and_dirs = os.listdir(tmpdirPath)
    for f in files_and_dirs:
        fpath = os.path.join(tmpdirPath, f)
        if os.path.isfile(fpath):
            os.remove(fpath)


from pyjom.commons import getRedisCachedSet
from pyjom.musictoolbox import neteaseMusic


def makeTemplateConfigsGenerator():
    NMClient = neteaseMusic()
    while True:
        # download one music, either from hottest songs or from fetched music list.
        # even if we search for the name, we will randomly choose the song to avoid problems.
        # you must download the file in a fixed location.
        while True:
            bgmCacheSet = getRedisCachedSet(bgmCacheSetName)
            keywords = random.choice(list(bgmCacheSet)).strip()
            if len(keywords) > 0:
                (
                    music_content,
                    music_format,
                ), lyric_string = NMClient.getMusicAndLyricWithKeywords(keywords,similar=random.choice([True, False]))
                if music_content is not None:
                    break
        with tempfile.NamedTemporaryFile(
            "wb", suffix=".{}".format(music_format)
        ) as music_file:
            with tempfile.NamedTemporaryFile("w+", suffix=".lrc") as lyric_file:
                musicFilePath, lyricPath = music_file.name, lyric_file.name
                music_file.write(music_content)
                music_file.seek(0)
                if lyric_string is not None:
                    lyric_file.write(lyric_string)
                    lyric_file.seek(0)
                else:
                    lyricPath = None
                data = {
                    "debug": True,  # we need to preview this video.
                    # use generator instead.
                    "music": {
                        "filepath": musicFilePath,  # these things were not right.
                        # how to get this music file? by bgm search?
                        # "filepath": "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.mp3",  # these things were not right.
                        "lyric_path": lyricPath,  ## you can choose not to pass the lyric_path anyway. also format different than .lrc is on the way?
                    },
                    "font": "/root/.local/share/fonts/simhei.ttf",
                    # "font": "/root/.local/share/fonts/simyou.ttf", # 幼圆可能打不出来
                    "policy": {},
                    "maxtime": 7.8,
                    "mintime": 2,  # we've write this shit!
                    "render_ass": lyricPath is not None,
                    # also determine how to translate the lyrics, whether to translate or not.
                    "translate": lyricPath is not None,  # default: False
                    # are you sure you want to use deepl? this is hard to configure. especially the goddamn proxy.
                    # you can simply implement the method to cofigure and test ping for websites in lazero library so we can share the same code.
                    # or you can borrow code from the web. some clash manager library for python.
                    "translate_method": "deepl",  # default: baidu
                    # damn cold for this mac!
                    "ass_template_configs": {},
                    "assStyleConfig": {},
                }
                yield data


templateConfigsGenerator = makeTemplateConfigsGenerator()
wbRev = OnlineAutoContentProducer(
    afterPosting=cleanupMedialangTmpdir,
    source="giphy",
    fast=False,
    metaTopic=metaTopics[dog_or_cat],
    # fast= True,  # pass this flag to medialang export engine
    template="pets_with_music_online",
    postMetadataGenerator=postMetadataGenerator,
    template_configs=templateConfigsGenerator,
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
    # print('args.partial:', args.partial)
    # breakpoint()

    COMPLETE_TEST = not args.partial
    if COMPLETE_TEST:
        completeTest()
    # so we don't have to run it all the time. really?
    else:
        # scriptFilePath = "/root/Desktop/works/pyjom/tests/medialang_tests/aef2ab90-6414-4b55-a40e-63014e5648a8.mdl"
        # set this scriptFilePath to something else.
        scriptFilePath = "/root/Desktop/works/pyjom/samples/medialang/dog_cat_test_nofast.mdl"  # make it real, not preview.
        # scriptFilePath = "/root/Desktop/works/pyjom/samples/medialang/dog_cat_test.mdl" # make it real, not preview.
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
