testData = """mixed content 我 從來沒想過我
這放蕩的靈魂
不經意間傷了你的心
如果 我們還有可 简体中文在这里 绝对是简体"""

# pip3 install opencc-python-reimplemented
# pip3 install opencc (if you want to)
# import opencc
from opencc import OpenCC # all the same.
cc = OpenCC('t2s')  # convert from Simplified Chinese to Traditional Chinese
# you can also try s2t
# can also set conversion by calling set_conversion
# cc.set_conversion('s2tw')
to_convert = testData
converted = cc.convert(to_convert)
print("CONVERTED: ", converted) # great.
# similar song/bgm label in video/audio -> song fullname -> music platform -> download song with lyrics