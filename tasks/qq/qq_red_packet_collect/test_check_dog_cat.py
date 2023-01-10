from adtools import checkIsCatOrDogImage

image_url = "http://gchat.qpic.cn/gchatpic_new/3318506826/205569604-2534335053-7D3B7BA4B3476AD210837D8C86F2E8DA/0?vuin=917521610&term=255&pictype=0"

r= checkIsCatOrDogImage(image_url)
print("RESULT?")
threshold = 0.4
import rich
rich.print(r)
r= checkIsCatOrDogImage(image_url)
r= checkIsCatOrDogImage(image_url)


# for species in r:
#     name = species['identity']
#     if name in ['cat','dog']:
#         conf = species['confidence']
#         if conf > threshold:
#             return name
