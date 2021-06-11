from printing.output_formatting_utils import array_to_pair_list
from search.scenes_recording.dynamicSceneWriter import DynamicSceneWriter
import datetime
import cv2
from search.scene_detection import utils
from search.scene_detection.utils import get_args
from printing.output_formatting_utils import get_video_file_name


def detect_scene_with_motion_average_frame(input_path, output_path, border_msec,
                                           buffer_size_value, rect_color, min_area, bounding_box,
                                           delta_thresh, motion_history):
    dynamic_scene_boundaries_list = []

    # initialize the video and arguments
    vs = cv2.VideoCapture(input_path)
    args = get_args(output_path, buffer_size_value, vs.get(cv2.CAP_PROP_FPS))

    # initialize dynamic scene writer and the consecutive number of frames that have not contained any action
    dsw = DynamicSceneWriter(bufSize=args["buffer_size"])
    consec_frames_without_action = 0

    # initialize the background template frame in the video stream
    background_template_frame = None

    end_second_num = 0

    while True:
        # grab the current frame
        ret, frame = vs.read()

        if frame is None:
            break

        # resize the current frame
        frame = utils.resize(frame, width=500)

        # initialize a boolean var used to indicate if the consecutive frames counter should be updated
        update_consec_frames = True

        # convert frame to grayscale, and blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the background template frame is None, initialize it
        if background_template_frame is None:
            print("Creating an initial background model")
            background_template_frame = gray.copy().astype("float")
            continue

        # accumulate the weighted average between the current frame and previous frames
        cv2.accumulateWeighted(gray, background_template_frame, motion_history)

        # compute the difference between the current frame and running average
        delta_frame = cv2.absdiff(gray, cv2.convertScaleAbs(background_template_frame))

        # threshold the delta frame
        thresh = cv2.threshold(delta_frame, delta_thresh, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded frame to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)

        # find contours on thresholded frame
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = utils.grab_contours(contours)

        video_msec = vs.get(cv2.CAP_PROP_POS_MSEC)

        # only proceed if at least one contour was found
        if len(contours) > 0:
            # find the largest contour in the contours array,
            # then use it to compute the Straight Bounding Rectangle
            c = max(contours, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(c)
            contour_area = cv2.contourArea(c)
            update_consec_frames = contour_area <= min_area

            # only proceed if the area meets a minimum size
            if not update_consec_frames:
                # reset the number of consecutive frames with no action to zero
                consec_frames_without_action = 0

                # draw the rectangle surrounding the object
                if bounding_box:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), rect_color, 2)

                # if we are not already recording, start recording
                if not dsw.recording:
                    p = "{}/{}_{}ms.avi".format(args["output"],
                                                get_video_file_name(input_path),
                                                int(round(video_msec)))
                    dsw.start(p, cv2.VideoWriter_fourcc(*args["codec"]), args["fps"])
                    print(datetime.datetime.now(), "Dynamic scene recording into video file: ", p)
                    dynamic_scene_boundaries_list.append(video_msec)

        # otherwise, no action has taken place in the current frame,
        # so increment the number of consecutive frames that contain no action
        if update_consec_frames:
            consec_frames_without_action += 1

        # update the actions frames clip buffer
        dsw.update(frame)

        # if recording is in progress
        # and reached a threshold on consecutive number of frames with no action,
        # stop recording the clip
        if dsw.recording and consec_frames_without_action == args["buffer_size"]:
            dsw.finish()
            dynamic_scene_boundaries_list.append(video_msec)

        # otherwise, if the boundaries of the scenes in the array still remain
        # and the current time has exceeded the boundary,
        # then stop recording and reset the background template
        elif (end_second_num < len(border_msec) - 1) and (video_msec >= border_msec[end_second_num]):
            end_second_num += 1
            background_template_frame = None
            dsw.finish()
            dynamic_scene_boundaries_list.append(video_msec)
            print(datetime.datetime.now(), "Scene change")

        # show the frame and record if the user presses a key
        cv2.imshow("Frame", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", delta_frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # if the process of recording a clip continues, then wrap it up
    if dsw.recording:
        dsw.finish()
        dynamic_scene_boundaries_list.append(border_msec[len(border_msec) - 1])

    print(datetime.datetime.now(), "All dynamic scenes are segmented")

    cv2.destroyAllWindows()

    return array_to_pair_list(dynamic_scene_boundaries_list)
