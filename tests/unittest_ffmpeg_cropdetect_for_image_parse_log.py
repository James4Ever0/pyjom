import ffmpeg
mediaPath = ""
stdout, stderr = (
            ffmpeg.input(mediaPath)
            .output("null", f="null")
            .run(capture_stdout=True, capture_stderr=True)
        )
stderr_lower = stderr.decode("utf-8")