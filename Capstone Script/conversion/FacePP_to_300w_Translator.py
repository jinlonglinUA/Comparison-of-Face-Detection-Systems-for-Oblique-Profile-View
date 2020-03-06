'''
    This code convert the Face++ results of Landmarks 83 points(json dictionary) to OpenFace 68 points format(plain text). 
    New update:now each face in one image can generate a json file, one image can have many face which store into different files.
    Name: Jinlong Lin
'''


import os

filepath = r"./AFLW_600_Facepp" #Given the dir for txt file which store Face++ 83 points
output_path = r"./AFLW_600_Detection_Facepp" #Given the dir for converted txt file whose format is OpenFace 68 points
Index_in_Facepp_output= [2,3,4,5,6,7,8,9,1,18,
                17,16,15,14,13,12,11,30,35,36,
                37,34,76,81,82,83,80,0,0,0,
                65,63,58,59,62,64,22,28,29,26,
                24,23,68,74,75,72,70,69,38,50,
                49,55,52,53,47,44,45,39,42,41,
                0,51,48,54,0,43,46,40]

for filename in os.listdir(filepath):
    #load the dic file which store the Face++ 83 points
    filedir = os.path.join(filepath,filename)
    file = open(filedir,"r")
    dic = eval(file.read())
    
    #Transform the Face++ 83 points to corresponding OpenFace 68 points
    #print filename
    if 'landmark' not in dic:
        continue;
    keys = sorted(list(dic['landmark'].keys()))
    Facepp_output_in_openFace_format = ""
    for index in Index_in_Facepp_output:
        if index != 0:
            x = dic['landmark'][keys[index-1]]['x']
            y = dic['landmark'][keys[index-1]]['y']
            Facepp_output_in_openFace_format += str(x) + " " + str(y) + '\n'
        else:
            Facepp_output_in_openFace_format += "NaN" + '\n'

    #output the new file to target location which store the OpenFace 68 points.
    resultdir = os.path.join(output_path,filename)
    result = open(resultdir,"w+")
    result.write(Facepp_output_in_openFace_format)
    result.close()
    
