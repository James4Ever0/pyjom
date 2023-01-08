from lazero.utils.importers import cv2_custom_build_init

cv2_custom_build_init()
import cv2
import numpy as np

# command used for reading an image from the disk, cv2.imread function is used
imagePath = "/root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png"
# cannot find image without dark/black boundaries.

# use blur detection, both for blur area removal and motion blur detection for key frame sampling/filtering

# tool for finding non-blur based black borders:
# ffmpeg -loop 1 -i /root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png -t 15 -vf cropdetect -f null -

# maybe you can change the seconds to something shorter.

img1 = cv2.imread(imagePath)
# gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
# edges1 = cv2.Canny(gray1,50,150,apertureSize=3)
# blurred = cv2.GaussianBlur(img1, (5, 5), 0)
blurred = cv2.bilateralFilter(img1, 15, 75, 75)
edges1 = cv2.Canny(blurred, 20, 210, apertureSize=3)

cv2.imshow("EDGE", edges1)
cv2.waitKey(0)

lines1 = cv2.HoughLines(edges1, 1, np.pi / 180, 200)  # wtf?
for rho, theta in lines1[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x = a * rho
    y = b * rho
    x_1 = int(x + 1000 * (-b))
    y_1 = int(y + 1000 * (a))
    x_2 = int(x - 1000 * (-b))
    y_2 = int(y - 1000 * (a))
    cv2.line(img1, (x_1, y_1), (x_2, y_2), (0, 0, 255), 2)
# Creation of a GUI window in order to display the image on the screen
cv2.imshow("line detection", img1)
# cv2.waitKey method used for holding the window on screen
cv2.waitKey(0)
cv2.destroyAllWindows()
