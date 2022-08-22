from asyncio import StreamReader
import ffmpeg

def basicTrimVideoProcess():
    input_source = "/root/Desktop/works/pyjom/samples/video/karaoke_effects_source.mp4"

    stream = ffmpeg.input(input_source,ss=4, to=10) # from 4 to 10 seconds?
    # stream = ffmpeg.hflip(stream)
    # we just need to crop this.
    stream = ffmpeg.output(stream, 'output.mp4')
    ffmpeg.run(stream, overwrite_output=True)

def getRandomCrop(width, height):
    import random
    randomGenerator = lambda: random.uniform(0.3, 0.8)

    newWidth, newHeight = int(randomGenerator()*width), int(randomGenerator()*height)

    newX, newY = random.randint(0, width-newWidth), random.randint(0, height-newHeight)
    return newX, newY, newWidth, newHeight
# pipCrop in some span?

def cropVideoRegion():
    # this lasts for 6 seconds.
    # what is the shape of your thing?
    # just use simple concat. right?
    # 334x188
    from MediaInfo import MediaInfo
    info = MediaInfo(filename = 'output.mp4')
    infoData = info.getInfo()
    # print(infoData)
    # breakpoint()
    defaultWidth = infoData["videoWidth"]
    defaultHeight = infoData["videoHeight"]
    # not only crop, but ZOOM!
    import math

    x, y, width, height = getRandomCrop(defaultWidth, defaultHeight)
    stream_0 = ffmpeg.input("output.mp4",ss=0, to=2).crop(x,y,width, height).filter("pad",x=math.floor((defaultWidth-width)/2), y=math.floor((defaultHeight-height)/2), width=defaultWidth, height=defaultHeight,color="black")



    x, y, width, height = getRandomCrop(defaultWidth, defaultHeight)
    stream_1 = ffmpeg.input("output.mp4",ss=2, to=4).crop(x,y,width, height).filter("pad",x=math.floor((defaultWidth-width)/2), y=math.floor((defaultHeight-height)/2), width=defaultWidth, height=defaultHeight,color="black")

    
    x, y, width, height = getRandomCrop(defaultWidth, defaultHeight)
    stream_2 = ffmpeg.input("output.mp4",ss=4, to=6).crop(x,y,width, height).filter("pad",x=math.floor((defaultWidth-width)/2), y=math.floor((defaultHeight-height)/2), width=defaultWidth, height=defaultHeight,color="black")

    video_stream = ffmpeg.concat(stream_0, stream_1, stream_2)

    audio_stream = ffmpeg.input("output.mp4").audio

    stream = ffmpeg.concat()
    # there is no audio down here! fuck.

    stream = ffmpeg.output(stream, "pipCrop.mp4")
    ffmpeg.run(stream, overwrite_output=True)

def concatVideoWithAudio():
    stream_0 = ffmpeg.input("output.mp4",ss=0, t=3)
    stream_1 = ffmpeg.input("output.mp4",ss=3, t=6)

    stream = ffmpeg.concat(stream_0.video, stream_0.audio, stream_1.video, stream_1.audio, v=1, a=1).node
    # print(stream)
    # breakpoint()
    stream = ffmpeg.output(stream[0], stream[1], "concatVideo.mp4")
    # print(stream.get_args())
    stream.run(overwrite_output=True)

if __name__ == "__main__":
    # cropVideoRegion()
    concatVideoWithAudio() # damn quiet out there.