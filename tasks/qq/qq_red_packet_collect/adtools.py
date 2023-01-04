def checkCatOrDog(Content: str):
    # cat? dog? None?
    catSignals = ["喵喵", "猫", "猫咪", "喵"]

    dogSignals = [
        "狗狗",
        "狗",
        "汪汪",
        "修勾",
        "汪",
        "狗子",
    ]
    dogSignals = []
    elemDict = {"cat": catSignals, "dog": dogSignals}
    for key, elems in elemDict.items():
        for elem in elems:
            if elem in Content.lower():
                return key
    return None


def makeCatOrDogConnections(group_id:str, sender_id:str, cat_or_dog:str): # whatever.
    