from test_commons import *
from pyjom.platforms.bilibili.credentials import getCredentialViaSMS

# myvalue = getCredentialViaSMS()
# print(myvalue)

# how the fuck you can do that?
# not possible. "RETURN OUTSIDE OF FUNCTION"
def myfunction():
    exec('return 1234')

value = myfunction()
print(value)