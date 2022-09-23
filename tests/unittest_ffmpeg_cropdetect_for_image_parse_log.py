import ffmpeg
mediaPath = "/root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png"
# ffmpeg -loop 1 -i /root/Desktop/works/pyjom/samples/image/dog_blue_sky_split_line.png -t 15 -vf cropdetect -f null -

stdout, stderr = (
            ffmpeg.input(mediaPath)
            .output("null", f="null")
            .run(capture_stdout=True, capture_stderr=True)
        )
stderr_lower = stderr.decode("utf-8")