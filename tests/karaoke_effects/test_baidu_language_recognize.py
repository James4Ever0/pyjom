import paddlehub as hub

language_translation_model = hub.Module(name="baidu_translate")
language_recognition_model = hub.Module(name="baidu_language_recognition")

# text = "hello world"
# "zh", 'en', 'jp'
# text = "請輸入要轉換簡繁體的中文漢字" # zh
text = "私は日本人です"
language_code = language_recognition_model.recognize(text)
print("language_code: %s" % language_code)
