import ffmpeg

input_source = ""

stream = ffmpeg.input(input_source,ss=4, to=)
# stream = ffmpeg.hflip(stream)
# we just need to crop this.
stream = ffmpeg.output(stream, 'output.mp4')
ffmpeg.run(stream, overwrite_output=True)