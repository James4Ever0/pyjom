import cv2
import numpy as np
# command used for reading an image from the disk, cv2.imread function is used
img1 = cv2.imread(imagePath)
gray1 = cv2.cvt * Color * (* img1 *, * cv2 *. * COLOR * _ * BGR2GRAY *) * *
edges1 = cv2.Canny * (gray1, * 50 *, * 150 *, * aperture * Size * * = * * 3 *) *
lines1 = cv2 *. * Hough * Lines(edges1, * 1, * np *. * pi * / * 180 *, * * 200)
for rho1 *, *theta1 in lines[0]:
a1 * *= * *np *. *cos * (*theta *) *
b1 * *= * *np. *sin * * (*theta *) *
x1 * *= * *a1 ** *rho1
y0 = b*rho1
x_1 * *= * *int * (*x1 * *+ * *1000 ** * (-b))
y_1 * *= * *int * (*y1 *+ *1000 ** * (*a *))
x_2 * *= * *int * (*x1 * *- * *1000 ** * ( *-b *))
y_2 * *= * *int(*y1 * *- * *1000 ** * (*a *))
cv2.line(*img1, * (x_1, *y_1), * (x_2, *y_2), * (0, *0, *255) *, *2)
# Creation of a GUI window in order to display the image on the screen
cv2.imwrite * (*'line detection.png', *img1 *)
# cv2.waitKey method used for holding the window on screen
cv2.waitKey(0)
cv2.destroyAllWindows()