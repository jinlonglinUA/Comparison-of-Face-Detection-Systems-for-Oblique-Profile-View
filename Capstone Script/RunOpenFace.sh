#!/bin/bash
# This is code is used to run openface in v11.
# Jinlong Lin
outputTxt='/data/faces/Landmarks/AFLW/experiments/OpenFace/detections' #the output .pts files which record the annotation information.
outputImages='/data/faces/Landmarks/AFLW/experiments/OpenFace/images_with_detections' # the annotated images.
input='/data/faces/Landmarks/AFLW/aflw/data/flickr_subset' # the input images.

/misc/bin/linux_x86_64_opteron/FaceLandmarkImg -fdir $input -ofdir $outputTxt -oidir $outputImages -q

