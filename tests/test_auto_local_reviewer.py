from test_commons import *
from pyjom.primitives import *  # this is capitalized.

# autoArgs = {"subtitle_detector": {"timestep": 0.2}} # not work for boundary works.
# autoArgs = {"subtitle_detector": {"timestep": 0.2},"yolov5_detector":{"model":"yolov5x"}}
# template_names = ["subtitle_detector.mdl.j2"] # test ocr entities first.
# template_names = ["yolov5_detector.mdl.j2"]
autoArgs = {
    "frameborder_detector": {
        "model": "huffline_horizontal_vertical",
        "config": {"includeBoundaryLines": True},
    }
}
# autoArgs={"frameborder_detector":{"model":"framedifference_talib","config":{}}}
template_names = ["frameborder_detector.mdl.j2"]
# template_names = ["framediff_detector.mdl.j2"]

# seems cudnn is causing trouble?
# CuDNN Version 降到7.6试试，这个问题是环境问题引起的
# https://pypi.tuna.tsinghua.edu.cn/packages/a4/1f/56dddeb4794137e3f824476ead29806d60a5d5fc20adba9f4d7ca5899900/paddlepaddle_gpu-2.2.2-cp39-cp39-manylinux1_x86_64.whl
# from pip._internal.cli.main
# we have modified the pip downloader.

wbRev = FilesystemAutoContentReviewer(
    dirpath="./samples/video/",
    dummy_auto=False,
    args=autoArgs,
    template_names=template_names,
    semiauto=False,  # i do not want to comment shit.
)

wbRev.main()
