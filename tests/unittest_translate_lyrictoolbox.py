from test_commons import *
from pyjom.lyrictoolbox import translate
sources = ['are you ok']
for source in sources:
    result = translate, backend='deepl')
    print('source:',source)
    print('result:',result)