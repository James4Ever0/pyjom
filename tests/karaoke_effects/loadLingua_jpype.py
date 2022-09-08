from jpype import *
startJVM(getDefaultJVMPath(), "-ea", classpath=["/root/Desktop/works/pyjom/tests/karaoke_effects/classpath/*"])
java.lang.System.out.println("Calling Java Print from Python using Jpype!")

import com.github.pemistahl.lingua.api as API

shutdownJVM()