# 
# import sys

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



# no support for block statements yet.

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
        try:
            maketrouble() # no content here! it fucking triggered the alarm.
        except:
            while True:
                try:
                    mCode = input("remedy>>> ")
                    if mCode.startswith('return '):
                        val = eval(mCode.replace('return ',''))
                        return val
                    else:
                except:
        print("won't have problem.")
    return 'myValue'

val = someFunction()
print('value returned:', val)