background = "setu2.jpg"

ebegging = "ebegging_template.png"

import pixie

bgImage = pixie.read_image(background)
ebImage = pixie.read_image(ebegging)

ratio_0 = 1200 / min(bgImage.width,bgImage.height)

factor = 5
ratio = min(bgImage.width, bgImage.height)/(max(ebImage.width, ebImage.height)*factor)

e_w, e_h = int(ratio*ebImage.width), int(ratio*ebImage.height)
# print(e_w, e_h)
# print(ratio)
# print(bgImage.width, bgImage.height)

ebImage = ebImage.resize(e_w, e_h)
ebImage.apply_opacity(0.5)
t_w, t_h = bgImage.width-e_w, bgImage.height-e_h

bgImage.draw(ebImage,transform = pixie.translate(t_w, t_h))
bgImage.write_file('ebegging_setu_transparent.png')