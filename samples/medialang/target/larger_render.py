ass_file_path=SUBTITLE="/root/Desktop/works/pyjom/samples/medialang/target/ass_larger_text_size.ass"
videoInput=VIDEO="/root/Desktop/works/pyjom/samples/medialang/target/halfdone_without_ass_dogcat_sample.mp4"

import ffmpeg
videoInput = ffmpeg.input(rendered_media_location).video
audioInput = ffmpeg.input(rendered_media_location).audio
videoInput = videoInput.filter(
    "ass", ass_file_path
)
ffmpeg.output(videoInput,audioInput,final_output_location,acodec='copy').run(overwrite_output=True)