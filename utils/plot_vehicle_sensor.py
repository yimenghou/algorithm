#! /usr/bin/env python
# last update 2018.08.12 yimeng
# merge gnss trajectory and kmz generation together
# check gnss trajectory

import rosbag, os, argparse
import numpy as np
import matplotlib.pylab as plt
from matplotlib.ticker import FormatStrFormatter

class plotTrajectory(object):

	def __init__(self, fileName):

		print ">> loading bag file: %s it may take seconds .."%fileName
		self.bag_filename = fileName
		self.bag = rosbag.Bag(fileName, 'r')

		self.time_data = []

		self.front_sensor = []
		self.back_sensor = []
		self.distance_data = []
		self.accumulate_distance = 0
		self.speed_data = []

		self.init_time = None

	def collect(self):

		for topic, msg, t in self.bag.read_messages():
			if self.init_time == None:
				self.init_time = msg.header.stamp.secs+1e-9*msg.header.stamp.nsecs

			if topic == "/vehicle_sensor":
				print msg.s_front_mid

				val0 = 6.23 - msg.s_front_mid
				if val0 < 0:
					val0 = 0
				val1 = 6.23 - msg.s_back_mid
				if val1 <0:
					val1 = 0

				self.front_sensor.append(val0)
				self.back_sensor.append(val1)
				self.time_data.append(msg.header.stamp.secs+1e-9*msg.header.stamp.nsecs - self.init_time)
				
			# elif topic == "/vehicle_state":
			# 	v = msg.gantry_speed*0.24
			# 	dt = self.init_time - msg.header.stamp.secs+1e-9*msg.header.stamp.nsecs
			# 	dd = msg.gantry_speed*dt
			# 	self.time_data.append(dt)
			# 	self.distance_data.append(self.accumulate_distance + dd)
			# 	self.speed_data.append(msg.gantry_speed)
			# 	self.accumulate_distance += dd

		n_peak = 0
		for i in range(len(self.front_sensor)):
			if self.front_sensor[i] >= 6 and self.back_sensor[i] >= 6:
				print self.time_data[i]
				n_peak += 1

		print "n_peak: ", n_peak

		plt.figure()
		plt.subplot(211)
		plt.plot(self.front_sensor)
		plt.subplot(212)
		plt.plot(self.back_sensor)
		plt.show()

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("rosbag_path")
	args = parser.parse_args()

	worker0 = plotTrajectory(args.rosbag_path)
	worker0.collect()