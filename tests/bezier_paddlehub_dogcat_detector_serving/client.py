test_image = "/root/Desktop/works/pyjom/samples/image/dog_with_text.jpg"
from server import changeDirForImport
changeDirForImport()
from pyjom.imagetoolbox import bezierPaddleHubResnet50ImageDogCatDetectorClient,bezierPaddleHubResnet50ImageDogCatDetectorServerChecker
import cv2
test_image = cv2.imread(test_image)

bezierPaddleHubResnet50ImageDogCatDetectorServerChecker()
result = bezierPaddleHubResnet50ImageDogCatDetectorClient(test_image)
print("RESULT?",result)