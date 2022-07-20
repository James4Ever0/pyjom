from pyjom.commons import *
import os


@decorator
def filesystemTopicGenerator(filepath=None, dirpath=None, recursive=False):
    mfilelist = []
    protocol = None
    path = getHostname() + "@"
    if filepath is not None:
        assert os.path.isfile(filepath)
        mpath = os.path.abspath(filepath)
        protocol = "file"
        path += mpath
        mfilelist.append(mpath)
    else:
        assert dirpath is not None
        assert os.path.isdir(dirpath)
        dirpath = os.path.abspath(dirpath)
        path += dirpath
        if recursive:
            protocol = "dir_recursive"
            for _, _, files in os.walk(dirpath):
                for fname in files:
                    fpath = os.path.join(dirpath, fname)
                    if os.path.isfile(fpath):
                        # mpath = os.path.abspath(fpath)
                        mfilelist.append(fpath)
        else:
            protocol = "dir"
            mfiles = os.listdir(dirpath)
            for fname in mfiles:
                fpath = os.path.join(dirpath, fname)
                if os.path.isfile(fpath):
                    # mpath = os.path.abspath(fpath)
                    mfilelist.append(fpath)
    return {"protocol": protocol, "path": path, "content": mfilelist}
