# use some delogo stuff.
from lazero.program.subprocess import runCommandGetJson
# these two are similar. can be used as threshold.
# aaaa3d8a2eaa1f8a delogo
# aaaa398a2faa5d8a not delogoed.
import os
import imagehash
assert os.path.exists(filepath)
assert os.path.isfile(filepath)
if not os.path.isabs(filepath):
    filepath = os.path.abspath(filepath)
commandLine = ["/root/Desktop/works/pyjom/tests/video_phash_deduplication/videohashes/videohashes-linux","-json",filepath]
myJson = runCommandGetJson(commandLine)
phashString = myJson['phash']
phash = imagehash.