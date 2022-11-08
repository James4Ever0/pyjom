from recover_and_rewrite import recover_and_rewrite

if __name__ == '__main__':
    import os
    dirpath = "/root/Desktop/works/pyjom/pyjom"
    def change_file_at_path(path):
        with  open(path,'r') as f:
            source_old = f.read()
            source_new = recover_and_rewrite(source_old)
        with open(path,'w') as f:
            f.write(source_new)
    pyfiles = []
    import progressbar
    for basedir, dirs, files in os.walk(dirpath):
        for fname in files:
            fpath = os.path.join(basedir, fname)
            if fname.endswith('.py'):
                pyfiles.append(fpath)
    mod=100
    for index, pyfile in progressbar.progressbar(enumerate(pyfiles)):
        if index % mod == 0:
            print('processing file at path: %s' % pyfile)
            change_file_at_path(pyfile)
