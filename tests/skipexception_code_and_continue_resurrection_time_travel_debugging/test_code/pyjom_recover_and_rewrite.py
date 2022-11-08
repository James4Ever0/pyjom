from recover_and_rewrite import recover_and_rewrite

if __name__ == '__main__':
    import os
    dirpath = "/root/Desktop/works/pyjom/pyjom"
    def change_file_at_path(path):
        # print('processing file at path: %s' % path)
        with  open(path,'r') as f:
            source_old = f.read()
            source_new = recover_and_rewrite(source_old)
        with open(path,'w') as f:
            f.write(source_new)
    for basedir, dirs, files in os.walk(dirpath):
        for fname in files:
            fpath = os.path.join(basedir, fname)