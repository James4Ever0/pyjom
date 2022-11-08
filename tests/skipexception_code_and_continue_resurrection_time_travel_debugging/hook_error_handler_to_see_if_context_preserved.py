# 
# import sys

# i can assure that not a single 'reloading' decorator has been added to my code manually yet.

# from basic import on_error_resume_next, err

# on_error_resume_next()
import tempfile

# def customExceptHook(a,b,c):
#     print('ERROR INFO:', a,b,c)
#     # <class 'AttributeError'> '_io.BufferedRandom' object has no attribute 'path' <traceback object at 0x7fd6c4325080>
#     # it is a traceback object.
#     print("context preserved! please take action!")
#     # preserved my ass.
#     # this won't preserve context in any degree.
#     while True:
#         i = input('exit? (y for exit)\n').lower()
#         if i == 'y':
#             break
#     print('closing program now!')

# sys.excepthook=customExceptHook
import os

# add reloading to all these files? are you sure?

# no support for block statements yet.
from reloadr import autoreload

@autoreload
def makeTrouble():
    return 'success!'

def someFunction():
    with tempfile.NamedTemporaryFile('w+',suffix='123') as f: # no such file now. wtf?
        # print('LOCATION:',dir(f))
        # /tmp/tmp7c5ffugz123
        # still exist?
        f.write('abcdefg')
        f.flush() # write to disk.
        print('LOCATION:',os.path.abspath(f.name))
        print('has file?', os.path.exists(f.name)) # debugpy is nice.
        # breakpoint() # we have the content here.
        # this exception is caught, handled, but still recognized by the damn debugger.
        try: # this must be directly in that context.
            maketrouble() # no content here! it fucking triggered the alarm.
        except:
            mCode=None
            while True:
                try:
                    mCode = input("remedy>>> ")
                    if mCode == 'return':
                        return
                    elif mCode.startswith('return '):
                        val = eval(mCode.replace('return ',''))
                        return val
                    else:
                        exec(mCode)
                except:
                    import traceback
                    traceback.print_exc()
                    print('trouble while executing code:', mCode)
        print("won't have problem.")
    return 'myValue'

from reloading import reloading

@reloading
def anotherFunction():
    # raise Exception('but just another shit!')
    # it does not hook the function.
    return 'yes please'

def mFunction():
    while True:
        try:
            val= anotherFunction()
            return val
        except:
            import traceback
            traceback.print_exc()
            print('please modify your code')
            while True:
                i = input('done? (y for done)\n').lower()
                if i == 'y':
                    break

import progressbar

import time

def main():
    print('please wait...')
    for _ in progressbar.progressbar(range(5)):
        time.sleep(1)

    val = anotherFunction()
    # val = mFunction()
    print('value returned:', val) # it cannot restart the function actually raises the exception!

if __name__ == "__main__":
    main()