# the script to count the number of undetected images coordinates points from the annoation files.
# Anthor : Jinlong Lin

import sys
import os
import pprint
import operator
from collections import Counter


#python invalid_statistics.py ./AFLW_600_Annotation ./AFLW_600_Facepp_Result/AFLW_face++_ConfusionTable.csv
def openFolder(path, suffix = '.pts'):
    return { f.replace(suffix, "") : os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(suffix)}

def count(files, path):
	dic = {}
	with open(path) as fr:
		for line in fr:
			line_num = 0
			if line.split(',')[1] == '0':
				with open(files[line.split(',')[0]]) as dr:
					for row in dr:
						if 'NaN' not in row:
							line_num += 1
				dic[line.split(',')[0]] = line_num
	return dic

def print_obj(data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)

if __name__ == '__main__':
	files = openFolder(os.path.abspath(sys.argv[1]))
	dic_data = count(files, os.path.abspath(sys.argv[2]))
	# sorted result
	sort_data = sorted(dic_data.items(), key=operator.itemgetter(1))
	average = sum(dic_data.values()) / len(dic_data.values())
	mode = Counter(dic_data.values()).most_common(1)
	print_obj(sort_data)
	print("average %d, mode %d" % (average, mode[0][0]))
	c = 0
	dic = Counter(dic_data.values())
	for key in dic:
		if key <= 11:
			c += dic[key]
	print("The Number of face is half face: ")
	print(c)