from test_commons import *
from pyjom.modules.topicGenerator import OnlineTopicGenerator
from lazero.utils import sprint
from lazero.network import download
from lazero.filesystem import tmpdir

elem, label = OnlineTopicGenerator()
sprint("LABEL:", label)
# # 'pyjom.commons.OnlineTopicGenerator'
# breakpoint()
path = "/dev/shm/medialang/online_test"
import os

with tmpdir(path=path) as testDir:
    print("TESTDIR:", testDir)
    for asset_id, meta in elem:
        print("X", asset_id, meta)
        url = meta["url"]
        extension = url.split("?")[0].split(".")[-1]
        basename = ".".join([asset_id, extension])
        download_path = os.path.join(path, basename)
        download(url, download_path)
        # X ('sr8jYZVVsCmxddga8w', {'height': 480, 'width': 474, 'url': 'https://media0.giphy.com/media/sr8jYZVVsCmxddga8w/giphy.gif'})
        breakpoint()
