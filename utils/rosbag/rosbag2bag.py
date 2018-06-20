# -*- coding: UTF-8 -*-
#! /usr/bin/env python

import rosbag, os, h5py, cv2, struct, copy, time, yaml
import pylab as plt, numpy as np
from modules.control.proto import control_cmd_pb2 

inbag_path = "/home/yimeng/Downloads/apollo-master/docs/demo_guide/demo_2.0.bag"
outbag_path  = "/media/yimeng/solid/rosbag_trail"

class rosbag2bag(object):

	def __init__(self, bag_path=None, out_bag_path=None):

		self.pb_msg = control_cmd_pb2.ControlCommand()
		self.bag_path = bag_path
		print "input bag", self.bag_path
		print "output bag", self.out_bag_path

	def collect(self):

		bag_temp = rosbag.Bag(self.bag_path, 'r')

		info_dict = yaml.load(bag_temp._get_yaml_info())

		for topic_item in info_dict["topics"]:
			print topic_item

		for topic, msg, t in bag_temp.read_messages():	
			if topic == '/apollo/control':
				self.pb_msg.CopyFrom(msg)
				print self.pb_msg.throttle
			time.sleep(1)


if __name__ == "__main__":

	if not os.path.exists(outbag_path):
		os.mkdir(outbag_path)

	worker0 = rosbag2bag(inbag_path, outbag_path)
	worker0.collect()

