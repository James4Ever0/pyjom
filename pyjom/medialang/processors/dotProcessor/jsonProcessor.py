from pyjom.medialang.functions import *
from pyjom.medialang.commons import *


def dotJsonProcessor(item, previous, verbose=True, medialangTmpDir="/dev/shm/medialang/"):
    # must contain something.
    args = item.args
    processorName = args["processor"]
    processor = getMedialangFunction(processorName)
    if processor is None:
        medialangFatalError("processor {} not found.".format(processorName), __file__)
    print("Using JSON processor:", processorName)
    args.pop("processor")
    # breakpoint()
    output = keywordDecorator(processor, **args)(previous)  # what is this shit?
    return output
