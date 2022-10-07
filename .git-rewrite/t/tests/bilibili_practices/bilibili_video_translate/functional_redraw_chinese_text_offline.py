from paddleocr import PaddleOCR
import wordninja

# from m2m100_1b_translator import zh_to_en_translator as translator
# cannot translate everything... not frame by frame...
# can summarize things. can block texts on location.
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
# img_path = 'target.png' # only detect english. or not?
ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
# image = cv2.imread(img_path)
# we will give it to you...
# internalFrameCounter = 0
# resultChineseInternal = []
def redraw_english_to_chinese(image): # whatever. it is dumb anyway. we need to be prudent. really?
    # global resultChineseInternal, internalFrameCounter # we need to look ahead.
    resultChineseInternal2 = ocr.ocr(image, cls=True) # you will be fucked if skip frames.
    prob_thresh = 0.6 # found watermark somewhere. scorpa
    resultChineseInternal = []

    for index, line in enumerate(resultChineseInternal2):
        # print(line)
        # breakpoint()
        coords, (text, prob) = line
        prob = float(prob)
        if prob > prob_thresh:
            rectified_text = " ".join(wordninja.split(text))
            line[1] = (rectified_text, prob)
            print(line)
            resultChineseInternal.append(line)
    return resultChineseInternal

# cv2.imshow('dst',dst2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# expand the area somehow.
# draw resultChineseInternal
# simhei_path = "/root/Desktop/works/bilibili_tarot/SimHei.ttf"
# from PIL import Image
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in resultChineseInternal]
# txts = [line[1][0] for line in resultChineseInternal]
# scores = [line[1][1] for line in resultChineseInternal]
# im_show = draw_ocr(image, boxes, txts, scores, font_path=simhei_path)
# im_show = Image.fromarray(im_show)
# im_show.save('resultChineseInternal.jpg')

# we will be testing one image only. not the whole goddamn video.
# may have cuda error when using my cv2 cuda libs.