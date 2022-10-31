background = "setu.jpg"

ebegging = "ebegging_template.png"

import pixie

bgImage = pixie.read_image(background)
ebImage = pixie.read_image(ebegging)

ratio = min(bgImage.width, bgImage.height)/(max(ebImage.width, ebImage.height)*4)

e_w, e_h = int(ratio*ebImage.width), int(ratio*ebImage.height)
# print(e_w, e_h)
# print(ratio)
# print(bgImage.width, bgImage.height)

ebImage = ebImage.resize(e_w, e_h)
t_w, t_h = bgImage.width-e_w, bgImage.height-e_h

bgImage.draw(ebImage,transform = pixie.translate(t_w, t_h),blend_mode=pixie.DARKEN_BLEND)
bgImage.write_file('ebegging_setu_transparent.png')