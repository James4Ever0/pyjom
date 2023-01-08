
    responses = getCatOrDogAd(cat_or_dog)
    success = False

    with getAdLock():
        if responses != []:
            videoInfo = random.choice(responses[:recentLimits])