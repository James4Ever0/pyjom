x,y,w,h=[1118.5,       545.5,        1585 ,       1069]
min_x, min_y =x-(w/2), y-(h/2)
import cv2
imagePath=""

image = cv2.imread(imagePath)
cv2.rectangle()
cv2.imshow("PIP",image)