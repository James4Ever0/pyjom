import ffmpeg

# mediaPath = "/root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png"
mediaPath = "/root/Desktop/works/pyjom/samples/image/dog_with_black_borders.png"  # use the image with black background.
# ffmpeg -loop 1 -i /root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png -t 15 -vf cropdetect -f null -

stdout, stderr = (
    ffmpeg.input(mediaPath, loop=1, t=15)
    .filter("cropdetect")
    .output("null", f="null")
    .run(capture_stdout=True, capture_stderr=True)
)


stdout_decoded = stdout.decode("utf-8")
stderr_decoded = stderr.decode("utf-8")

# nothing here.
# for line in stdout_decoded.split("\n"):
#     print(line)

# breakpoint()

for line in stderr_decoded.split("\n"):
    line = line.replace("\n", "").strip()
    import parse
    formatString='[{}] x1:{x1} x2:{x2} y1:{y1} y2:{y2} w:{w} h:{h} x:{x} y:{y} pts:{pts} t:{t} crop='
    print(line)
    # [Parsed_cropdetect_0 @ 0x56246a16cbc0] x1:360 x2:823 y1:0 y2:657 w:464 h:656 x:360 y:2 pts:3 t:0.120000 crop=464:656:360:2
    # this crop usually will never change. but let's count?