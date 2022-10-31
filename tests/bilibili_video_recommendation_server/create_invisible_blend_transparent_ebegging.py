background = "setu.jpg"

ebegging = "ebegging_template.png"

import pixie

bgImage = pixie.read_image(background)
ebImage = pixie.read_image(ebegging)

ratio = min(bgImage.width, bgImage.height)/(max(ebImage.width, bgImage.height)*4)

e_w, e_h = int(ratio*ebImage.width), int(ratio*ebImage.height)

ebImage = ebImage.resize(e_w, e_h)

bgImage.draw(ebImage,transform = pixie.translate(10, 10) )