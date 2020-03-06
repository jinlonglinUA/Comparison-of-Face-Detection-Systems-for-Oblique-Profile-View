#! python2/3
# written by jinlong.
import sys
import os
import numpy
import math
import operator
import pprint

def openFolder(path, suffix):
    return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(suffix)]

def readFile(fr, pos):
    l = [tuple(map(float, coor.split(" "))) for i, coor in enumerate(fr) if i in pos and not "NaN" in coor ] 
    return l if l != [] else [(0,0),(0,0)]
        
def loadData(path, pos, suffix = ""):
    return {file.split(os.sep)[-1].replace(suffix, ""): operator.itemgetter(0,-1)(readFile(open(file, "r"), pos)) for file in openFolder(path, suffix)}
        
def line_slope(points):
    if points[0][0] == points[1][0]:
        return float("inf")
    try:
        x_coords, y_coords = zip(*points)
        return float('%.4f' % math.degrees(numpy.arctan(abs(numpy.polyfit(x_coords, y_coords, 1)[0]))))
    except:
        return float("inf")
        
def ConfusionMatrix(file):
    with open(file, "r") as fr:
        return{line.split(",")[0] : int(line.split(",")[1]) for line in fr if "TP" not in line}

def mark_file(key, table):
    return key+" (detected)" if table[key] == 1 else key+" (undetected)"

def print_obj(data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)
    
def readme():
    if len(sys.argv) != 3:
        #Usage:python slope.py ./AFLW_600_Annotation ./AFLW_600_Facepp_Result/AFLW_face++_ConfusionTable.csv
        #Usage:python slope.py /AFLW_600_Annotation /AFLW_600_OpenFace_Result/AFLW_OpenFace_ConfusionTable.csv
        print("Usage: python2/3 slope.py <path to folder> <path to Confusion Matrix Table file>")
        print("Notice: the folder contains the annotation files")
        print("Notice: Line 38, slope.py files. Manully change the numbers in [,], which represent the line number used for getting eye corner landmarks")
        exit() 
    
if __name__ == "__main__":
    readme()
    cmt = ConfusionMatrix(os.path.abspath(sys.argv[2]))
    slope = {mark_file(key, cmt): line_slope(value) for key, value in loadData(os.path.abspath(sys.argv[1]), [36, 45, 42, 39], ".pts").items()}
    undetect_group = {}
    group_all = {}
    for w in sorted(slope.items(), key=operator.itemgetter(1)):
        if w[1] == float("inf"):
                pass
        if w[1] <= 14:
            if '0-14' not in group_all:
                group_all['0-14'] = []
            group_all['0-14'].append(w)
        elif w[1] <= 29:
            if '15-29' not in group_all:
                group_all['15-29'] = []
            group_all['15-29'].append(w)
        elif w[1] <= 44:
            if '30-44' not in group_all:
                group_all['30-44'] = []
            group_all['30-44'].append(w)
        elif w[1] <= 59:
            if '45-59' not in group_all:
                group_all['45-59'] = []
            group_all['45-59'].append(w)
        elif w[1] <= 74:
            if '60-74' not in group_all:
                group_all['60-74'] = []
            group_all['60-74'].append(w)
        else:
            if '75-90' not in group_all:
                group_all['75-90'] = []
            group_all['75-90'].append(w)

        if "undetected" in w[0]:
            if w[1] == float("inf"):
                pass
            if w[1] <= 14:
                if '0-14' not in undetect_group:
                    undetect_group['0-14'] = []
                undetect_group['0-14'].append(w)
            elif w[1] <= 29:
                if '15-29' not in undetect_group:
                    undetect_group['15-29'] = []
                undetect_group['15-29'].append(w)
            elif w[1] <= 44:
                if '30-44' not in undetect_group:
                    undetect_group['30-44'] = []
                undetect_group['30-44'].append(w)
            elif w[1] <= 59:
                if '45-59' not in undetect_group:
                    undetect_group['45-59'] = []
                undetect_group['45-59'].append(w)
            elif w[1] <= 74:
                if '60-74' not in undetect_group:
                    undetect_group['60-74'] = []
                undetect_group['60-74'].append(w)
            else:
                if '75-90' not in undetect_group:
                    undetect_group['75-90'] = []
                undetect_group['75-90'].append(w)
            #print(w)

    for key in undetect_group:
        print(key, end=' :')
        print(str(len(undetect_group[key]) / len(group_all[key]) * 100) + "%")
        print(str(len(undetect_group[key])) +  "/"  + str(len(group_all[key])))
        print()


        
        

    