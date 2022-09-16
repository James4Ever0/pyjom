from test_commons import *
from pyjom.modules.contentReviewer import 

autoArgs = {"subtitle_detector": {"timestep": 0.2},"yolov5_detector":{"model":"yolov5x"}}
template_names = ["yolov5_detector.mdl.j2"]
semiauto=False
dummy_auto=False

filesystemReviewer(
                    auto=True,
                    semiauto=semiauto,
                    dummy_auto=dummy_auto,
                    template_names=template_names,
                    args={'autoArgs':autoArgs},
                )