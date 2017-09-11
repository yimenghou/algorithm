
from utils import *
import pylab as plt
import numpy as np
import os

ORG_IMG_SIZE = (240,320,3)

filepath = "/home/yimeng/Documents/dataset/dump/0601"
filename_lst = os.listdir(filepath)

for item in filename_lst:

	filename = os.path.join(filepath, item)
	print "Loading %s"%filename
	dataset, labelset = loadDumpData(filename)
	dataset_f, labelset_f = flipHorizontal(dataset, labelset, ORG_IMG_SIZE, None)
	saveDumpData(filename+".f", dataset_f, labelset_f)