import argparse
import cv2


def get_args(output_path, buffer_size_value, fps_value=20):
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output",
                    default=output_path,
                    help="path to output directory")
    ap.add_argument("-f", "--fps", type=int,
                    default=fps_value,
                    help="FPS of output video")
    ap.add_argument("-c", "--codec", type=str,
                    default="MJPG",
                    help="codec of output video")
    ap.add_argument("-b", "--buffer-size", type=int,
                    default=buffer_size_value,
                    help="buffer size of video clip writer")
    args = vars(ap.parse_args())
    return args


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # grab the image size
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    return resized


def grab_contours(cnts):
    # if the length the contours tuple returned by cv2.findContours is '2'
    # then we are using either OpenCV v2.4
    if len(cnts) == 2:
        cnts = cnts[0]

    # if the length of the contours tuple is '3' then we are using either OpenCV v3
    elif len(cnts) == 3:
        cnts = cnts[1]

    # otherwise OpenCV has changed their cv2.findContours return
    # signature yet again and I have no idea WTH is going on
    else:
        raise Exception(("Contours tuple must have length 2 or 3, "
                         "otherwise OpenCV changed their cv2.findContours return "
                         "signature yet again. Refer to OpenCV's documentation "
                         "in that case"))

    # return the actual contours array
    return cnts
