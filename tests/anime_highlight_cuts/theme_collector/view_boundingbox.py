x, y, w, h = [1118.5, 545.5, 1585, 1069]
min_x, min_y = int(x - (w / 2)), int(y - (h / 2))
import cv2

imagePath = ""

image = cv2.imread(imagePath)
p0, p1 = (min_x, min_y), (min_x + w, min_y + h)

cv2.rectangle(image, p0, p1, (0, 255, 0), 3)
cv2.imshow("PIP", image)
