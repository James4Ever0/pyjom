import sys

import tempfile

def customExceptHook(a,b,c):
    print('ERROR INFO:', a,b,c)
    # <class 'AttributeError'> '_io.BufferedRandom' object has no attribute 'path' <traceback object at 0x7fd6c4325080>
    # it is a traceback object.
    print("context preserved! please take action!")
    # preserved my ass.
    # this won't preserve context in any degree.
    while True:
        i = input('exit? (y for exit)\n').lower()
        if i == 'y':
            break
    print('closing program now!')

sys.excepthook=customExceptHook
import os
with tempfile.NamedTemporaryFile('w+',suffix='123') as f: # no such file now. wtf?
    # print('LOCATION:',dir(f))
    # /tmp/tmp7c5ffugz123
    # still exist?
    f.write('abcdefg')
    f.flush() # write to disk.
    print('LOCATION:',os.path.abspath(f.name))
    breakpoint() # we have the content here.
    maketrouble() # no content here! it fucking triggered the alarm.