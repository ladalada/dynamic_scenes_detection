import math
import os


def get_video_file_name(input_video):
    return os.path.splitext(os.path.basename(input_video))[0]


def convert(milliseconds):
    seconds = milliseconds / 1000
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return hours, minutes, seconds


def array_to_pair_list(array):
    dynamic_scene_boundaries = []
    i = 0
    while i < len(array):
        start = array[i]
        i += 1
        end = array[i]
        i += 1
        dynamic_scene_boundaries.append((start, end))
    return dynamic_scene_boundaries


def arr_convert(arr):
    new_arr = []
    for el in arr:
        new_arr.append(convert(el))
    return new_arr


def pairs_arr_convert(pairs_arr):
    new_arr = []
    for pair in pairs_arr:
        el1 = convert(pair[0])
        el2 = convert(pair[1])
        new_arr.append((el1, el2))
    return new_arr


def zero(x):
    zeros_count = 2
    return str(x).zfill(zeros_count)


def get_time_str(time):
    new_time = ""
    hour = time[0]
    minutes = time[1]
    seconds = time[2]
    new_time += str(zero(math.trunc(hour))) + ":"
    new_time += str(zero(math.trunc(minutes))) + ":"
    new_time += str(round(seconds, 3))
    return new_time


def get_arr_for_print(arr):
    new_arr = []
    for time in arr:
        el = get_time_str(time)
        new_arr.append(el)
    return new_arr


def get_pairs_arr_for_print(pairs_arr):
    new_arr = []
    for pair in pairs_arr:
        el1 = get_time_str(pair[0])
        el2 = get_time_str(pair[1])
        new_arr.append((el1, el2))
    return new_arr
