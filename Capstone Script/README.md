ConfusionMatrix.py:
The script ConfusionMatrix.py contains functions for computing the convex hull of set of points and the area of this hull. It is used to check TP (true positive), FP (false positive), FN (false negative), and wite down into a table for face detection modules.
ConfusionMatrix .py is a version with libraries. Scipy library is used to get convex hull and area, Polygon library is used to calculate intersection area, pandas is used to load data and drop NaN values
The script solved Convex Hull issues, could handle multi-annotation-faces in one image, and could handle multi-detection-faces for one real face.

The logicality (The threshold is based on accounting on given images, it affected by personal definition):
    If there is a face in original images but the ML modules did not detect any face, the face detector will not write a file or the area of the points will be zero , it is defined as FN (False Negative).
    If the original face area is so different with detected face area, e.g. detected face area is less then half area of original face, or is 1.5x (or more) bigger then original face, This means that the module detect an item which is not a face, It is named as FP (False Positive).
   Otherwise: They are TP (True Positive).
    Notice:
    Since in our test cases, there is a face in every image so logic does not currently account for true negative (TRUE NEGATIVE)

Usage:
    Usage: python ConfusionMatrix.py <annotation file path> <experiment file path> <output file path> <dataset name> <ML modle name>
    Notice:
        1.Plase use Absolute Path.
        2.When you try to use this script for other dataset, please notice the data file of other datasets, and modify the code to match your data file.
        3. As for annotation and experiment file, this script cannot handle with empty file. Please fill at least one NaN (must be NaN, cannot be nan, NAN or others) in the file.
        4. The number of annotation files must be match with the number of experiment files.
    
 Guide to run the scripts:
  Using ConfusionMatrix.py to run the AFLW dataset as an sample:
  Face++:
  python ConfusionMatrix.py ./AFLW_600_Annotation/ ./AFLW_600_Facepp_temp/ ./ AFLW face++ ./config_facepp.csv 21 83
  OpenFace:
  python ConfusionMatrix.py ./AFLW_600_Annotation/ ./AFLW_600_Detection_OpenFace/ ./ AFLW OpenFace ./config_openface.csv 21 68






FaceAccurateCalculator.py:

'''
    The script is used to conduct the computation of the face-size-normalized point-to-point error between a set of predicted and annotated landmark locations, the ideas of script is from the SeanMHendryx's script  DistanceBetweenPoints.py, 
    and add more functions including the support of the multiple faces in one image and the support of dateset which contains the data tuple format "NAN", "NaN".
   - Jinlong Lin
'''

Usage:
  python FaceAccurateCalculator.py <Confusion Table csv file path> <annotation directory> <detection directory> <eye or all> <output file path (optional)>
Notice:
Confusion Table csv file path, it is the csv which indicate the the face has found, not found will be ignored without the computation of the face-size-normalized point-to-point error 
    
Guide to run the scripts(the script is long,such that the pasta is good choice):

AFLW Dataset:
  Face++:
  python FaceAccurateCalculator.py ./AFLW_600_Facepp_Result/AFLW_face++_ConfusionTable.csv AFLW_600_Annotation/ AFLW_600_Detection_Facepp/ all
  python FaceAccurateCalculator.py ./AFLW_600_Facepp_Result/AFLW_face++_ConfusionTable.csv AFLW_600_Annotation/ AFLW_600_Detection_Facepp/ eye
  OpenFace:
  python FaceAccurateCalculator.py ./AFLW_600_OpenFace_Result/AFLW_OpenFace_ConfusionTable.csv AFLW_600_Annotation/ AFLW_600_Detection_OpenFace/ all
  python FaceAccurateCalculator.py ./AFLW_600_OpenFace_Result/AFLW_OpenFace_ConfusionTable.csv AFLW_600_Annotation/ AFLW_600_Detection_OpenFace/ eye
  -Jinlong Lin
300W Dataset:
  [Face++]
  ---300w Indoor images
  python FaceAccurateCalculator.py ./300w_indoor_Face++_ConfusionTable.csv 300w_Indoor_annotation/ 300w_Indoor_Face++_Detection/ all
  python FaceAccurateCalculator.py ./300w_indoor_Face++_ConfusionTable.csv 300w_Indoor_annotation/ 300w_Indoor_Face++_Detection/ eye
  ---300w Outdoor images
  python FaceAccurateCalculator.py ./300w_outdoor_Face++_ConfusionTable.csv 300w_Outdoor_annotation/ 300w_Outdoor_Face++_Detection/ all
  python FaceAccurateCalculator.py ./300w_outdoor_Face++_ConfusionTable.csv 300w_Outdoor_annotation/ 300w_Outdoor_Face++_Detection/ eye
  [OpenFace]
  ---300w Indoor images
  python FaceAccurateCalculator.py ./300w_indoor_OpenFace_ConfusionTable.csv 300w_Indoor_annotation/ 300w_Indoor_OpenFace_Detection/ all
  python FaceAccurateCalculator.py ./300w_indoor_OpenFace_ConfusionTable.csv 300w_Indoor_annotation/ 300w_Indoor_OpenFace_Detection/ eye
  ---300w Outdoor images
  python FaceAccurateCalculator.py ./300w_outdoor_OpenFace_ConfusionTable.csv 300w_Outdoor_annotation/ 300w_Outdoor_OpenFace_Detection/ all
  python FaceAccurateCalculator.py ./300w_outdoor_OpenFace_ConfusionTable.csv 300w_Outdoor_annotation/ 300w_Outdoor_OpenFace_Detection/ eye
