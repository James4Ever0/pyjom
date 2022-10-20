# let's try to make it right.
pic_file = "sample_cover.jpg"
qrcode_file = "MyQRCode1.png"
# we need some font for this.
# font_location = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc" # ttc -> ttf
font_location = "./wqy-microhei0.ttf"

import pixie

font = pixie.read_font(font_location)
font.size = 20

text = "中文能够显示么 超出了字符边缘能不能显示 Typesetting is the arrangement and composition of text in graphic design and publishing in both digital and traditional medias."
# 可以显示 但是边缘的字符需要被注意到 看看是不是超出了边界

image = pixie.Image(200, 200)
image.fill(pixie.Color(1, 1, 1, 1))

image.fill_text(
    font, text, bounds=pixie.Vector2(180, 180), transform=pixie.translate(10, 10)
)

# print('image type:', type(image))
# 'pixie.pixie.Image'
# hard to say.

path = pixie.Path()
path.rounded_rect(0, 0, 100, 100, 25, 25, 25, 25)
# how to use mask?
cover_width, cover_height = 100, 100
mask = pixie.Mask(cover_width, cover_height)  # must match mask size?
mask.fill_path(path)

picture = pixie.read_image(pic_file)
# we need to reshape this.
picture = picture.resize(
    cover_width, cover_height
)  # recommend to do this in pyjom.imagetoolbox since that will be safer.
picture.mask_draw(mask)
transform = pixie.translate(50, 50)

qrcode_width = qrcode_height = 50

qrcode_image = pixie.read_image(qrcode_file)
qrcode_image = qrcode_image.resize(qrcode_width, qrcode_height)
qrcode_transform = pixie.translate(150, 150)


image.draw(picture, transform=transform)
# image.draw(picture)
# image.draw(picture,transform=transform)
image.draw(qrcode_image, transform=qrcode_transform)

# now we try to reverse engineer that thing.

# not only we need to create ads, we need to modify ads on the fly.

# detect qr code and replace the code with ours.

# first of all, the picture needs to be big.


avatar_path = "up_image.jpg"
up_name = "J4D"

avatar_width, avatar_height = 50, 50
path2 = pixie.Path()
path2.circle(25, 25, 25)
mask2 = pixie.Mask(avatar_width, avatar_height)
mask2.fill_path(path2)
avatar = pixie.read_image(avatar_path)
avatar = avatar.resize(avatar_width, avatar_height)
avatar.mask_draw(mask2)
a_transform = pixie.translate(25, 25)
image.draw(avatar, a_transform)


font2 = pixie.read_font(font_location)
font2.size = 40
font2.paint.color = pixie.Color(0, 0.5, 0.953125, 1)
val = image.fill_text(font2, up_name, transform=pixie.translate(25 + 50, 20))
# print('VAL',val) # NONE

path3 = pixie.Path()
path3.rounded_rect(0,0,100,50,10,10,10,10)

paint = pixie.Paint(pixie.SOLID_PAINT)
paint.color = pixie.parse_color("#FC427B")
transform3 = pixie.translate(25+50+50, 20)
image.fill_path(path3, paint, transform3)

label_text = "UP主"


font3 = pixie.read_font(font_location)
font3.size = 30
font3.paint.color = pixie.Color(1,1,1, 1)
image.fill_text(
    font3, label_text, transform=pixie.translate(25 + 50 + 50, 20)
)  # where should i put the thing?

bilibili_logo_path = "bilibili_transparent.png"

bilibili_logo = pixie.read_image(bilibili_logo_path)
bilibili_logo = bilibili_logo.resize(50,100)
image.draw(bilibili_logo)

play_button_path = 'play_button.png'
play_button = pixie.read_image(play_button_path)
play_button = play_button.resize(50,50)
t4 = pixie.translate(100,100)
image.draw(play_button, t4)
# so no more masking here. we need some png magic.

image.write_file("ad_0.png")