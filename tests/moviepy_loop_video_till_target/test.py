from loop_till_target import main

target_secs = 20
video_in = "/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif"
video_out = f"/root/Desktop/works/pyjom/samples/video/cute_cat_gif_{target_secs}_secs_plus.gif"

main(video_in, target_secs ,f_out=video_out ,in_place=False)