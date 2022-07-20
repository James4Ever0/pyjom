import cv2

video_file = "/media/root/help/pyjom/samples/video/dog_with_text.mp4"

video = cv2.VideoCapture(video_file)

ret, img = video.read()
prevImg = img.copy()

counter = 0
while True:
    ret, img = video.read()
    if img is None: break
    else:
        frame1 = prevImg
        # frame1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        frame2 = img # why freaking grayscale?
        # frame2 =  cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        if counter == 40:
            cv2.imwrite("frame0.png",frame1)
            cv2.imwrite("frame1.png",frame2)
        prevImg = img.copy()
        counter +=1
        