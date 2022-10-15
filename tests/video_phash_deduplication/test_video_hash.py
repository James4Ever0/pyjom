# use some delogo stuff.
from lazero.program.subprocess import runCommandGetJson

# these two are similar. can be used as threshold.
# aaaa3d8a2eaa1f8a delogo
# aaaa398a2faa5d8a not delogoed.
# aaaa3c8a2faa5e8a mp4 (very similar to delogoed version)

def getVideoPHash(filepath,debug=False, timeout=100):
    import os
    import imagehash
    assert os.path.exists(filepath)
    assert os.path.isfile(filepath)
    if not os.path.isabs(filepath):
        filepath = os.path.abspath(filepath)
    commandLine = [
        "videohashes", # installed in path.
        # "/root/Desktop/works/pyjom/tests/video_phash_deduplication/videohashes/videohashes-linux",
        "-json",
        filepath,
    ]
    success, myJson = runCommandGetJson(commandLine, debug=debug, timeout=timeout)
    if debug:
        print("SUCCESS?", success)
        print(myJson, type(myJson))
    if not success:
        return
    # breakpoint()
    phashString = myJson["phash"]
    phash = imagehash.hex_to_hash(phashString)
    if debug:
        print("FILEPATH: %s" % filepath)
        print(myJson)
        print("PHASH:", phash)
    # if withDuration:
    #     duration = myJson["duration"]
    #     return duration, phash
    # duration is inaccurate
    return phash

if __name__ == "__main__":
    videoPaths = [
        "cute_cat_gif.mp4",
        "cute_cat_gif.gif",
        "cat_delogo.gif",
        "/root/Desktop/works/pyjom/samples/video/dog_with_large_text.gif",
    ]

    hashs = [getVideoPHash(filepath,debug=True) for filepath in videoPaths]

    dis0 = hashs[0] - hashs[1]  # small
    dis1 = hashs[1] - hashs[2]  # big
    dis2 = hashs[0] - hashs[2]  # big
    dis3 = hashs[0] - hashs[3]  # big

    print(dis0, dis1, dis2, dis3)

    # 4 4 4
    # strange. why?
    # 4 4 4 42
    # huge difference.
    # what value do you decide to be duplicate?
    # phash < 7 (really?)

    # so how do we run this test?