from jpype import *
import jpype.imports  # this is needed! shit.

addClassPath("/root/Desktop/works/pyjom/tests/karaoke_effects/classpath/lingua.jar")

startJVM(getDefaultJVMPath())

java.lang.System.out.println("Calling Java Print from Python using Jpype!")

from com.github.pemistahl.lingua.api import *


# detector = LanguageDetectorBuilder.fromAllLanguages().withLowAccuracyMode().build()
linguaDetector = (
    LanguageDetectorBuilder.fromAllLanguages().build()
)  # 3.5GB just for detecting language! it is somehow crazy.


def getLinguaDetectedLanguageLabel(sample):
    result = linguaDetector.detectLanguageOf(sample)
    # print(result, type(result)) # <java class 'com.github.pemistahl.lingua.api.Language'>
    # but we can convert it into string.
    strResult = str(result)
    return strResult


# shutdownJVM()
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def server_hello():
    return "say hello to jpype fastapi server"


@app.get("/langid")
def read_item(text: str):
    code = 200
    try:
        result = getLinguaDetectedLanguageLabel(text)
    except:
        code = 400
        import traceback

        traceback.print_exc()
        print("ERROR ANALYSING TEXT LANGID %s" % text)
        result = "ERROR"
    return {"code": code, "result": result}
