import sys
import os
def changeDirForImport():
    os.chdir("/root/Desktop/works/pyjom")
    sys.path.append(".")
from pyjom.imagetoolbox import bezierPaddleHubResnet50ImageDogCatDetectorServer

if __name__ == '__main__':
    changeDirForImport()
    bezierPaddleHubResnet50ImageDogCatDetectorServer()