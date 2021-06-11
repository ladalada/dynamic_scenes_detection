import datetime

from search.scene_change_detection.detectSceneChange import get_scenes_border_milliseconds
from search.scene_detection.detectSceneWithMotion import detect_scene_with_motion
from printing.print_info import print_dynamic_scenes_info, print_scene_change_info


def detect_dynamic_scenes(input, output):

    scenes_border_msec = get_scenes_border_milliseconds(input)
    print_scene_change_info(scenes_border_msec)

    dynamic_scene_borders = detect_scene_with_motion(
        alg="AverageFrameComparison",
        input_path=input,
        output_path=output,
        border_msec=scenes_border_msec,
        bounding_box=False,
        motion_history=0.2,
        buffer_size_value=40,
        min_area=10,
        delta_thresh=20
    )

    print_dynamic_scenes_info(dynamic_scene_borders)


if __name__ == '__main__':

    startTime = datetime.datetime.now()
    print("Start time:", startTime)

    # the path to the input video file
    input_path = 'data/input/input_video.mp4'

    # path to directory for recording output videos
    output_dir = 'data/output/output_for_input_video'

    detect_dynamic_scenes(input_path, output_dir)

    finishTime = datetime.datetime.now()
    print("Finish time:", finishTime)
    print("Total time:", finishTime - startTime)
