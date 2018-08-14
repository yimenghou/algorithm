#! /usr/bin/env python

import pylab as plt
import rospy, time
from ws_msgs.msg import lane

class waypointObserver(object):

	def __init__(self):

		self.waypoint_x = []
		self.waypoint_y = []
		self.waypoint_type = []
		self.waypoint_length = 0
		self.init_done = False
		self.sub0 = rospy.Subscriber("/original_waypoints", lane, self.wpcallback)

	def wpcallback(self,data):
		if self.init_done:
			return
		self.waypoint_length = len(data.waypoints)
		for i in range(self.waypoint_length):
			self.waypoint_x.append(data.waypoints[i].pose.pose.position.x)
			self.waypoint_y.append(data.waypoints[i].pose.pose.position.y)
			self.waypoint_type.append(data.waypoints[i].type)
		self.init_done = True

	def run(self):

		time.sleep(2)
		plt.figure()
		plt.axis('equal')

		print "waypoints: ", self.waypoint_length
		for i in range(self.waypoint_length):
			if self.waypoint_type[i] == 0:
				plt.plot(self.waypoint_x[i], self.waypoint_y[i], ".y")
			elif self.waypoint_type[i] == 1:
				plt.plot(self.waypoint_x[i], self.waypoint_y[i], "bx", markersize=10)
			elif self.waypoint_type[i] == 4:
				plt.plot(self.waypoint_x[i], self.waypoint_y[i], "rx", markersize=10)
			elif self.waypoint_type[i] == 9:
				plt.plot(self.waypoint_x[i], self.waypoint_y[i], "bo", markersize=10)				
			# plt.pause(0.0001)

			print " "+str(self.waypoint_type[i]),
		plt.show()
		# raw_input("press anykey to continue")


rospy.init_node("ob", anonymous=True)
worker0 = waypointObserver()
worker0.run()
