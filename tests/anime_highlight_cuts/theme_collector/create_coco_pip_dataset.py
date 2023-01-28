# use what? better use some standard library.
imageBasePath = "/Users/jamesbrown/Desktop/"
imagePaths = [
    "Screen Shot 2023-01-17 at 15.35.29.png"
] * 4  # let's all be the same, for testing.
width = 800
half_width = int(width / 2) # either use 1,2,4 images.
textTotalHeight = 300  # either add to top or bottom.
marginRatio = 0.1

imageIndex = 0  # shall be increased on demand.

alphabets = "abcdefghijklmnopqrstuvwxyz"
ALPHABETS = alphabets.upper()
numbers = "0123456789"
import os
from string import punctuation

import cv2

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
colorsWithIndex = [(index, color) for index, color in enumerate(colors)]
# we are not doing this while testing.

# imageFormat = random.choice(imageFormats)
# textFormat = random.choice(textFormats)
# backgroundFormat = random.choice(backgroundFormats)

import itertools
import numpy as np

for imageFormat, textFormat, backgroundFormat in itertools.product(
    imageFormats, textFormats, backgroundFormats
):
    colorDistances = {}
    for imagePath in random.sample(imagePaths, k=imageFormat):
        imageRealPath = os.path.join(imageBasePath, imagePath)
        image = cv2.imread(
            imageRealPath, cv2.IMREAD_COLOR
        )  # BGR? are you sure this is correct?
        averageColor = np.average(image.reshape((-1, 3)), axis=0)
        for index, color in colors:
            colorDistances.get(index, []).append(
                np.sum(np.abs(averageColor - np.array(color)))
            )
    sortedColorsWithIndex = list(
        sorted(
            colorsWithIndex, key=lambda element: -np.sum(colorDistances[element[0]])
        )  # the further the better.
    )
    sortedColors = [color for _, color in sortedColorsWithIndex]

    ## create background first.
    imageCanvasHeight = half_width if imageFormat == 2 else width
    textCanvasHeight = 0 if textFormat == "none" else textTotalHeight
    backgroundShape = (imageCanvasHeight + textCanvasHeight, width,3)  # height, width
    backgroundImage = np.zeros(backgroundShape,dtype=np.uint8)
