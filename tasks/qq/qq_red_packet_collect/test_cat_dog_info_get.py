from adtools import getCatOrDogAd
import random

def test_init():
    cat_or_dog='cat'
    for _ in range(2):
        responses = getCatOrDogAd(cat_or_dog)
        videoInfo = random.choice(responses[:20])
        print(videoInfo)
        print()

def test_cats_and_dogs():
    ...