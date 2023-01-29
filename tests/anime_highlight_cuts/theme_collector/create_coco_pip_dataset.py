# use what? better use some standard library.
# you must know where you have put all these images.

# TODO: remember to upload dataset creation things to kaggle as separate python scripts and execute it in separate process to prevent memory leaks (hopefully)

import cv2
import numpy as np
import os
from string import punctuation
import random
import itertools


imageBasePath = "/Users/jamesbrown/Desktop/"
imagePaths = [
    "Screen Shot 2023-01-17 at 15.35.29.png"
] * 4  # let's all be the same, for testing.
width = 800
half_width = int(width / 2)  # either use 1,2,4 images.
textTotalHeight = 300  # either add to top or bottom.
marginRatio = 0.1

textOrigin = (30, 30)
fontScale = 1
font = cv2.FONT_HERSHEY_SIMPLEX
fontThickness = 2


imageIndex = 0  # shall be increased on demand.

MAX_COCO_PIP_IMAGE_COUNT = 10000  # well, super huge. is it?

alphabets = "abcdefghijklmnopqrstuvwxyz"
ALPHABETS = alphabets.upper()
numbers = "0123456789"


characterList = list(alphabets + ALPHABETS + numbers + punctuation + " ")

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
colorsNumpyArray = [np.array(color) for color in colors]
colorsWithIndex = [(index, color) for index, color in enumerate(colors)]
# we are not doing this while testing.

# imageFormat = random.choice(imageFormats)
# textFormat = random.choice(textFormats)
# backgroundFormat = random.choice(backgroundFormats)


for imageFormat, textFormat, backgroundFormat in itertools.product(
    imageFormats, textFormats, backgroundFormats
):  # you can use these things to get test output picture names.
    colorDistances = {}
    for imagePath in random.sample(imagePaths, k=imageFormat):
        imageRealPath = os.path.join(imageBasePath, imagePath)
        image = cv2.imread(
            imageRealPath, cv2.IMREAD_COLOR
        )  # BGR? are you sure this is correct?
        averageColor = np.average(image.reshape((-1, 3)), axis=0)
        for index, colorNumpyArray in colorsNumpyArray:
            colorDistances.get(index, []).append(
                np.sum(np.abs(averageColor - colorNumpyArray))
            )
    sortedColorsWithIndex = sorted(
        colorsWithIndex, key=lambda element: -np.sum(colorDistances[element[0]])
    )  # the further the better.

    # sortedColors = [color for _, color in sortedColorsWithIndex]

    ## create background first.
    imageCanvasHeight = half_width if imageFormat == 2 else width
    textCanvasHeight = 0 if textFormat == "none" else textTotalHeight
    backgroundShape = (imageCanvasHeight + textCanvasHeight, width, 3)  # height, width

    backgroundImage = np.zeros(backgroundShape, dtype=np.uint8)

    _, color_main = sortedColorsWithIndex[0]

    # fill background with color_main first.
    backgroundImage[:, :, 0] = color_main[0]
    backgroundImage[:, :, 1] = color_main[1]
    backgroundImage[:, :, 2] = color_main[2]

    if backgroundFormat in ["horizontalStripes", "verticalStripes", "gradients"]:
        _, color_sub = sortedColorsWithIndex[1]
        if backgroundFormat in ["horizontalStripes", "verticalStripes"]:
            stripeCount = random.randint(2, 5)
            if backgroundFormat == "verticalStripes":
                arr = np.linspace(0,,stripeCount+1)
        else:  # gradient!
            ...
    else:  # pure color.
        pass

    ## next, paint text!
    if textFormat != "none":
        ## only calculate text color when needed.
        backgroundAverageColor = np.average(backgroundImage.reshape((-1, 3)), axis=0)
        textColorNumpyArray = sorted(
            colorsNumpyArray,
            key=lambda colorNumpyArray: -np.sum(
                np.abs(backgroundAverageColor - np.array(colorNumpyArray))
            ),
        )[0]
        textColor = textColorNumpyArray.tolist()
        # let's paint it all over the place!
        textContent = getRandomLinesOfCharacters(
            20, 20
        )  # TODO: check if string is **just enough** to fill the background.
        backgroundImage = cv2.putText(
            backgroundImage,
            textContent,
            textOrigin,
            font,
            fontScale,
            textColor,
            fontThickness,
            cv2.LINE_AA,
        )

    ## preview
    previewImageName = f"{imageFormat}_{textFormat}_{backgroundFormat}.png"
    cv2.imshow(previewImageName, backgroundImage)
    cv2.waitKey(0)
