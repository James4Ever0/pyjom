import sys
import os
def changeDirForImport():
    os.chdir("/root/Desktop/works/pyjom")
    sys.path.append(".")


if __name__ == '__main__':
    changeDirForImport()
    from pyjom.config.shared import pyjom_config
    pyjom_config['BEZIER_PADDLE_RESNET50_IMAGE_DOG_CAT_DETECTOR_SERVER_INSTANCE']=True
    from pyjom.imagetoolbox import bezierPaddleHubResnet50ImageDogCatDetectorServer
    bezierPaddleHubResnet50ImageDogCatDetectorServer()