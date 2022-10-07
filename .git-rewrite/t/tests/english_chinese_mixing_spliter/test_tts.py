from paddlebobo_paddletools_tts import TTSExecutor

from english_grepper import analyze_mixed_text
mtext = "你这dollar有问题啊"
# analyze this shit.

# you can translate all english into chinese. doesn't hurt.

text_analyze_result = analyze_mixed_text(mtext)
# print(text_analyze_result)
# breakpoint()

tts_config = {"zh": {"model_tag": 'fastspeech2_csmsc-zh',
                     "voc_tag": "hifigan_csmsc-zh", "lang": "zh"}, "en": {"model_tag": 'fastspeech2_ljspeech-en',
                                                                          "voc_tag": "hifigan_ljspeech-en", "lang": "en"}}

# tts_config = {"zh": {"model_tag": 'tacotron2_csmsc-zh',
#                      "voc_tag": "hifigan_csmsc-zh", "lang": "zh"}, "en": {"model_tag": 'tacotron2_ljspeech-en',
#                      "voc_tag": "hifigan_ljspeech-en", "lang": "en"}}

for langid in ["en", "zh"]:
    lang_config = tts_config[langid]
    TTS = TTSExecutor('default.yaml', **lang_config)  # PaddleSpeech语音合成模块
    # do we need to delete the TTS?
    for data in text_analyze_result[langid]:
        index, text = data["index"], data["text"]
        wavfile = TTS.run(
            text=text, output='output_{}_{}.wav'.format(langid, index))  # 合成音频
    del TTS
# there is no freaking english shit.
# we need english tool.
# you can also translate this shit.
