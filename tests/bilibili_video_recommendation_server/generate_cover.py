# let's try to make it right.
pic_file = "sample_cover.jpg"
qrcode_file = "MyQRCode1.png"
# we need some font for this.
# font_location = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc" # ttc -> ttf
font_location = "./wqy-microhei0.ttf"

import pixie

font = pixie.read_font(font_location)
font.size=20

text = "中文能够显示么 超出了字符边缘能不能显示 Typesetting is the arrangement and composition of text in graphic design and publishing in both digital and traditional medias."
# 可以显示 但是边缘的字符需要被注意到 看看是不是超出了边界
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

path = pixie.Path()
path.rounded_rect(0,0, 100, 100, 25, 25, 25, 25)
# how to use mask?

mask = pixie.Mask(100,100) # must match mask size?
mask.fill_path(path)

picture = pixie.read_image("sample_cover.jpg")
# we need to reshape this.
width, height = 100,100
picture = picture.resize(width, height) # recommend to do this in pyjom.imagetoolbox since that will be safer.
picture.mask_draw(mask)
# transform=pixie.translate(10,10)

# image.draw(picture,transform=transform)
image.draw(picture)
# image.draw(picture,transform=transform)

image.write_file("text.png")