import test # for appending path only.
from pyjom.audiotoolbox import detect_volume_average, adjustVolumeInMedia

output_path = "volDetect_test.mp4"
# detect_volume_average(output_path, debug=True)
normalizedOutputPath = "normalized.mp4"
# Output extension mp4 does not support PCM audio. Please choose a suitable audio codec with the -c:a option.
# wtf are you talking about?

online_fetched_media = "/root/Desktop/works/pyjom/tests/calculate_separate_video_scene_duration_in_dog_video_with_bgm/sample.mp4"
# is this the standard?
targets, error = detect_volume_average(online_fetched_media, debug=True)
# at least let me see this shit.
# breakpoint()
# {'mean': -10.6, 'max': 0.0}
# according to the volume, it seems that everyone agree with this 'industrial standard'
if not error:
    adjustVolumeInMedia(
        output_path, normalizedOutputPath, overwrite_output=True, targets=targets
    )
    detect_volume_average(normalizedOutputPath, debug=True)
else:
    print("error when detecting volume in media: %s" % online_fetched_media)
    # what is cliping?
    # WARNING: Adjusting will lead to clipping of 4.209296 dB                                 
# even worse with default settings.
# VOLUME NORMALIZATION SUCCESSFUL
# MEDIA PATH: normalized.mp4
# VOLUME: {'mean': -25.1, 'max': -8.8}
# ERROR STATUS: False
# 'mean' -> target level
# 'max' -> true peak (really?)
