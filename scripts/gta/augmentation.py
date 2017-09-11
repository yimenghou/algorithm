from progress.bar import IncrementalBar
import h5py, os
import numpy as np
import pylab as plt

train_data_path = "/media/yimeng/0ade5f79-daf5-43f5-9b3f-fbad02d13a32/dataset/gta/20170628"

dump_path = "/media/yimeng/0ade5f79-daf5-43f5-9b3f-fbad02d13a32/dataset/gta/processed_data/train/20170628"

IMG_SIZE = (240, 320, 3)
IMG_RESIZE = (140, 320, 3)
CROP_BORD = (60, 200, 0, 320)

tr_data_o = np.zeros((1000, np.prod(IMG_RESIZE)), dtype=np.uint8)
tr_data_f_o = np.zeros((1000, np.prod(IMG_RESIZE)), dtype=np.uint8)
tr_label_processed = np.zeros((1000, 1), dtype=np.float32)

tot_h5_num = sum([len(files) for r, d, files in os.walk(train_data_path)])

# train
p_bar = IncrementalBar("Processing", max=tot_h5_num)

for h5_dir in os.listdir(train_data_path):
	dir_h5_list = os.listdir( os.path.join(train_data_path, h5_dir))
	for h5_file in dir_h5_list:

		with h5py.File( os.path.join(train_data_path, h5_dir, h5_file), "r") as f:
			tr_data = f['dataset'][:]
			tr_label = f['labelset'][:]

			for i in range(tr_data.shape[0]):
				img = tr_data[i,:].reshape(IMG_SIZE)
				img_resize = img[CROP_BORD[0]:CROP_BORD[1], CROP_BORD[2]:CROP_BORD[3]]
				img_flip = np.fliplr(img_resize) 

				tr_data_o[i,:] = img_resize.flatten()
				tr_data_f_o[i,:] = img_flip.flatten()
				tr_label_processed[i] = tr_label[i,1]

		with h5py.File( os.path.join(dump_path, str(p_bar.index)+".h5"), "w") as f:
			f.create_dataset('dataset', data = tr_data_o)
			f.create_dataset('labelset', data = tr_label_processed)
		with h5py.File( os.path.join(dump_path, str(p_bar.index)+"_f.h5"), "w") as f:
			f.create_dataset('dataset', data = tr_data_f_o)
			f.create_dataset('labelset', data = -tr_label_processed)

		p_bar.next()


p_bar.finish()


# with h5py.File( os.path.join(dump_path, "0.h5"), "r") as f:
# 	tr_data = f['dataset'][:]
# 	tr_label = f['labelset'][:]
# with h5py.File( os.path.join(dump_path, "0_f.h5"), "r") as f:
# 	tr_data_f = f['dataset'][:]
# 	tr_label_f = f['labelset'][:]

# img = tr_data[12,:].reshape(IMG_RESIZE)
# img_f = tr_data_f[12,:].reshape(IMG_RESIZE)


# plt.figure()
# plt.subplot(121)
# plt.title("%.4f"%tr_label[12])
# plt.imshow(img)
# plt.subplot(122)
# plt.title("%.4f"%(-tr_label[12]))
# plt.imshow(img_f)
# plt.show()

# data[rand_flip_idx] = np.fliplr(tr_data)
# label[rand_flip_idx, 0] = -label[rand_flip_idx, 0]

# img = tr_data[12:14, :] 
# img_reshape = np.reshape(img[0,:], (240,320,3))
# img_flip = np.fliplr(img)
# img_reshape_clip = np.reshape(img_flip[0,:], (240,320,3))
# plt.figure()
# plt.subplot(121)
# plt.imshow(img_reshape)
# plt.subplot(122)
# plt.imshow(img_reshape_clip)
# plt.show()