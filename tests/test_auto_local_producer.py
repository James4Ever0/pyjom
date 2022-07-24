from test_commons import *
from pyjom.primitives import *  # this is capitalized.

autoArgs = {"subtitle_detector": {"timestep": 0.2}} # what is this? should't you detect all before production?
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
    reviewerLogs = ["/media/root/help/pyjom/logs/local/1648576077_705094.log", # this is the paddleocr result.
    "/media/root/help/pyjom/logs/local/1652502047_091761.json",# yolov5
    "/media/root/help/pyjom/logs/local/1652856912_480332.json", # framedifference_talib
    ],
    filters={"yolov5":{"objects":["dog","cat"],"min_time":2},"meta":{"timelimit":{"min":1,}}},
    path_replacers=[
        [
            ["/media/root/help/pyjom/samples/",
            "/root/Desktop/works/pyjom/src/samples/",
            "/media/root/help1/pyjom/samples/"
            ],
            "/root/Desktop/works/pyjom/samples/"
        ]
    ]
    # filters={"yolov5":["dog","cat"],"labels":["dog","cat"],"framedifference_talib_detector":30}
    # you can also translate funny videos from youtube.
    # dummy_auto=False,
    # args=autoArgs,
    # template_names=template_names,
    # semiauto=False # i do not want to comment shit.
)

wbRev.main()
