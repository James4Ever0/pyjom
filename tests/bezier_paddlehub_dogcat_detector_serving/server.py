import sys
import os
def changeDirForImport():
    os.chdir("/root/Desktop/works/pyjom")
    sys.path.append(".")


if __name__ == '__main__':
    changeDirForImport()
    from pyjom.imagetoolbox import bezierPaddleHubResnet50ImageDogCatDetectorServer
    bezierPaddleHubResnet50ImageDogCatDetectorServer()