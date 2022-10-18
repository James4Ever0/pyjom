data="https://b23.tv/DPn1G4p"
# Importing library
import qrcode

# Encoding data using make() function
img = qrcode.make(data)
print("image type:", type(img))
# <class 'qrcode.image.pil.PilImage'>
# Saving as an image file
img.save('MyQRCode1.png')