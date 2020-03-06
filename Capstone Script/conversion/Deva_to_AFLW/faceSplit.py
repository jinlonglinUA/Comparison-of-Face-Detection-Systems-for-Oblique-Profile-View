import sys
import os

'''
1. split detections landmarks of faces from one image into unique file with unique face id
2. Remove unsued data of ConfusionMatrix and Accuracy scprits
3. Convert half face into full face by adding NaN points
'''

def getFileName(path):
	return [os.path.abspath(os.path.join(path,filename)) for filename in os.listdir(path)]

def splitFile(file):
	faces = []
	with open(file, 'r') as fr:
		for line in fr:
			line = [ t for t in line.split(' ') if t != '' ]
			faces.append(line)
	return faces

def saveFile(faces, fileName, path, leftConfig, rightConfig):
	for i, face in enumerate(faces):
		with open(os.path.abspath(os.path.join(path,fileName.split(os.sep)[-1].replace('.txt', "") + '_face_det_' + str(i) + '.pts')), 'w') as fw:
			if len(face) < 100:
				# left face
				config = leftConfig if int(face[0]) > 0 else rightConfig
				face = face[1:-2]
				with open(config, 'r') as lcr:
					for line in lcr:
						line = line.strip().split(',')
						if line[-1] == 'NaN':
							fw.write('NaN\n')
						else:
							index = int(line[-1])-1
							fw.write(str(face[index * 2]) + ' ' + str(face[index * 2 + 1]) + '\n')
			else:
				face = face[1:-2]
				face = iter(face)
				for e in face:
					fw.write(str(e) + ' ' + next(face) + '\n')

def main(argc, argv):
	if argc != 5:
		print("Usage: python faceSplit.py <detection directory> <target diractory> <leftFace.csv> <rightFace.csv>")
		print("detection directory: directory contains face detection file by models")
		print("target directory: the directory you want to save")
		exit()
	else:
		files= getFileName(argv[1])
		for file in files:
			face = splitFile(file)
			saveFile(face, file, argv[2], argv[3], argv[4])

if __name__ == '__main__':
	main(len(sys.argv), sys.argv)


