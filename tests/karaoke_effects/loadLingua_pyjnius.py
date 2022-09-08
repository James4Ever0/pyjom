import jnius_config
# jnius_config.add_options('-Xrs', '-Xmx4096')
jnius_config.set_classpath('.', "/root/Desktop/works/pyjom/tests/karaoke_effects/classpath/lingua.jar")
import jnius
jnius.autoclass('java.lang.System').out.println('Running Java Program Using Pyjnius!')
pyjniusLinguaDetector = jnius.autoclass('com.github.pemistahl.lingua.api.LanguageDetectorBuilder').fromAllLanguages().build()

sample = 'hello world'

result = pyjniusLinguaDetector.detectLanguageOf(sample)
print(result, type(result))
# breakpoint()
strResult = result.toString()
print(strResult, type(strResult))