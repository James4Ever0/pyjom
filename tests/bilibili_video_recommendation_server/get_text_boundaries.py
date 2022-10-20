import pixie

text = 'test me please'
export_path = 'detect_text_bounds.png'
image = pixie.Image(200,200)
font_location = "./wqy-microhei0.ttf"

font = pixie.read_font(font_location)
font.size = 20
font.paint.color = pixie.Color(1,1,1,1)

image.fill_text(
    font, text, bounds=pixie.Vector2(180, 180), transform=pixie.translate(10, 10)
)

image.write_file(export_path)

from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()
import cv2

img = cv2.imread(export_path)
# print(img.shape) #(200,200,3)
# exit()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# print(img_gray)

rect = cv2.boundingRect(img_gray)
# fuck?
print(rect)
# (10, 13, 130, 21)
# x,y,w,h?