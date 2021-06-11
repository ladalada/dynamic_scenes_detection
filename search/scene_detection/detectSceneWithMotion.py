from search.scene_detection.detect_motion_scenes_using_average_frame import detect_scene_with_motion_average_frame
from search.scene_detection.detect_motion_scenes_using_first_frame import detect_scene_with_motion_first_frame


def detect_scene_with_motion(alg, input_path, output_path, border_msec,
                             buffer_size_value=6, rect_color=(204, 0, 204), min_area=10, bounding_box=False,
                             delta_thresh=25, motion_history=0.3):
    if alg == 'FirstFrameComparison':
        return detect_scene_with_motion_first_frame(input_path, output_path, border_msec,
                                                    buffer_size_value, rect_color, min_area, bounding_box)
    elif alg == 'AverageFrameComparison':
        return detect_scene_with_motion_average_frame(input_path, output_path, border_msec,
                                                      buffer_size_value, rect_color, min_area, bounding_box,
                                                      delta_thresh, motion_history)
    else:
        print('AverageFrameComparison is automatically selected')
        return detect_scene_with_motion_average_frame(input_path, output_path, border_msec,
                                                      buffer_size_value, rect_color, min_area, bounding_box,
                                                      delta_thresh, motion_history)
