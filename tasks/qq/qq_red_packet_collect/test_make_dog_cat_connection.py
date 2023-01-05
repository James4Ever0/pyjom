
from adtools import makeCatOrDogConnections
def test_main():
    makeCatOrDogConnections('123','345','cat', debug=True)
def test_delete():
    makeCatOrDogConnections('123','345','cat', debug=True, delete=True)