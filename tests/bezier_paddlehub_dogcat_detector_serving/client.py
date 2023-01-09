test_image =""
from server import changeDirForImport
changeDirForImport()
from pyjom.imagetoolbox import bezierPaddleHubResnet50ImageDogCatDetectorClient
result = bezierPaddleHubResnet50ImageDogCatDetectorClient(test_image)
print("RESULT?",result)