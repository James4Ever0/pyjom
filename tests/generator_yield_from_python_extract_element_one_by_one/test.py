from lazero.filesystem.temp import tmpfile
import pathlib
def generator(tempfile):
    with tmpfile(tempfile):
        pathlib.Path(tempfile).touch()
        for index in range(100):
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


if __name__ == "__main__":
    tempfile = "tmp_test"
    myGenerator = generator2(tempfile)
    generator3(myGenerator)  # good.
    # another test on generator, about tempfiles during iteration.
