from comby import Comby
comby = Comby()

# better not to use this!

def rewrite(source_old):
    # match = ':[prefix~$]def :[functionName](:[args]):'
    match = ':[prefix~$]def :[functionName](:[args]):'
    # match = ':[prefix~\n$]def :[functionName](:[args]):'
    rewrite = ':[prefix]\n@reloading\ndef :[functionName](:[args]):'

    source_new = comby.rewrite(source_old, match, rewrite,language='.py')

    if source_new !=source_old:
        source_new = 'from reloading import reloading\n'+source_new
    return source_new

if __name__ == "__main__":
    source_old = open('test2.py','r').read()
    # source_old = open('/root/Desktop/works/pyjom/pyjom/platforms/bilibili/uploader.py','r').read()
    # source_old = open('/root/Desktop/works/pyjom/pyjom/platforms/bilibili/uploader.py','r').read()
    # comby = Comby()

    source_new = rewrite(source_old)
    print(source_new)