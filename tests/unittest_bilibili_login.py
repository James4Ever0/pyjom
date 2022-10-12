test = 2
if test == 1:
    import os
    credpath = "/root/.bilibili_api.json"
    if os.path.exists(credpath):
        os.remove(credpath)

    from test_commons import *

    from pyjom.platforms.bilibili.credentials import getCredentialByDedeUserId, getCredentialViaSMS

    # myvalue = getCredentialViaSMS()
    # print(myvalue)

    val = getCredentialByDedeUserId()
    print(val)
else:
    # you may want to remove database.
    # how the fuck you can do that?
    # not possible. "RETURN OUTSIDE OF FUNCTION"
    def myfunction():
        exec('val= 1234'+';break'*1000000)
    value = myfunction()
    print(value)