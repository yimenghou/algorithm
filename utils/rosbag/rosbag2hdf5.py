# -*- coding: UTF-8 -*-
#! /usr/bin/env python

import rosbag, os, h5py, cv2, struct, copy, time, yaml
import pylab as plt, numpy as np
from progress.bar import IncrementalBar
from cv_bridge import CvBridge, CvBridgeError

"""
Convert rosbags in the source path into hdf5 files in the target path

bag_path: input bagfile path, where you put the bagfiles into
h5_path: output hdf5 path, where you want to dump hdf5 files
topic_list: the topics which will be saved into h5 files

2017.06.14 Yimeng
"""

bag_path = "/home/yimeng/Documents/ningbo_port/bag" #"/home/yimeng/Documents/dataset/rosbag" 
h5_path  = "/home/yimeng/Documents/ningbo_port/h5"
topic_list = ["/nav/fix", "/nav/status", "/usb_cam/image_raw", "/velodyne_points"]

class rosbag2hdf5(object):

	def __init__(self, bag_path=None, h5_path=None):

		# dirname, self.bag_filename = os.path.split(os.path.abspath(bag_path))

		self.bag_path = bag_path
		self.bag_filelist = os.listdir(bag_path)
		
		if h5_path !=None:
			self.h5_path = h5_path
		else:
			self.h5_path = bag_path

		print "bag path (input path)", self.bag_path
		print "h5 path (output path)", self.h5_path

		self.greyscale = False # convert images into greyscale? 
		self.img_size = (480, 640, 3)
		self.batch_num = 0
		self.batch_size = 5000

		self.bridge = CvBridge()

	def collect(self, topic_list):

		data_num = np.zeros(4, dtype=np.int)

		for bag_file in self.bag_filelist:

			print "loading bag file: ", bag_file
			bag_temp = rosbag.Bag( os.path.join(self.bag_path, bag_file), 'r')

			info_dict = yaml.load(bag_temp._get_yaml_info())

			for topic_item in info_dict["topics"]:
				for i in range(len(topic_list)):
					if topic_item["topic"] == topic_list[i]:
						data_num[i] = topic_item["messages"]

			data_pose = np.zeros((self.batch_size, 6), dtype=np.float)
			data_status = np.zeros((self.batch_size, 2), dtype=np.int)

			if self.greyscale:
				data_image = np.zeros((self.batch_size, np.prod(self.img_size)/3), dtype=np.uint8)
			else:				
				data_image = np.zeros((self.batch_size, np.prod(self.img_size)), dtype=np.uint8)

			# data_lidar = np.zeros((self.batch_size, 1000000), dtype=np.uint8)			

			bar = IncrementalBar('Processing messages', max=np.sum(data_num))

			cout = np.zeros(4, dtype=np.int) 
			cout_tot = np.zeros(4, dtype=np.int)
			for topic, msg, t in bag_temp.read_messages(topics=topic_list):				

				if topic == "/nav/fix":
					data_pose[cout[0], 0] = msg.pose.position.x
					data_pose[cout[0], 1] = msg.pose.position.y
					data_pose[cout[0], 2] = msg.pose.orientation.x
					data_pose[cout[0], 3] = msg.pose.orientation.y
					data_pose[cout[0], 4] = msg.pose.orientation.z
					data_pose[cout[0], 5] = msg.pose.orientation.w	
					cout[0] += 1

				if topic == "/nav/status":		
					data_status[cout[1], 0] = msg.gps
					data_status[cout[1], 1] = msg.satellite
					cout[1] += 1

				if topic == "/usb_cam/image_raw":
					img_array = self.bridge.imgmsg_to_cv2(msg, "rgb8")
					if self.greyscale:
						img_array = cv2.cvtColor(np.reshape(img_array, self.img_size), cv2.COLOR_RGB2GRAY).flatten()
					else:
						img_array = img_array.flatten()
					data_image[cout[2], :] = img_array
					cout[2] += 1

				bar.next()

				if (bar.index+1)%self.batch_size == 0:

					self.save(bag_file, topic_list, \
						data_pose[:cout[0],  :],\
						data_status[:cout[1],:],\
						data_image[:cout[2], :])

					cout_tot += cout				
					cout = np.zeros(4, dtype=np.int)

				# if topic == "/velodyne_points":
				# 	point_tuple = struct.unpack("B"*len(msg.data), msg.data)
				# 	point_array = np.asarray(point_tuple)
				# 	data_lidar[cout[3], :len(msg.data)] = point_array
				# 	cout[3] += 1

			bar.finish()
			del bag_temp

			self.save(bag_file, topic_list, \
				data_pose[:cout[0],  :],\
				data_status[:cout[1],:],\
				data_image[:cout[2], :])
	
	def save(self, bag_file, topic_list, data_pose, data_status, data_image):

		h5_dump_path = os.path.join(self.h5_path, bag_file[:-4]+"-part"+str(self.batch_num)+".h5")
		# h5_dump_path = os.path.join(self.h5_path, bag_file[:-4]+".h5")

		with h5py.File(h5_dump_path, 'w') as f:																												
			print "\ndumping to path: %s"%h5_dump_path

			if "/nav/fix" in topic_list:
				f.create_dataset('nav_fix', data = data_pose)
			if "/nav/status" in topic_list:
				f.create_dataset('nav_status', data = data_status)
			if "/usb_cam/image_raw" in topic_list:
				f.create_dataset('camera_image', data = data_image)
			# if "/velodyne_points" in topic_list:
			# 	f.create_dataset('lidar_point', data = self.data_lidar)

		self.batch_num += 1

def loadH5(h5_path, topic_list):
	
	h5_filelist = os.listdir(h5_path)
	data_pose_lst, data_status_lst, data_img_lst, data_lidar_lst = [],[],[],[]

	for h5_file in sorted(h5_filelist):

		print "loading file: ", h5_file
		with h5py.File(os.path.join(h5_path, h5_file), "r") as f:

			if "/nav/fix" in topic_list:
				data_pose_lst.append( f['nav_fix'][:] )
				print "> nav_fix loaded"
			if "/nav/status" in topic_list:
				data_status_lst.append( f['nav_status'][:] )
				print "> nav_status loaded"
			if "/usb_cam/image_raw" in topic_list:
				data_img_lst.append( f['camera_image'][:] )
				print "> camera_image loaded"
			# if "/velodyne_points" in topic_list:
			# 	data_lidar_lst.append( f['lidar_point'][:] )
			# 	print "/velodyne_points loaded"

	data_pose_nparray = np.vstack(data_pose_lst)
	data_status_nparray = np.vstack(data_status_lst)
	data_img_nparray  = np.vstack(data_img_lst)

	print "loaded %d files in total"%len(h5_filelist)
	print "nav_fix shape:", data_pose_nparray.shape
	print "nav_status shape:", data_status_nparray.shape
	print "img shape:", data_img_nparray.shape

	return data_pose_nparray, data_status_nparray, data_img_nparray

if __name__ == "__main__":

	worker0 = rosbag2hdf5(bag_path, h5_path)
	worker0.collect(topic_list)

	# loadH5(h5_path, topic_list)