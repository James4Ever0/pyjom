from jpype import *
startJVM(getDefaultJVMPath(), "-ea",classpath="")
java.lang.System.out.println("Calling Java Print from Python using Jpype!")
shutdownJVM()