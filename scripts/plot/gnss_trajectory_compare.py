#! /usr/bin/env python
# last update 2017.8.17 yimeng
# check gnss trajectory

import rosbag, os
import numpy as np
import pylab as plt

pathName = "/home/yimeng/Documents/data_temp"
class plotTrajectory(object):

	def __init__(self, pathName):

		self.bag_lst = []
		self.bag_name_lst = []
		print "Filepath: %s"%pathName
		for bag_file in os.listdir(pathName):
			print "loading bag file: %s, it may takes seconds .."%bag_file
			self.bag_name_lst.append(bag_file)
			self.bag_lst.append( rosbag.Bag( os.path.join(pathName, bag_file), 'r'))

		self.ptn = 0

	def collect(self, bag_file):

		fix_long, fix_lat, fix_h, fix_status = [], [], [], []

		# with open(self.bag_name_lst[self.ptn][:-3]+"txt", "w") as f:

		for topic, msg, t in bag_file.read_messages(topics=["/nav/fix"]):
			if topic == "/nav/fix":
				fix_long.append(msg.longitude)
				fix_lat.append(msg.latitude)
				fix_h.append(msg.altitude)
				fix_status.append(msg.status.status)

					# f.write("%.9f,%.9f,%.9f\n"%(msg.longitude,msg.latitude,msg.altitude))

		data = np.hstack((np.array(fix_long).reshape(-1,1), \
			np.array(fix_lat).reshape(-1,1), \
			np.array(fix_status, dtype=np.int).reshape(-1,1)) )

		self.ptn += 1
		return data

	def plot(self):

		self.data_lst = []
		self.color_lst = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
		for bag_file in self.bag_lst:
			self.data_lst.append( self.collect(bag_file))

		plt.figure()
		handle_lst = []
		for data_item in enumerate(self.data_lst):
			title_name = self.bag_name_lst[data_item[0]]
			plot_handle, = plt.plot(data_item[1][:,0], data_item[1][:,1], '.'+self.color_lst[data_item[0]], label=title_name, linewidth=0.5)
			handle_lst.append(plot_handle)
		plt.legend(handles=handle_lst, loc=1)
		plt.show()

plotter = plotTrajectory(pathName)
plotter.plot()