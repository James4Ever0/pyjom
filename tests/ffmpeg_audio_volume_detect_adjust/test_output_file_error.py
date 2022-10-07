from test import detect_volume_average, adjustVolumeInMedia

output_path = "volDetect_test.mp4"
# detect_volume_average(output_path, debug=True)
normalizedOutputPath = "normalized.mp4"
# Output extension mp4 does not support PCM audio. Please choose a suitable audio codec with the -c:a option.
# wtf are you talking about?
adjustVolumeInMedia(output_path, normalizedOutputPath)
detect_volume_average(normalizedOutputPath, debug=True)