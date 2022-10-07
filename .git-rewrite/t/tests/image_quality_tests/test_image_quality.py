# import imquality.brisque as brisque
import cv2
import PIL

video = cv2.VideoCapture("../../samples/video/dog_with_text.mp4")

_,frame = video.read()
# frame = imutils.resize(frame,width=720) #why?
index = 0
score = -1
period = 20
while frame is not None:
    _, frame = video.read()
    index+=1
    if frame is None:
        print("VIDEO END.")
        break
    # just get image quality.
    # the speed is not so damn fast.
    image = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    image = PIL.Image.fromarray(image)
    if index%period == 0:
        try:
            score = brisque.score(image) # the lower the better, it was said.
        except:
            score = -1 # unknown.
    cv2.putText(
        frame,
        "[{}]".format(str(score)[:5]),
        (200,200),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0,255,0),
        3,
        cv2.LINE_AA,
    )
    cv2.imshow('Output',frame)
    key  =  cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break

