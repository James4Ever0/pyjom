testData = """mixed content 我 從來沒想過我
這放蕩的靈魂
不經意間傷了你的心
如果 我們還有可 简体中文在这里 绝对是简体"""

import pyopencc
CN2TW = pyopencc.OpenCC('zhs2zhtw_vp.ini').convert

if __name__ == '__main__':
  print(CN2TW("中国鼠标软件打印机"))