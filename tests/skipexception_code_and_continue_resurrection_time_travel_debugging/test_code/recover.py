from comby import Comby

comby = Comby()
source_old = open('new_test.py','r').read()
kw = 'from reloading import reloading\n'
if source_old.startswith(kw):
    source_old = source_old.lstrip(kw)

match = ':[prefix~$]def :[functionName](:[args]):'
rewrite = ':[prefix]\n@reloading\ndef :[functionName](:[args]):'
source_new = comby.rewrite(source_old, match, rewrite)

print(source_new)