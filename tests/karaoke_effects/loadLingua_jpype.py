from jpype import *
import jpype.imports # this is needed! shit.

addClassPath("/root/Desktop/works/pyjom/tests/karaoke_effects/classpath/lingua.jar")

startJVM(getDefaultJVMPath())
java.lang.System.out.println("Calling Java Print from Python using Jpype!")

from com.github.pemistahl.lingua.api import *


detector = LanguageDetectorBuilder.fromAllLanguages().withLowAccuracyMode().build()

sample = 'hello world'

detector.detectLanguageOf(sample)

shutdownJVM()