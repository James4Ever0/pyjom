from jpype import *

startJVM(getDefaultJVMPath(), "-ea")
java.lang.System.out.println("Calling Java Print from Python using Jpype!")
addClassPath("/root/Desktop/works/pyjom/tests/karaoke_effects/classpath/lingua.jar")

from com.github.pemistahl.lingua.api import *

shutdownJVM()