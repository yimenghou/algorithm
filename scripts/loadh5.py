import h5py
import numpy as np
import pylab as plt

filepath = "/media/yimeng/0ade5f79-daf5-43f5-9b3f-fbad02d13a32/dataset/gta/processed_data/train/20170627/65.h5"
with h5py.File(filepath, "r") as f:
	print f.keys()
	dataset = f["dataset"][:]
	labelset = f["labelset"][:]

print dataset.shape

plt.figure()
plt.imshow(np.reshape(dataset[np.random.randint(1000),:], (140, 320, 3)))
plt.show()
