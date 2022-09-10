

    def getPathAccessTime(path):
        if os.path.exists(path):
            return os.stat(path).st_mtime
        else:
            return -1

    modelPaths = ["/media/root/parrot/pyjom/tests/cpm_chinese_chitchat_model_gpt2/model","/media/root/parrot/pyjom/tests/cpm_chinese_chitchat_model_gpt2/model2"]
    # sort them with time.
    workingModelPath = None

    modelPaths.sort(key = lambda modelPath: -getPathAccessTime(os.path.join(modelPath, 'pytorch_model.bin'))) # get latest model first, if loaded successifully

    for modelPath in modelPaths:
        try:
            model = modelClass.from_pretrained(modelPath)
            workingModelPath = modelPath
        except:
            pass
    if workingModelPath:
        saveModelPath = [modelPath for modelPath in modelPaths if modelPath !=workingModelPath][0]
        return model, (worki)
    else:
        print("no working model found. program will exit.")
        exit()