import ffmpeg

input_source = ""

stream = ffmpeg.input(input_source)
stream = ffmpeg.hflip(stream)
stream = ffmpeg.output(stream, 'output.mp4')
ffmpeg.run(stream)