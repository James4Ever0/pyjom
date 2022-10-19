# let's try to make it right.
pic_file = "sample_cover.jpg"
qrcode_file = "MyQRCode1.png"
# we need some font for this.
# font_location = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc" # ttc -> ttf
font_location = "./wqy-microhei0.ttf"

import pixie

font = pixie.read_font(font_location)
font.size=20

text = "Typesetting is the arrangement and composition of text in graphic design and publishing in both digital and traditional medias."
image = pixie.Image(200, 200)
image.fill(pixie.Color(1, 1, 1, 1))

image.fill_text(
    font,
    text,
    bounds = pixie.Vector2(180, 180),
    transform = pixie.translate(10, 10)
)

# print('image type:', type(image))
# 'pixie.pixie.Image'
# hard to say.

image.write_file("text.png")