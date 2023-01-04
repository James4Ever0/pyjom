def checkCatOrDog(Content:str):
    # cat? dog? None?
    catSignals = []
    dogSignals = []
    elemDict = {"cat":catSignals, "dog":dogSignals}
    for key, elems in elemDict.items():
        for elem in elems:
            if elem in Content.lower():
                return key
    return None