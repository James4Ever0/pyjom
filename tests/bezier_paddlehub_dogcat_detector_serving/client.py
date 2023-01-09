test_image = "/root/Desktop/works/pyjom/samples/image/dog_with_text.jpg"
from server import changeDirForImport
changeDirForImport()
from pyjom.imagetoolbox import bezierPaddleHubResnet50ImageDogCatDetectorClient
result = bezierPaddleHubResnet50ImageDogCatDetectorClient(test_image)
print("RESULT?",result)