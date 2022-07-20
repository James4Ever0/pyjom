from pyjom.commons import *


@decorator
def filesystemFetcher(topic):
    protocol = topic["protocol"]
    path = topic["path"]
    content = []
    for fname in topic["content"]:
        ftype = getLocalFileType(fname)
        content.append({"type": ftype, "path": fname})
    # maybe using this protocol is a good start to pass things around?"
    return "{}://{}".format(protocol, path), content
