import sys
sys.path.append("/root/Desktop/works/pyjom/tests/skipexception_code_and_continue_resurrection_time_travel_debugging/codemod_redbaron")
from pasta_test import recover_and_rewrite as rar1
from recover_and_rewrite import recover_and_rewrite as rar2

if __name__ == "__main__":
    import os

    # from comby import Comby

    # comby = Comby()
    dirpath = "/root/Desktop/works/pyjom/pyjom"

    def change_file_at_path(path,no_rewrite=False):
        with open(path, "r") as f:
            source_old = f.read()
            if len(source_old) < 20 or "\ndef " not in source_old:
                return
            try:
                source_new = rar1(source_old,no_rewrite=no_rewrite)
            except:
                import traceback
                traceback.print_exc()
                print('pasta failed to process the code at path: %s' % path)
                source_new = rar2(source_old,no_rewrite=no_rewrite)
        with open(path, "w+") as f:
            f.write(source_new)

    pyfiles = []
    import progressbar

    for basedir, dirs, files in os.walk(dirpath):
        for fname in files:
            fpath = os.path.join(basedir, fname)
            if fname.endswith(".py"):
                pyfiles.append(fpath)
                # print(fpath)
    mod = 100
    for pyfile in progressbar.progressbar(pyfiles):
        # if index % mod == 0:
        print("processing file at path: %s" % pyfile)
        change_file_at_path(pyfile,no_rewrite=True)
