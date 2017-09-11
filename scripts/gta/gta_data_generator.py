
import os
import numpy as np

basepath = "/media/yimeng/0ade5f79-daf5-43f5-9b3f-fbad02d13a32/dataset/gta/data_batch_2"
filepath = os.path.join(basepath, "2017-06-18-21-50.txt")
imagepath = os.path.join(basepath, "2017-06-18-21-50")

IMG_SIZE = (480, 640, 3)

with open(filepath) as f:
	velocity = np.loadtxt(f)
	velocity = np.reshape(velocity, (-1, 3)) # [index, yawrate, speed]

img_path = os.path.join(filepath, "image")
img_len = len(os.listdir(img_path))
image_dataset = np.zeros( (img_len, np.prod(IMG_SIZE) ), dtype=np.uint8)
image_labelset = np.zeros( (img_len, 3 ), dtype=np.float)

bar = Bar('Processing', max=len(os.listdir(img_path)))

for img_item in enumerate( sorted(os.listdir(img_path)) ):
	idx = img_item[1][4:-4]
	img = cv2.imread( os.path.join(img_path, img_item[1]) )
	image_dataset[img_item[0], :] = np.array(img, dtype=np.uint8).flatten()
	image_labelset[img_item[0], :] = velocity[int(idx),:]
	bar.next()

bar.finish()

with h5py.File(o_filepath, 'w') as f:
	f.create_dataset('dataset', data = image_dataset)
	f.create_dataset('labelset', data = image_labelset)
