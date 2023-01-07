from pyjom.commons import *
from typing import Literal
from lazero.network import download
from lazero.filesystem import tmpdir

@decorator
def OnlineFetcher(
    infoList,
    source: Literal["giphy"] = "giphy",
    frame_size_filter: dict = {
        "width": {"min": 150, "max": 1000},
        "height": {"min": 150, "max": 1000},
    },
    tempdir="/dev/shm/medialang/online",
    threads=20,
    # threads=-0.5,
    use_multithread=True,
    timeout=120
):
    # how do you chain this shit up?

    assert os.path.isabs(tempdir)
    with tmpdir(path=tempdir) as TD:
        assert os.path.isdir(tempdir)
        assert os.path.exists(tempdir)
        for info in infoList:  # generator most likely
            if source == "giphy":
                (source_id, frameMeta) = info
                width, height = frameMeta["width"], frameMeta["height"]
                asset_id = "video_[{}_{}]_[{}x{}]".format(source, source_id, width, height)
                flag = frameSizeFilter(frameMeta, frame_size_filter)
                if flag:
                    # this time it is selected.
                    url = frameMeta["url"]
                    extension = url.split("?")[0].split(".")[-1]
                    basename = ".".join([asset_id, extension])
                    download_path = os.path.join(tempdir, basename)
                    try:
                        result = download(
                            url,
                            download_path,
                            threads=threads,
                            size_filter={"min": 0.4, "max": 50},
                            use_multithread=use_multithread,
                            timeout=timeout
                        )
                        if result:
                            yield source_id, download_path
                        else:
                            print("not downloading source:", source_id)
                            print("skipping:", frameMeta)
                            # print("____WTF IS GOING ON WITH THE DOWNLOADER?____")
                            # breakpoint()
                    except:
                        import traceback
                        traceback.print_exc()
                        print("error fetching assets from giphy")
