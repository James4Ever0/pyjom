from test import detect_volume_average

output_path = "volDetect_test.mp4"
# detect_volume_average(output_path, debug=True)
adjustVolumeInMedia(output_path, normalizedOutputPath)
detect_volume_average(normalizedOutputPath, debug=True)