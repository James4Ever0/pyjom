scenedetect -i sample.mp4 -s video.stats.csv detect-content list-scenes -f sample_scenes.csv
# for dynamic analysis:
# https://github.com/Breakthrough/PySceneDetect/README.md
# from scenedetect import open_video, SceneManager, split_video_ffmpeg
# from scenedetect.detectors import ContentDetector
# from scenedetect.video_splitter import split_video_ffmpeg

# def split_video_into_scenes(video_path, threshold=27.0):
#     # Open our video, create a scene manager, and add a detector.
#     video = open_video(video_path)
#     scene_manager = SceneManager()
#     scene_manager.add_detector(
#         ContentDetector(threshold=threshold))
#     scene_manager.detect_scenes(video, show_progress=True)
#     scene_list = scene_manager.get_scene_list()
#     split_video_ffmpeg(video_path, scene_list, show_progress=True)