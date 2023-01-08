from test_commons import *
from pyjom.lyrictoolbox import translate
from lazero.utils.logger import sprint

sources = ["are you ok", "are you happy", "are you good", "are you satisfied"]
for source in sources:
    result = translate(
        source, backend="deepl"
    )  # this is cached. no matter what backend you use.
    print("source:", source)
    sprint("result:", result)
