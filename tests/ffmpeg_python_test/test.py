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
    stream = ffmpeg.input("output.mp4")

    stream = ffmpeg.output(stream, "pipCrop.mp4")
    ffmpeg.run(stream, overwrite_output=True)