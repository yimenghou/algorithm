#! /usr/bin/env python
# last update 2017.9.10 yimeng
# check gnss trajectory

import rosbag, os, argparse
import numpy as np
import matplotlib.pylab as plt
from matplotlib.ticker import FormatStrFormatter

class plotTrajectory(object):

	def __init__(self, fileName):

		print "loading bag file from: %s it may takes seconds .."%fileName
		self.bag = rosbag.Bag(fileName, 'r')
		self.gnss_data_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

	def collect(self):

		for topic, msg, t in self.bag.read_messages(topics="/nav/fix"):
			if topic == "/nav/fix":

				self.gnss_data_dict[msg.status.status].append( np.array([msg.longitude, msg.latitude]) )

		status_num = [0]*8
		for key_name in self.gnss_data_dict.keys():
			status_len = len(self.gnss_data_dict[key_name])
			if status_len == 0:
				continue
			elif status_len == 1:
				self.gnss_data_dict[key_name] = np.array(self.gnss_data_dict[key_name])
			else:
				self.gnss_data_dict[key_name] = np.vstack( self.gnss_data_dict[key_name])
				status_num[key_name] += status_len

		bar_edge = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
		plt.figure()
		plt.subplot(121)
		plt.xlabel("GNSS status")
		plt.ylabel("Points")
		plt.title("Total points: %d"%sum(status_num))
		plt.bar(bar_edge, status_num)
		for i, v in enumerate(status_num):
		    plt.text(bar_edge[i], v, str(v))

		self.color_lst = ['k', 'w', 'm', 'c', 'r', 'o', 'y', 'b']
		handle_lst = []
		plt.subplot(122)
		plt.axis('equal')
		plt.xlabel("Longitude")
		plt.ylabel("Latitude")
		plt.ticklabel_format(useOffset=False)

		for i in range(8):
			if status_num[i] == 0:
				continue
			if i != 7:
				plt_handle, = plt.plot(self.gnss_data_dict[i][:,0], self.gnss_data_dict[i][:,1], \
					"*"+self.color_lst[i],label="status="+str(i), markersize=10)
			else:
				plt_handle, = plt.plot(self.gnss_data_dict[i][:,0], self.gnss_data_dict[i][:,1], \
					"."+self.color_lst[i],label="status="+str(i), markersize=2)
			handle_lst.append(plt_handle)

		plt.legend(handles=handle_lst, loc=2)
		plt.show()  


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--path', default="/home/yimeng/Documents/dataset/20170909/2017-09-09-15-41-13.bag")
	args = parser.parse_args()

	plotter = plotTrajectory(args.path)
	plotter.collect()