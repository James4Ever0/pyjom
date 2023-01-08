from test_commons import *
from pyjom.primitives import *  # this is capitalized.

template_names = ["subtitle_detector.mdl.j2"]
autoArgs = {"subtitle_detector": {"timestep": 0.2}}

wbRev = WeiboPetsReviewer(
    auto=True,
    semiauto=False,
    dummy_auto=False,
    args=autoArgs,
    template_names=template_names,
)
# wbRev.main(skip_review=True) # to test feedback.
wbRev.main()
