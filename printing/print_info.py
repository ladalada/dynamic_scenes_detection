import datetime

from printing.output_formatting_utils import get_arr_for_print, arr_convert, get_pairs_arr_for_print, pairs_arr_convert


def print_scene_change_info(scenes_borders_milliseconds):
    print()
    print(datetime.datetime.now(), "Number of scenes changed: ", len(scenes_borders_milliseconds))
    print(datetime.datetime.now(), "Scene changes boundaries in milliseconds: ")
    scene_bound_count = 1
    for el in get_arr_for_print(arr_convert(scenes_borders_milliseconds)):
        print(scene_bound_count, " ", el)
        scene_bound_count += 1
    print()


def print_dynamic_scenes_info(dynamic_scenes_borders_milliseconds):
    print()
    print(datetime.datetime.now(), "Number of dynamic scenes: ", len(dynamic_scenes_borders_milliseconds))
    print(datetime.datetime.now(), "Dynamic scene boundaries in milliseconds: ")
    dyn_scene_bound_count = 1
    for el in get_pairs_arr_for_print(pairs_arr_convert(dynamic_scenes_borders_milliseconds)):
        print(dyn_scene_bound_count, " ", el)
        dyn_scene_bound_count += 1
    print()
