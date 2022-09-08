from jpype import *
startJVM(getDefaultJVMPath(), "-ea")
java.lang.System.out.println("Calling Java Print from Python using Jpype!")
shutdownJVM()