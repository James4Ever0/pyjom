from reloading import reloading
from pyjom.commons import decorator


@decorator
@reloading
def dummyProcessor(info):
    return {"husky": "cute husky check my youtube"}
