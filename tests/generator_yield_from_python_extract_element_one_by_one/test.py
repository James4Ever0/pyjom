from lazero.filesystem.temp import tmpfile
import pathlib
def generator(tempfile):
    with tmpfile(tempfile):
        pathlib.Path(tempfile).touch()
        for index in range(100): # zero to 11
            yield index


def generator2(tempfile):
    yield from generator(tempfile)  # this is to simplifying the process of iteration.


def iterator(lambdaFunction):
    for _ in range(4):
        result = lambdaFunction()
        print(result)


def generator3(myGenerator):
    getNextNumber = lambda: myGenerator.__next__()
    for _ in range(3):
        iterator(getNextNumber)
        print("_" * 30)

import os

def checkFileExists(filePath, debug=False):
    result = os.path.exists(filePath)
    if debug:
        print('exists?', result)

if __name__ == "__main__":
    tempfile = "tmp_test"
    if os.path.exists(tempfile):
        os.remove(tempfile)
    myGenerator = generator2(tempfile)
    generator3(myGenerator)  # good.
    # not over yet.
    checkFileExists(tempfile, debug=True)
    myGenerator.close() # choose to close this so you would get this result.
    checkFileExists(tempfile, debug=True)
    # another test on generator, about tempfiles during iteration.
