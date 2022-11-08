from reloading import reloading
from pyjom.commons import *


@decorator
@reloading
def dummyFetcher(topic):
    # maybe using this protocol is a good start to pass things around?"
    return "randomprotocol://randomcontent", {"husky": {"video": "<cute huskies>"}}
