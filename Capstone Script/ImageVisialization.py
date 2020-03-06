import os
from PIL import Image
from PIL import ImageDraw
## Author: Jinlong Lin

#filepath = r"./AFLW_600_Detection_Facepp/image00661_face_0.txt" #Given the dir for landmarks dictionary txt file
#filepath = r"./AFLW_600_Annotation/image02686_face_anno_55923.pts"
filepath = r"./AFLW_600_Detection_OpenFace/image00661_face_0.pts"
#filepath = r"./temp3.txt"
imgpath = r"./600Images/image00661.jpg" #dir for image
#imgpath = r"./Output_Images/image_visualized.jpg" #dir for image
output_path = r"./Output_Images" #Given the dir for visualized images

file = open(filepath,"r")
imgdir = os.path.join(imgpath)
img = Image.open(imgdir)
draw = ImageDraw.Draw(img)

try:
	i = 1
	for line in file:
		if line.strip() != 'NaN':
			x=float(line.strip().split(" ")[0])
			y=float(line.strip().split(" ")[-1])
			draw.text((x,y),"*"+str(i),(225,225,0))
			img.save(os.path.join(output_path,"00661_3.jpg"))
			i += 1
except Exception as e:
	print e
	pass