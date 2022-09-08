sample = 'last friday night 影響包含'

import pycld2 as cld2
text_content = sample
_, _, _, detected_language = cld2.detect(text_content,  returnVectors=True)
print(detected_language) # unknown! fucking shit
# ((0, 323, 'FRENCH', 'fr'), (323, 64, 'ENGLISH', 'en'))

import cld3

result = cld3.get_frequent_languages(sample)

print(result)