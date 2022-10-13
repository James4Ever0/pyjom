# use some delogo stuff.
from lazero.program.subprocess import runCommandGetJson

# these two are similar. can be used as threshold.
# aaaa3d8a2eaa1f8a delogo
# aaaa398a2faa5d8a not delogoed.
# aaaa3c8a2faa5e8a mp4 (very similar to delogoed version)

videoPaths = ["cute_cat_gif.mp4", "cute_cat_gif.gif", "cat_delogo.gif"]


def getVideoPHash(filepath, debug=False):
    import os
    import imagehash

    assert os.path.exists(filepath)
    assert os.path.isfile(filepath)
    if not os.path.isabs(filepath):
        filepath = os.path.abspath(filepath)
    commandLine = [
        "/root/Desktop/works/pyjom/tests/video_phash_deduplication/videohashes/videohashes-linux",
        "-json",
        filepath,
    ]
    success,myJson = runCommandGetJson(commandLine, debug=debug)
    if not success:
        return
    print(myJson, type(myJson))
    breakpoint()
    phashString = myJson["phash"]
    phash = imagehash.hex_to_hash(phashString)
    if debug:
        print("FILEPATH: %s" % filepath)
        print(myJson)
        print("PHASH: ", phash)
    return phash


hashs = [getVideoPHash(filepath) for filepath in videoPaths]


dis0 = hashs[0] - hashs[1]  # small
dis1 = hashs[1] - hashs[2]  # big
dis2 = hashs[0] - hashs[2]  # big

print(dis0, dis1, dis2)
