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

textOrigin = (0, 30)
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
getRandomLinesOfCharacters = lambda lineCount, charCount: "\r".join(
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


def get_gradient_2d(start, stop, width, height, is_horizontal):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T


def get_gradient_3d(width, height, start_list, stop_list, is_horizontal_list):
    result = np.zeros((height, width, len(start_list)), dtype=np.float64)
    for i, (start, stop, is_horizontal) in enumerate(
        zip(start_list, stop_list, is_horizontal_list)
    ):
        result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)
    return result.astype(np.uint8)


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
        for index, colorNumpyArray in enumerate(colorsNumpyArray):
            colorDistances[index] = colorDistances.get(index, []) + [
                np.sum(np.abs(averageColor - colorNumpyArray))
            ]
    sortedColorsWithIndex = sorted(
        colorsWithIndex, key=lambda element: -np.sum(colorDistances[element[0]])
    )  # the further the better.

    # sortedColors = [color for _, color in sortedColorsWithIndex]

    ## create background first.
    imageCanvasHeight = half_width if imageFormat == 2 else width
    textCanvasHeight = 0 if textFormat == "none" else textTotalHeight
    backgroundShape = (imageCanvasHeight + textCanvasHeight, width, 3)  # height, width

    _, color_main = sortedColorsWithIndex[0]

    if backgroundFormat in ["horizontalStripes", "verticalStripes", "gradients"]:
        # fill background with color_main first.

        _, color_sub = sortedColorsWithIndex[1]
        if backgroundFormat in ["horizontalStripes", "verticalStripes"]:

            backgroundImage = np.zeros(backgroundShape, dtype=np.uint8)
            backgroundImage[:, :, 0] = color_main[0]
            backgroundImage[:, :, 1] = color_main[1]
            backgroundImage[:, :, 2] = color_main[2]

            stripeCount = random.randint(2, 5)
            if backgroundFormat == "verticalStripes":  # slice width
                arr = np.linspace(0, backgroundShape[1], stripeCount + 1)
                for width_start, width_end in [
                    (int(arr[i]), int(arr[i + 1]))
                    for i in range(stripeCount)
                    if i % 2 == 1
                ]:
                    backgroundImage[:, width_start:width_end, 0] = color_sub[0]
                    backgroundImage[:, width_start:width_end, 1] = color_sub[1]
                    backgroundImage[:, width_start:width_end, 2] = color_sub[2]
            else:  # horizontal. slice height.
                arr = np.linspace(0, backgroundShape[0], stripeCount + 1)

                for height_start, height_end in [
                    (int(arr[i]), int(arr[i + 1]))
                    for i in range(stripeCount)
                    if i % 2 == 1
                ]:
                    backgroundImage[height_start:height_end, :, 0] = color_sub[0]
                    backgroundImage[height_start:height_end, :, 1] = color_sub[1]
                    backgroundImage[height_start:height_end, :, 2] = color_sub[2]
        else:  # gradient!
            is_horizontal = [False, False, False]
            is_horizontal[random.randint(0, 2)] = True
            backgroundImage = get_gradient_3d(
                backgroundShape[1],
                backgroundShape[0],
                color_main,
                color_sub,
                is_horizontal,
            )
    else:  # pure color.
        backgroundImage = np.zeros(backgroundShape, dtype=np.uint8)
        backgroundImage[:, :, 0] = color_main[0]
        backgroundImage[:, :, 1] = color_main[1]
        backgroundImage[:, :, 2] = color_main[2]

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
        textShift = 40
        # TODO: check if string is **just enough** to fill the background.
        for textLineIndex in range(
            int((backgroundShape[0] / (textTotalHeight + width)) * 27)
        ):
            textContent = getRandomCharacters(50)
            backgroundImage = cv2.putText(
                backgroundImage,
                textContent,
                (textOrigin[0], textOrigin[1] + textShift * textLineIndex),
                font,
                fontScale,
                textColor,
                fontThickness,
                cv2.LINE_AA,
            )

    ## put pictures!
    imageCanvasShape = (imageCanvasHeight,width,3)
    imageMask = np.zeros()

    ## preview
    previewImageName = f"{imageFormat}_{textFormat}_{backgroundFormat}.png"
    cv2.imshow(previewImageName, backgroundImage)
    cv2.waitKey(0)
