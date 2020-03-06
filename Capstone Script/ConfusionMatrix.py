"""
    This code is used to perform the calculation and statistic of the confusion matrix of face detections.
    Its formula is to calculate "the intersection area of two faces/The union area of two faces"
    We use the result of formula as threshold to declare that if the model detect a face correct or not,
    as default, the threshold is 0.5. We may change in future work.
    
    Jinlong Lin
"""

from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
from glob import glob
import numpy as np
import pandas as pd
import sys
#import glob, os

def readLandmarkFile(anno, det):
    """
    Reads in landmark file from a path and returns a numpy array
    Assumes landmark file has nothing but coordinates e.g. command-f ex.txt:
    Using pandas library could earier to drop coordinates with NaN value

    """
    data = {}
    anno_fnames = glob(anno+"/*")
    for anno_file in anno_fnames:
    	anno_imageID = anno_file.split("/")[-1].split("_face_")[0]
    	anno_faceID = anno_file.split("/")[-1].split("_face_")[1].split(".")[0]
    	if anno_imageID not in data:
    		data[anno_imageID] = {}
    	if anno_faceID not in data[anno_imageID]:
		data[anno_imageID][str(anno_faceID)] = pd.read_csv(anno_file,delimiter=" ", header=None,  skip_blank_lines=True, error_bad_lines=False, names=list('xy'))
        det_fnames = glob(det+"/*")
    	for det_file in det_fnames:
    		det_imageID = det_file.split("/")[-1].split("_face_")[0]
    		det_faceID = det_file.split("_face_")[1].split(".")[0]
    		if det_imageID == anno_imageID:
    			data[anno_imageID][str(det_faceID)] = pd.read_csv(det_file,delimiter=" ", header=None,  skip_blank_lines=True, names=list('xy'))
    return data

def trace_data(data):
	'''
	Editor: Jinlong

	'''
	format_f = open(sys.argv[6], 'r')
	anno_len = int(sys.argv[7])
	det_len = int(sys.argv[8])
	anno_drop = [i for i in range(anno_len)]
	anno_reminder = []
	det_drop = [i for i in range(det_len)]
	det_reminder = []
	for line in format_f:
		line = line.strip().split(',')
		if line[1] != 'NaN' and line[0] != 'NaN':
			anno_reminder.append(int(line[0]) - 1)
			det_reminder.append(int(line[1]) - 1)
	
	anno_drop = list(filter(lambda x: x not in anno_reminder, anno_drop))
	det_drop = list(filter(lambda x: x not in det_reminder, det_drop))

	for imageID in sorted(data):
		anno_list = [anno for anno in data[imageID] if anno.startswith('anno')]
		det_list = [det for det in data[imageID] if det.startswith('det')]
		for annoID in anno_list:
			if len(data[imageID][annoID].dropna(axis = 0, how = "any").values) > min(anno_len, det_len):
				data[imageID][annoID] = data[imageID][annoID].drop(anno_drop)
			data[imageID][annoID] = data[imageID][annoID].dropna(axis = 0, how = "any").values
		for detID in det_list:
			if len(data[imageID][detID].dropna(axis = 0, how = "any").values) > min(anno_len, det_len):
				data[imageID][detID] = data[imageID][detID].drop(det_drop)
			data[imageID][detID] = data[imageID][detID].dropna(axis = 0, how = "any").values
	#usage for print certain image landmarks
	#print(data["image<number>"])
	#print(data['image22675'])

def confusionAnalysis(data):
	"""
	Iterate every image from dataset, and for each iamge, iterate every annotation. In each annotation, find out each
	detection with same image id.
	Compare each detection with each annotation with same image id, and count the number of 
	TruePositive, FalsePositve, and FalseNegative
	"""
	FN = FP = TP = 0
	try:
		fileWriter = open(sys.argv[3]+'/'+sys.argv[4] + "_" + sys.argv[5] + "_ConfusionTable.csv", 'w')
	except IOError, e:
		print "open failed\n"
		sys.exit()
	fileWriter.write("ImageID,TP,landmarks_file_ID_pridiction\n")
	#edit: Jinlong
	trace_data(data)
	for imageID in sorted(data):
		anno_list = [anno for anno in data[imageID] if anno.startswith('anno')]
		det_list = [det for det in data[imageID] if det.startswith('det')]
		currTP = 0
		for annoID in anno_list:
			annotation_hull, annotation_area = getConvexHullPoints_and_Area(data[imageID][annoID])
			flag = True
			for detID in det_list:
				#print detID
				detection_hull, detection_area = getConvexHullPoints_and_Area(data[imageID][detID])
				intersection_area = getIntersectionArea(annotation_hull, detection_hull)
				#usage for print certain image intersection / union
				if intersection_area / (annotation_area + detection_area - intersection_area) > 1:
					print "Error"
				if intersection_area / (annotation_area + detection_area - intersection_area) > 0.5:
					fileWriter.write(str(imageID)+'_face_'+str(annoID)+","+"1"+","+str(imageID)+'_face_'+str(detID)+"\n")
					data[imageID].pop(detID)
					det_list.remove(detID)
					TP += 1
					currTP += 1
					flag = False
			if flag:
				fileWriter.write(str(imageID)+'_face_'+str(annoID)+","+"0"+","+"/" + "\n")
		FP += len(data[imageID]) - len(anno_list)
		# if (imageID == 'image02686'):
		#  	print data[imageID][detID]
		#  	exit()
		FN += len(anno_list) - currTP
	return [FN, FP, TP]

def getConvexHullPoints_and_Area(points):
	"""
	:param points: 2-d numpy array where each row is a vertex, the first column is x and the second column is y.
	:return the points of ConvexHull points, and the area of the hull
	
	using scipy library
	Note: convex_hull.volume is not a typo. The "valume" of 2D images is the hull area
	"""
	if len(points) == 0:
		return [[],-1]
	convex_hull = ConvexHull(points)
	convex_points =  np.array(np.dstack([points[convex_hull.vertices,0], points[convex_hull.vertices,1]]).tolist()[0])
	convex_area = convex_hull.volume
	return convex_points, convex_area

def getIntersectionArea(pts1, pts2):
	"""
	:param points: 2-d numpy array where each row is a vertex, the first column is x and the second column is y.
				   both pts1 and pts2 are convext hull points
	:return the area of the intersection hull
	
	using shapely library
	"""
	if (len(pts1) == 0 or len(pts2) == 0):
		return -1;
	face1 = Polygon(pts1)
	face2 = Polygon(pts2)
	return face1.intersection(face2).area


def main():
	if len(sys.argv) != 9:
		print "Usage: python ConfusionMatrix.py <annotation file path> <experiment file path> <output file path> <dataset name> <ML modle name>"
		sys.exit()

	data = readLandmarkFile(sys.argv[1], sys.argv[2])
	FN, FP, TP = confusionAnalysis(data);

	try:
		fileWriter = open(sys.argv[3]+'/'+sys.argv[4] + "_" + sys.argv[5] + "_ConfusionAnalysis.txt", 'w')
	except IOError, e:
		print "open failed\n"
		print sys.argv[3]+'/'+sys.argv[4] + "_" + sys.argv[5] + "_ConfusionAnalysis.txt"
		sys.exit()

	fileWriter.write("\tPositive\tNegative\n")
	fileWriter.write("True\t"+str(TP)+"\t\t/\n")
	fileWriter.write("False\t"+str(FP)+"\t\t"+str(FN)+"\n")
	fileWriter.write("F1\t" + str(2*TP*1.0/(2*TP+FP+FN))  + "\n")
	fileWriter.close()

if __name__ == '__main__':
	main()
