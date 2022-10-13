pic_0= 'cat.png'
pic_0_similar = "cat3.png"
pic_1 = "/root/Desktop/works/pyjom/samples/image/dick.png"
from PIL import Image
# >>> import imagehash
# >>> hash = imagehash.average_hash(Image.open
import imagehash

pics = [pic_0, pic_0_similar, pic_1]
hashs = [imagehash.phash(Image.open(pic)) for pic in pics]

dis0 = hashs[0]-hashs[1]
dis1 = hashs[1]-hashs[2]

# 0 24
# 6 24

# well, let's check?
print([type(h) for h in hashs])
breakpoint()
print(dis0, dis1)
# three truth tables.
# 2^4 = 16, total 2*8 digits=16?
