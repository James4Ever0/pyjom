from jpype import *
startJVM(getDefaultJVMPath(), "-ea",classpath=["/root/Desktop/works/pyjom/tests/karaoke_effects/lingua-1.2.2-with-dependencies.jar"])
java.lang.System.out.println("Calling Java Print from Python using Jpype!")
java.
shutdownJVM()