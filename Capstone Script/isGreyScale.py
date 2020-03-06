from PIL import Image
import sys
import os
from os import listdir
from os.path import isfile, join
from shutil import copyfile

def getImages(mypath):
	return [f for f in listdir(mypath) if isfile(join(mypath, f))]


def getImageName(file, path):
	image_list = []
	with open(file) as fr:
		for line in fr:
			if line.strip().split(',')[1] == '0':
				image = line.strip().split(',')[0].split('_')[0] + '.jpg'
				image_list.append(image)
	return image_list


def is_grey_scale(img_path):
    img = Image.open(img_path).convert('RGB')
    w,h = img.size
    for i in range(w):
        for j in range(h):
            r,g,b = img.getpixel((i,j))
            if r != g != b: return False
    return True


def extractFile(file, origin, target):
	source_file = os.path.abspath(os.path.join(origin,file))
	target_file = os.path.abspath(os.path.join(target,file))
	print(source_file, target_file)
	try:
		copyfile(source_file, target_file)
	except:
		copyfile(source_file.replace('.jpg', '.png'), target_file)


# images = getImages(sys.argv[2])
# gray_all = 0
# for i, image in enumerate(images):
# 	print("\r             \r %d / %d" % (i, len(images)), end="")
# 	gray_all += 1 if is_grey_scale(image) else 0
# print("\r             \r %d" % gray_all)

images = getImageName(sys.argv[1], sys.argv[2])
gray = 0
for i, image in enumerate(images):
	print("\r             \r %d / %d" % (i, len(images)), end="")
	gray += 1 if is_grey_scale(image) else 0
print("\r             \r %d / %d" % (gray, gray_all))

# images = getImageName(sys.argv[1], sys.argv[2])
# for i, image in enumerate(images):
# 	print("\r             \r %d / %d" % (i, len(images)), end="")
# 	if is_grey_scale(join(sys.argv[2], image)):
# 		extractFile(image, sys.argv[2], sys.argv[3])



