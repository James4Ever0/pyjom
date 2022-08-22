import ffmpeg

def basicTrimVideoProcess():
    input_source = "/root/Desktop/works/pyjom/samples/video/karaoke_effects_source.mp4"

    stream = ffmpeg.input(input_source,ss=4, to=10) # from 4 to 10 seconds?
    # stream = ffmpeg.hflip(stream)
    # we just need to crop this.
    stream = ffmpeg.output(stream, 'output.mp4')
    ffmpeg.run(stream, overwrite_output=True)


# pipCrop in some span?

def cropVideoRegion():
    # this lasts for 6 seconds.
    # what is the shape of your thing?
    # just use simple concat. right?
    # 334x188
    # not only crop, but ZOOM!
    stream_0 = ffmpeg.input("output.mp4",ss=0, to=2).filter("crop",x,y,width,height)
    stream_1 = ffmpeg.input("output.mp4",ss=2, to=4).filter("crop",x,y,width,height)
    stream_2 = ffmpeg.input("output.mp4",ss=4, to=6).filter("crop",x,y,width,height)

    stream = ffmpeg.output(stream, "pipCrop.mp4")
    ffmpeg.run(stream, overwrite_output=True)