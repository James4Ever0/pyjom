from adtools import makeCatOrDogConnections, getCatOrDogAd


def test_main():
    makeCatOrDogConnections("123", "345", "cat", debug=True)


def test_delete():
    makeCatOrDogConnections("123", "345", "cat", debug=True, delete=True)


def test_query():
    response = getCatOrDogAd("cat", debug=True)
    response = getCatOrDogAd("dog", debug=True)


if __name__ == "__main__":
    test_query()
