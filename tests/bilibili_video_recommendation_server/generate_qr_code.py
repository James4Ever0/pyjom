# Importing library
import qrcode

# Encoding data using make() function
def makeAndSaveQrcode(data, save_path, debug=False):
    img = qrcode.make(data)
    if debug:
        print("image type:", type(img))
    img.save(save_path)

# <class 'qrcode.image.pil.PilImage'>
# Saving as an image file
if __name__ == "__main__":
    data="https://b23.tv/DPn1G4p"
    save_path = 'MyQRCode1.png'
    makeAndSaveQrcode(data, save_path)