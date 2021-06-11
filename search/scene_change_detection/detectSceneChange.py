import moviepy.editor

from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector


def get_duration_in_seconds(input_video):
    video = moviepy.editor.VideoFileClip(input_video)
    # Contains video duration in seconds
    video_duration = int(video.duration)
    return video_duration


def get_scenes_border_milliseconds(input_video, threshold_for_scene_change_detector=30.0):
    scenes = find_scene_change(input_video, threshold_for_scene_change_detector)
    border_msec = []
    for scene in scenes:
        border_msec.append(scene.get_seconds() * 1000)
    if len(scenes) == 0:
        border_msec.append(get_duration_in_seconds(input_video) * 1000)
    return border_msec


def find_scene_change(video_path, threshold):
    # Create video manager and scene manager
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    # Add the detector
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    # Improve processing speed by downscaling before processing
    video_manager.set_downscale_factor()
    # Start the video manager and perform the scene detection
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    return scene_manager.get_cut_list()
