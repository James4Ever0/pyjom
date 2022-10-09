from lazero.filesystem.temp import tmpfile
import pathlib

import os

def checkFileExists(filePath, debug=False):
    result = os.path.exists(filePath)
    if debug:
        print('exists?', result)

def generator(tempfile):
    # for index in range(12): # 0 to 11 means 12
    for index in range(11): # what if it is 11? -> StopIteration and shit get cleaned.
        with tmpfile(tempfile):
            pathlib.Path(tempfile).touch()
            yield index


def generator2(tempfile):
    yield from generator(tempfile)  # this is to simplifying the process of iteration.


def iterator(lambdaFunction, tempfile):
    for _ in range(4):
        result = lambdaFunction()
        print(result) # cleaned after next FAILED iteration, which is what we need the most.
        checkFileExists(tempfile, debug=True)
        # cleaning after 'close' or next iteration.


def generator3(myGenerator, tempfile):
    getNextNumber = lambda: myGenerator.__next__()
    for _ in range(3):
        iterator(getNextNumber, tempfile)
        print("_" * 30)


if __name__ == "__main__":
    tempfile = "tmp_test"
    if os.path.exists(tempfile):
        os.remove(tempfile)
    myGenerator = generator2(tempfile)
    print(type(myGenerator))
    breakpoint()
    generator3(myGenerator, tempfile)  # good.
    # not over yet.
    checkFileExists(tempfile, debug=True)
    myGenerator.close() # choose to close this so you would get this result.
    checkFileExists(tempfile, debug=True)
    # another test on generator, about tempfiles during iteration.
