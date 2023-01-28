# use what? better use some standard library.
imageBasePath = "/Users/jamesbrown/Desktop/"
imagePaths = ["Screen Shot 2023-01-17 at 15.35.29.png"]*4 # let's all be the same, for testing.
width = 800
half_width = width / 2  # either use 1,2,4 images.
textTotalHeight = 300  # either add to top or bottom.
marginRatio = 0.1

imageIndex = 0  # shall be increased on demand.

alphabets = "abcdefghijklmnopqrstuvwxyz"
ALPHABETS = alphabets.upper()
numbers = "0123456789"
import os
from string import punctuation

characterList = list(alphabets + ALPHABETS + numbers + punctuation + " ")
import random

getRandomCharacter = lambda: random.choice(characterList)
getRandomCharacters = lambda charCount: "".join(
    [getRandomCharacter() for _ in range(charCount)]
)
getRandomLinesOfCharacters = lambda lineCount, charCount: "\n".join(
    [getRandomCharacters(charCount) for _ in range(lineCount)]
)

imageFormats = [1, 2, 4]
textFormats = ["up", "down", "none"]
backgroundFormats = ["solidColor", "horizontalStripes", "verticalStripes", "gradients"]
colors = [
    (0, 0, 0),
    (255, 255, 255),
    (0, 0, 192),
    (255, 255, 64),
    (0, 255, 0),
    (0, 0, 255),
    (255, 0, 0),
]

# we are not doing this while testing.

# imageFormat = random.choice(imageFormats)
# textFormat = random.choice(textFormats)
# backgroundFormat = random.choice(backgroundFormats)



for imagePath in random.sample(imagePaths,k=imageFormat):
    image = os.path.join(imageBasePath, imagePath)