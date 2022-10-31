background = "setu.jpg"

ebegging = "ebegging_template.png"

import pixie

bgImage = pixie.read_image(background)
ebImage = pixie.read_image(ebegging)

ratio = min(bgImage.width, bgImage.height)/(max(ebImage.width, bgImage.height))