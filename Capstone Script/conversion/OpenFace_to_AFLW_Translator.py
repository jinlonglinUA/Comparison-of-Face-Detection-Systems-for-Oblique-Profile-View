'''
this is a python script which can translate openface 68 points to the form of AFLW 21 points
Name: Jinlong Lin
'''

import os
output_path="/Users/jinlonglin/Desktop/Outdoor_Output" #Given the dir for txt file which store OpenFace 68 points
file_path="/Users/jinlonglin/Desktop/OpenFace_21Points/Outdoor_Output" #Given the dir for converted txt file whose format is AFLW 21 points
time=0
for file in os.listdir(file_path):
        #Import the result from Face++
		file2=os.path.join(file_path,file)
        
        #Convert the result
		fp=open(file2,"r")
		aflw=[]
		lines=fp.readlines()
		aflw.insert(1,lines[20]) 
		aflw.insert(2,lines[22]) 
		aflw.insert(3,lines[24]) 
		aflw.insert(4,lines[25]) 
		aflw.insert(5,lines[27]) 
		aflw.insert(6,lines[29]) 
		aflw.insert(7,lines[39])

		# aflw.insert(lines[20]) 8
		data01=lines[39].split()
		data02=lines[42].split()
		value8_x=(float(data01[0])+float(data02[0]))/2
		value8_y=(float(data01[1])+float(data02[1]))/2
		point8=str(value8_x)+" "+str(value8_y)+'\n'
		aflw.insert(8,point8)

		aflw.insert(9,lines[42]) 
		aflw.insert(10,lines[45]) 


		# aflw.insert(lines[45]) 11
		data01=lines[45].split()
		data02=lines[48].split()
		value11_x=(float(data01[0])+float(data02[0]))/2
		value11_y=(float(data01[1])+float(data02[1]))/2
		point11=str(value11_x)+" "+str(value11_y)+'\n'
		aflw.insert(11,point11)

		aflw.insert(12,lines[48]) 
		aflw.insert(13,lines[5]) 
		aflw.insert(14,lines[34]) 
		aflw.insert(15,lines[36]) 
		aflw.insert(16,lines[38]) 
		aflw.insert(17,lines[17]) 
		aflw.insert(18,lines[51]) 

		# aflw.insert(lines[45]) 19
		data01=lines[65].split()
		data02=lines[69].split()
		value19_x=(float(data01[0])+float(data02[0]))/2
		value19_y=(float(data01[1])+float(data02[1]))/2
		point19=str(value19_x)+" "+str(value19_y)+'\n'
		aflw.insert(19,point19)

		aflw.insert(20,lines[57]) 
		aflw.insert(21,lines[11]) 

        #Store the results
		result=os.path.join(output_path,file)
		output=open(result,"w")
		for item in aflw:
			output.write(item)
