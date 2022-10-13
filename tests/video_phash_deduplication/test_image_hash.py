pic_0= 'cat.png'
pic_0_similar = "cat2.png"
pic_1 = "/root/Desktop/works/pyjom/samples/image/dick.png"

import imagehash

pics = [pic_0, pic_0_similar, pic_1]
hashs = [ for pic in pics]