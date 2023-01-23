#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytesseract

# pytesseract.get_languages(config="")
langs =['eng','chi_sim','chi_tra','jpn']
langCode = "+".join(langs)

picPath = "test_render.png"

output = pytesseract.image_to_string(picPath, lang=langCode)
print("OUTPUT?")
print(output)
# many incorrect results?
