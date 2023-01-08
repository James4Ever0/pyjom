import paddlehub as hub

language_translation_model = hub.Module(name="baidu_translate")
language_recognition_model = hub.Module(name="baidu_language_recognition")

text = "hello world"
language_code = language_recognition_model.recognize(text)
print("language_code: %s" % language_code)
