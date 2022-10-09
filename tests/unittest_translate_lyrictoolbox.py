from test_commons import *
from pyjom.lyrictoolbox import translate
from lazero.utils.logger import sprint
sources = ['are you ok']
for source in sources:
    result = translate(source, backend='baidu')
    print('source:',source)
    sprint('result:',result)