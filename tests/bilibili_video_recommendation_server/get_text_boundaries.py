import pixie

text = 'test me please'
export_path = 'detect_text_bounds.png'
image = pixie.Image(200,200)
font_location = "./wqy-microhei0.ttf"

font = pixie.read_font(font_location)
font.size = 20


image.fill_text(
    font, text, bounds=pixie.Vector2(180, 180), transform=pixie.translate(10, 10)
)

image.write_file(export_path)

from lazero.utils.importers import cv2_custom_build_init
cv2_custom_build_init()
import cv2

img = cv2.imread(export_path)
print(img.shape)
exit()
img = cv2.cvtColor(img, cv2.COLOR)

rects = cv2.boundingRect(img)
print(rects)