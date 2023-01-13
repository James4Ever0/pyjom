import random
from adtools import getCatOrDogAd

def test_init():
    cat_or_dog='cat'
    for _ in range(2):
        responses = getCatOrDogAd(cat_or_dog)
        videoInfo = random.choice(responses[:20])
        print(videoInfo)
        print()

def test_cats_and_dogs_get_video_names():
    for category in ['cat','dog']:
        print("_"*20)
        print("CATEGORY?",category)
        print()

        responses = getCatOrDogAd(category,method='bm25') # it does not update that often. use online search instead? (fill keywords in description)
        for info in responses:
            title = info['title']
            print("VIDEO?",title)

if __name__ == '__main__':
    # test_init()
    test_cats_and_dogs_get_video_names()