# Detection and segmentation of dynamic scenes in video

This repository contains a Python implementation of a system capable of detecting and segmenting dynamic scenes in a video.

A dynamic scene means a sequence of frames containing a relatively stable semantic background in which there is a movement of objects belonging to the scene.

The main stages of the algorithm are as follows: 
* search for scene changes; 
* search for object movement;
* segmentation of selected video fragments into video files.

This algorithm is applicable for videos recorded from a fixed camera or for video files created by concatenating such videos.
