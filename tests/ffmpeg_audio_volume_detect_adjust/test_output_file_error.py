from test import detect_volume_average, adjustVolumeInMedia

output_path = "volDetect_test.mp4"
# detect_volume_average(output_path, debug=True)
normalizedOutputPath = "normalized.mp4"
# Output extension mp4 does not support PCM audio. Please choose a suitable audio codec with the -c:a option.
# wtf are you talking about?

online_fetched_media = "/root/Desktop/works/pyjom/tests/calculate_separate_video_scene_duration_in_dog_video_with_bgm/sample.mp4"

adjustVolumeInMedia(output_path, normalizedOutputPath, overwrite_output=True)
detect_volume_average(normalizedOutputPath, debug=True)
# even worse with default settings.
# VOLUME NORMALIZATION SUCCESSFUL
# MEDIA PATH: normalized.mp4
# VOLUME: {'mean': -25.1, 'max': -8.8}
# ERROR STATUS: False
# 'mean' -> target level
# 'max' -> true peak (really?)