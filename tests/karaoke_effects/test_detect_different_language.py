sample = 'last friday night 影響包含'

import pycld2 as cld2
text_content = sample
_, _, _, detected_language = cld2.detect(text_content,  returnVectors=True)
print(detected_language) # unknown! fucking shit
# ((0, 323, 'FRENCH', 'fr'), (323, 64, 'ENGLISH', 'en'))

# ((0, 30, 'Unknown', 'un'),)

import cld3

result = cld3.get_frequent_languages(sample,num_langs=3)

print(result)

# what the fuck?

# [LanguagePrediction(language='uz', probability=0.44310665130615234, is_reliable=False, proportion=0.5757575631141663), LanguagePrediction(language='zh', probability=0.9812981486320496, is_reliable=True, proportion=0.42424243688583374)]

print(cld3.get_language('last friday night do it all again this friday night'))

# not very freaking reliable.

import whatlang

whatlang.detect_language('last friday night do it all again this friday night')