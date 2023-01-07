from pyjom.commons import *


def serializeSRT(srtObj):
    index = srtObj.index
    start = srtObj.start.total_seconds()
    end = srtObj.end.total_seconds()
    content = srtObj.content
    data = {"index": index, "timespan": [start, end], "content": content}
    return data


def medialangFatalError(error_msg, script_file):
    print("Medialang fatal error:", os.path.abspath(script_file))
    print(error_msg)
    os.abort()


medialangTmpDir = "/dev/shm/medialang"


def getTmpMediaName(medialangTmpDir = medialangTmpDir):
    while True:
        uniq_id = str(uuid.uuid4())
        uniq_id = uniq_id.replace("-", "")
        fname = "{}.ts".format(uniq_id)
        fpath = os.path.join(medialangTmpDir, fname) # why no respect to the medialang config!
        if not os.path.exists(fpath):
            return fpath
