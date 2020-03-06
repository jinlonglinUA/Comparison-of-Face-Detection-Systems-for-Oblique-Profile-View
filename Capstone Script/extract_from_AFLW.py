# Edit by Jinlong Lin
# it is to connect to sqlite3 database to extract the information from database

#!/usr/bin/python

import sqlite3 as lite
import sys
import csv
import os

location=os.getcwd()
conn = lite.connect('aflw.sqlite')


for file in os.listdir(location):
	if file.startswith("image") and file.endswith(".csv"):
		with open(os.path.join(location,file)) as myfile:
			print "start translate"
			lines=myfile.readlines()
			l=[e.strip() for e in lines]
			l=list(map(str,l))
			for string in l:
					name1="%s_"%os.path.splitext(myfile.name)[0] 
					filename2=name1+"%s.pts"%string
					with open(filename2,"wb") as f:
						cur = conn.cursor()
						for row in cur.execute('''Select feature_id, x , y from FeatureCoords where face_id=%s'''%string):
							writeRow=",".join([str(i) for i in row])
							f.write(writeRow.encode()+'\n')
	else:
		print "errors found"

cur.close()
conn.close()