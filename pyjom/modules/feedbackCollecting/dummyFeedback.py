from pyjom.commons import *
from lazero.program.functools import iterateWithTempDirectory # you can also switch to 'AUTO'


@decorator
def dummyFeedback(
    content # i think i need another function decorator for this. really? this will break pattern, for sure. temp files will be missing? so you need some tempdir decorator?
):  # anyway, it is dummy. i don't expect nothing.
    @iterateWithTempDirectory()
    def inner(elem):
        print("from poster:", elem)
        return "pending"
    return inner(elem)