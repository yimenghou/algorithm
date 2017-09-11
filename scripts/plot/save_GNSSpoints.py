#! /usr/bin/env python
# last update 2017.8.17 yimeng
# check gnss trajectory

from __future__ import division

pathName = "/media/yimeng/0ade5f79-daf5-43f5-9b3f-fbad02d13a32/dataset/rosbag/20170815"
# fileName = "2017-08-16-17-24-27.bag"
fileName = "2017-08-16-17-29-56.bag"
filePath_o = "/home/yimeng/gnss_20170816.txt"
# fileName = "2017-08-16-17-42-36.bag"
topic_list = ["/nav/fix"] # which topic to plot?

import rosbag, os, yaml
import numpy as np
import pylab as plt
from scipy import signal

class plotTrajectory(object):

	def __init__(self, fileName):

		print "loading bag file, it may takes seconds .."
		bag = rosbag.Bag(fileName, 'r')

		info_dict = yaml.load(bag._get_yaml_info())

		for item in info_dict['topics']:
			if item['topic'] == '/nav/fix':
				msg_freq = item['frequency']
				msg_length = item['messages']

		fix_array = np.zeros((msg_length, 4))

		n = 0
		for topic, msg, t in bag.read_messages(topics=topic_list):

			fix_array[n, 0] = msg.latitude
			fix_array[n, 1] = msg.longitude
			fix_array[n, 2] = msg.altitude
			fix_array[n, 3] = msg.status.status
			n += 1

		with open(filePath_o, 'a') as f:
			for i in range(fix_array.shape[0]):
				sentence = str(fix_array[i, 0]) + " " + str(fix_array[i, 1]) + str(fix_array[i, 2]) + " " + str(fix_array[i, 3]) + "\n"
				f.write(sentence)

if __name__ == "__main__":

	worker0 = plotTrajectory( os.path.join(pathName, fileName) )