sample = 'hello world'

>>> import pycld2 as cld2
>>> text_content = """"""
_, _, _, detected_language = cld2.detect(text_content,  returnVectors=True)
>>> print(detected_language)
((0, 323, 'FRENCH', 'fr'), (323, 64, 'ENGLISH', 'en'))