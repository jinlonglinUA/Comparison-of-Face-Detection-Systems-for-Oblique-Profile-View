'''
    The script is used to conduct the computation of the face-size-normalized point-to-point error between a set of predicted and annotated landmark locations, the ideas of script is from the SeanMHendryx's script  DistanceBetweenPoints.py, 
    and add more functions including the support of the multiple faces in one image and the support of dateset which contains the data tuple format "NAN", "NaN".
    Author: Jinlong Lin
 	How to run:
 	Face++:
  	python FaceAccurateCalculator.py ./AFLW_600_Facepp_Result/AFLW_face++_ConfusionTable.csv AFLW_600_Annotation/ AFLW_600_Detection_Facepp/ all
  	python FaceAccurateCalculator.py ./AFLW_600_Facepp_Result/AFLW_face++_ConfusionTable.csv AFLW_600_Annotation/ AFLW_600_Detection_Facepp/ eye
  	OpenFace:
  	python FaceAccurateCalculator.py ./AFLW_600_OpenFace_Result/AFLW_OpenFace_ConfusionTable.csv AFLW_600_Annotation/ AFLW_600_Detection_OpenFace/ all
  	python FaceAccurateCalculator.py ./AFLW_600_OpenFace_Result/AFLW_OpenFace_ConfusionTable.csv AFLW_600_Annotation/ AFLW_600_Detection_OpenFace/ eye

'''
import sys
import os
import math
from numpy import nanmedian

# find matching annotation file and detection file
def matchFile(file, anno_drit, det_drit):
	file = open(file, "r")
	lines = file.readlines()[1:]
	file.close()
	anno_extension = os.listdir(anno_drit)[0].strip().split('.')[-1]
	det_extension  = os.listdir(det_drit)[0].strip().split('.')[-1]
	match_files = []
	for line in lines:
		line = line.strip().split(",")
		if line[1] == '0':
			continue
		else:
			match_files.append([anno_drit + '/' + line[0]  + "." +  anno_extension, det_drit + '/' + line[2] + "." + det_extension])
	return match_files

# read coordinate data in each file 
def readFile(anno, det):
	anno_landmarks = []
	det_landmarks  = []

	with open(anno) as anno_file, open(det) as det_file: 
	    for anno_data, det_data in zip(anno_file, det_file):
	        if 'NaN' in anno_data or 'NaN' in det_data:
	        	anno_landmarks.append((float('-inf'), float('-inf')))
	        	det_landmarks.append((float('-inf'), float('-inf')))
	        else:
	        	anno_data = anno_data.strip().split('\t')
	        	anno_landmarks.append((float(anno_data[0]), float(anno_data[1])))
	        	det_data = det_data.strip().split(' ')
	        	det_landmarks.append((float(det_data[0]), float(det_data[1])))
	return anno_landmarks, det_landmarks

# calucalate euclidean distance
def euclideanDistance(anno, det, domain):
	left = []
	right = []
	if det == None:
		for index, anno_coor in enumerate(anno):
			left = anno_coor if index == 35 else left
			right = anno_coor if index == 45 else right
		return math.hypot(left[0] - right[0], left[1] - right[1])
	if len(anno) != len(det):
	    raise ValueError('annotation and detection must have the same shape.')
	dims = len(anno)
	dist = []
	check = []
	for index, (anno_coor, det_coor) in enumerate(zip(anno, det)):
		if index not in domain or float('-inf') in anno_coor or float('-inf') in det_coor:
			continue
		else:
			dist.append(math.hypot(anno_coor[0] - det_coor[0], anno_coor[1] - det_coor[1]))
	return dist

# do normalization
def meanOfInterocularNormalizedDistance(ground_truth, face_dist):
	distance = sum(face_dist)
	#Jinlong Lin: Print the result for each image: print (distance)
	count = len(face_dist)
	return distance / (count * ground_truth) 

def main():
	if len(sys.argv) < 4:
		print('Usage: python FaceAccurateCalculator.py <Confusion Table csv file> <annotation drictory> <detection directory> <eye or all> <output file>')
	match_file = matchFile(sys.argv[1], sys.argv[2], sys.argv[3])
	normalized_errors = []
	for files in match_file:
		anno, det = readFile(files[0], files[1])
		domain = range(0,68) if sys.argv[4] == 'all' else range(35,46)
		face_dist = euclideanDistance(anno, det, domain)
		interocular_dist =  euclideanDistance(anno, None, None)
		normalized_errors.append(meanOfInterocularNormalizedDistance(interocular_dist, face_dist))
	#print normalized_errors
	median_normalized_errors = nanmedian(normalized_errors)
	print("Median normalized error conditioned on being true positive face: {}".format(median_normalized_errors))
	if len(sys.argv) == 6:
		outFile = open(sys.argv[5], "w")
		outFile.write("Median normalized error conditioned on being true positive face: {}".format(median_normalized_errors))
	
if __name__ == '__main__':
    main()

