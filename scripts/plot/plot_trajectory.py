#! /usr/bin/env python
# last update 2017.4.27 yimeng

pathName = "/media/yimeng/0ade5f79-daf5-43f5-9b3f-fbad02d13a32/dataset/rosbag/20170815"
fileName = "2017-08-16-17-24-27.bag"
animate = False # plot in animate mode?
filterCurve = False # filter original data?
topic_list = ["/nav/fix"] # which topic to plot?


import rosbag, os
import numpy as numpy
import pylab as plt
import multiprocessing
from scipy import signal

class plotTrajectory(object):

	def __init__(self, fileName):

		print "loading bag file, it may takes seconds .."
		self.bag = rosbag.Bag(fileName, 'r')

	def plot(self, topic_list, interactiveMode = True):

		fix_long, fix_lat = [], []
		pose_x_auto, pose_y_auto = [], []
		pose_x_cutt, pose_y_cutt = [], []
		odom_x, odom_y = [], []
		odom_flt_x, odom_flt_y = [], []

		for topic, msg, t in self.bag.read_messages(topics=topic_list):

			# if topic == "/nav/fix":
			# 	fix_long.append(msg.longitude)
			# 	fix_lat.append(msg.latitude)
			if topic == "/nav/fix":
				fix_long.append(msg.longitude)
				fix_lat.append(msg.latitude)
			elif topic == "/gnss_pose/cutter":
				pose_x_cutt.append(msg.pose.position.x)
				pose_y_cutt.append(msg.pose.position.y)		
			elif topic == "/gnss_pose":
				pose_x_auto.append(msg.pose.position.x)
				pose_y_auto.append(msg.pose.position.y)
			elif topic == '/husky_velocity_controller/odom':
				odom_x.append(msg.pose.pose.position.x)
				odom_y.append(msg.pose.pose.position.y)
			elif topic == '/odometry/filtered':
				odom_flt_x.append(msg.pose.pose.position.x)
				odom_flt_y.append(msg.pose.pose.position.y)
			else:
				raise Exception("topic name in the list not exist in bag file, check topic name")

		if interactiveMode:

			if "/nav/fix" in topic_list:
				P0 = multiprocessing.Process(target = plot_base, args = (fix_long, fix_lat, "/nav/fix", True, filterCurve))
				P0.start()
			if "/gnss_pose/cutter" in topic_list:				
				P1 = multiprocessing.Process(target = plot_base, args = (pose_x_cutt, pose_y_cutt, "/gnss_pose/cutter", True, filterCurve))
				P1.start()
			if "/gnss_pose" in topic_list:
				P2 = multiprocessing.Process(target = plot_base, args = (pose_x_auto, pose_y_auto, "/gnss_pose", True, filterCurve))
				P2.start()
			if '/husky_velocity_controller/odom' in topic_list:
				P3 = multiprocessing.Process(target = plot_base, args = (odom_x, odom_y, '/husky_velocity_controller/odom', True, filterCurve))
				P3.start()
			if '/odometry/filtered' in topic_list:
				P4 = multiprocessing.Process(target = plot_base, args = (odom_flt_x, odom_flt_y, '/odometry/filtered', True, filterCurve))
				P4.start()

		else:
			for topic in topic_list:

				if topic == "/nav/fix":
					plot_base(fix_long, fix_lat, topic, False, filterCurve)
				elif topic == "/gnss_pose/cutter":
					plot_base(pose_x_cutt, pose_y_cutt, topic, False, filterCurve)
				elif topic == "/gnss_pose":
					plot_base(pose_x_auto, pose_y_auto, topic, False, filterCurve)	
				elif topic == '/husky_velocity_controller/odom':			
					plot_base(odom_x, odom_y, topic, False, filterCurve)
				elif topic == '/odometry/filtered':
					plot_base(odom_flt_x, odom_flt_y, topic, False, filterCurve)					
				else:
					raise Exception("topic name in the list not exist in bag file")

		plt.show()

def plot_base(x, y, plot_title, interactiveMode, filtered = False):

	_step_size = 200
	print "topic name: ", plot_title

	if filtered:
		order = 4 # low pass filter order
		stopBandAttenuation = 40 # in dB unit
		passBandCutOffFreq = 0.03 # in normalized frequency scale

		b, a = signal.cheby2(order, stopBandAttenuation, passBandCutOffFreq)
		y = signal.filtfilt(b, a, y)
		x = signal.filtfilt(b, a, x)

	if len(x) != len(y):
		raise Exception("x and y are not equal length")

	if interactiveMode:
		plt.figure()
		plt.grid()
		plt.title(plot_title)
		plt.ion()

		if len(x)%_step_size == 0:
			batch_num = len(x)/_step_size
		else:
			batch_num = len(x)/_step_size + 1

		for i in range(_step_size, len(x) - len(x)%_step_size +_step_size , _step_size):

			if batch_num*_step_size - i < _step_size:
				print temp_endpoint
				temp_endpoint = i+len(x)%_step_size
			else:
				temp_endpoint = i

			plt.plot(x[i-_step_size:temp_endpoint], y[i-_step_size:temp_endpoint], 'b', x[0],y[0], 'ob', x[-1],y[-1], '*r', )
			plt.pause(1e-9)

		plt.show()

	else:
		plt.figure()
		plt.title(plot_title)
		plt.grid()
		plt.plot(x, y, 'b', x[0],y[0], 'ob', x[-1],y[-1], '*r')

plotter = plotTrajectory(os.path.join(pathName, fileName))
plotter.plot(topic_list, animate)