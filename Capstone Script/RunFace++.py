# This code is usd to ask for Facepp_API to generate the face detection files, face++ can detect the face in the images, and 
# it can output each face into a json file,such that one image with many faces would generate seperate files.
# By Jinlong Lin

import requests
import os
import json

http_url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
key = "99GVokV5jlY-q3Sm4jJb7W8rcQ8WGL8d"
secret = "qAupNc2-ByBW4gz_axZBEID2IuNx5nd5"
filepath = "./600Images"
outputpath = "./AFLW_600_Facepp"

data = {"api_key":key, "api_secret":secret, "return_landmark":1}



for filename in os.listdir(filepath):
    if filename.endswith(""):
        filedir = os.path.join(filepath,filename)
        files = {"image_file": open(filedir, "rb")}  
        try:
            response = requests.post(http_url, data=data, files=files)
        except requests.exceptions.Timeout as e:
            # Maybe set up for a retry, or continue in a retry loop
            print e
        except requests.exceptions.TooManyRedirects as e:
            # Tell the user their URL was bad and try a different one
            print e
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            print e
        req_con = response.content.decode('utf-8')
        #print req_con
        try:
            req_dict = json.loads(req_con)
            for i in range(len(req_dict['faces'])):
            	f = open(os.path.join(outputpath,filename[0:10]+"_face_" + str(i) + ".txt"),"w+")
            	f.write(str(req_dict['faces'][i]))
            	f.close()
        except:
            req_dict = req_con
            #f = open(os.path.join(outputpath,filename[0:11]+"_UNABLE_DECODE.txt"),"w+")
            #f.write(str(req_dict))
            #f.close()
