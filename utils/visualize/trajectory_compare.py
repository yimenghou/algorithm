#! /usr/bin/env python
# last update 2018.6.19 yimeng
# Real-time plot and compare two curves from ros subscription or rosbag

# TO compare the trajectory in a ROS bag, just run the following in the command line:
# python trajectory_compare.py -p /complete/path/to/the/rosbag

# TO compare the trajectory from ros topic:
# 1. make sure your program advertive std_msgs::Float32 to /trajectory0 and /trajectory1 respectively 
# 2. run the following in the command line:
# python trajectory_compare.py

# TO change plot refresh rate to 5Hz:
# python trajectory_compare.py -r 5

import rosbag, os, argparse, rospy, time, sys
from std_msgs.msg import *
import numpy as np
import matplotlib.pylab as plt
from matplotlib.ticker import FormatStrFormatter
import warnings

class DataPlotter(object):

	def __init__(self, fileName=None, update_rate=10):

		self.sub_data0 = []
		self.sub_data1 = []

		if fileName==None or fileName=="":
			print ">> Subscribing to /trajectory0, /trajectory1, with datatype: std_msgs::Float32"
			self.sub0 =  rospy.Subscriber("/trajectory0", Float32, self.callback0)
			self.sub1 =  rospy.Subscriber("/trajectory1", Float32, self.callback1)
		else:
			if not os.path.exists(fileName):
				raise IOError("Specified rosbag path not exists, please check again")
				sys.exit()

			print ">> Loading ROS bag: %s it may take seconds .."%fileName
			self.bag_filename = fileName
			self.bag = rosbag.Bag(fileName, 'r')
			for topic, msg, t in self.bag.read_messages():
				if topic == "/trajectory0":
					self.sub_data0.append(msg.data)
				elif topic == "/trajectory1":
					self.sub_data1.append(msg.data)
				else:
					pass

		self.update_rate = update_rate
		self.n = [0, 0]
		self.color_list = ['k', 'w', 'm', 'c', 'r', 'y', 'b']
		self.color_choice = np.random.choice(len(self.color_list), 2, replace=False)

	def callback0(self, data):
		self.sub_data0.append(data.data)

	def callback1(self, data):
		self.sub_data1.append(data.data)

	def plotTrajectory(self, sample_type='o-'):

		handle_lst = []
		plt.axis('equal')
		plt.xlabel("time sample")
		plt.ylabel("value")
		plt.ticklabel_format(useOffset=False)

		plt_handle0, = plt.plot(self.sub_data0, sample_type+self.color_list[self.color_choice[0]], label="/trajectory0", markersize=5)
		plt_handle1, = plt.plot(self.sub_data1, sample_type+self.color_list[self.color_choice[1]], label="/trajectory1", markersize=5)		
		handle_lst.append(plt_handle0)
		handle_lst.append(plt_handle1)

		plt.legend(handles=handle_lst, loc=2)
		plt.pause(0.5/self.update_rate) 

	def run(self):

		plt.figure()
		plt.ion()
		plt.hold(True)

		while not rospy.is_shutdown():
			self.plotTrajectory()
			time.sleep(0.5/self.update_rate)

rospy.init_node('trajectory_plotter', anonymous=True)
warnings.filterwarnings("ignore",".*Using default event loop until function specific to this GUI is implemented*")
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help='Rosbag path', type=str, default="")
parser.add_argument('-r', '--rate', help='Plot refresh rate', type=int, default=10)
args = parser.parse_args()

worker0 = DataPlotter(args.path, args.rate)
worker0.run()

# def plotTrajectory(self, sample_type='-o'):

# 	handle_lst = []
# 	plt.axis('equal')
# 	plt.xlabel("time sample")
# 	plt.ylabel("value")
# 	plt.ticklabel_format(useOffset=False)

# 	if len(self.sub_data0)!=0:
# 		plt_handle0, = plt.plot([i for i in range(self.n[0], len(self.sub_data0), 1)], self.sub_data0[self.n[0]:len(self.sub_data0)], \
# 			sample_type+self.color_list[self.color_choice[0]], label="/trajectory0", markersize=5)
# 		handle_lst.append(plt_handle0)
# 		self.n[0] = len(self.sub_data0)
# 		# [self.sub_data0.pop(0) for i in range(len(self.sub_data0))]

# 	if len(self.sub_data1)!=0:
# 		plt_handle1, = plt.plot([i for i in range(self.n[1], len(self.sub_data1), 1)], self.sub_data1[self.n[1]:len(self.sub_data1)], \
# 			sample_type+self.color_list[self.color_choice[1]], label="/trajectory1", markersize=5)		
# 		handle_lst.append(plt_handle1)
# 		self.n[1] = len(self.sub_data1)
# 		# [self.sub_data1.pop(0) for i in range(len(self.sub_data1))]

# 	plt.legend(handles=handle_lst, loc=2)
# 	plt.pause(0.5/self.update_rate) 