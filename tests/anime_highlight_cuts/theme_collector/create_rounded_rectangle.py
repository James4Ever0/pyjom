from PIL import Image, ImageDraw
import cv2
import numpy as np


def rectangle():
    image = Image.new("RGB", (800, 400), "black")  # width, height?
    draw = ImageDraw.Draw(image)
    # Draw a regular rectangle
    draw.rectangle((200, 100, 300, 200), fill="white")
    # Draw a rounded rectangle
    draw.rounded_rectangle((50, 50, 150, 150), fill="white", radius=20)
    npArray = np.array(image)  # /255
    # uint8? then float64? great.
    print(npArray)
    print(npArray.shape, npArray.dtype, npArray.max())  # 255?
    cv2.imshow("mask", npArray)
    # maybe we just want "1" instead of "255"
    # divide by 255 then.
    cv2.waitKey(0)


rectangle()
