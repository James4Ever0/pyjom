# use what? better use some standard library.
imageBasePath = ""
imagePaths = []
width = 800
half_width = width/2 # either use 1,2,4 images.
textTotalHeight = 300 # either add to top or bottom.

imageIndex=0 # shall be increased on demand.

alphabets = "abcdefghijklmnopqrstuvwxyz"
ALPHABETS = alphabets.upper()
numbers = "0123456789"
from string import punctuation
characterList = list(alphabets+ALPHABETS+numbers+)
getRandomCharacters