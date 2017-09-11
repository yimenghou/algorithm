import numpy as np
import os

basepath = "/media/yimeng/0ade5f79-daf5-43f5-9b3f-fbad02d13a32/dataset/gta/data_batch_2"
filepath = os.path.join(basepath, "2017-06-18-21-50.txt")
imagepath = os.path.join(basepath, "2017-06-18-21-50")

with open(filepath, "r") as f:
	data = np.loadtxt(f)

print("total text number: %d"%(len(data)/3))

image_num = len(os.listdir(imagepath))
# for dirs in os.listdir(imagepath):
# 	image_num += len(os.listdir( os.path.join(imagepath, dirs ) ))

print("total image number: %d"%image_num)