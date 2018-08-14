#! /usr/bin/env python

import pylab as plt
import rospy
from ws_msgs.msg import lane

class waypointObserver(object):

    def __init__(self):

    	self.waypoint_x = []
    	self.waypoint_y = []
    	self.waypoint_type = []
    	self.waypoint_length = 0
        self.sub0 = rospy.Subscriber("/original_waypoints", lane, self.wpcallback)

    def wpcallback(self,data):

		self.waypoint_length = len(data.waypoints)
    	for i in range(self.waypoint_length):
	        self.waypoint_x.append(data.waypoints[i].pose.pose.position.x)
	        self.waypoint_y.append(data.waypoints[i].pose.pose.position.y)
	        self.waypoint_type.append(data.waypoints[i].type)

    def run(self):

		plt.figure()
		plt.ion()
		plt.axis('equal')

		for i in range(self.waypoint_length):		
			if self.waypoint_type[i] == 0:
				plt.plot(self.waypoint_x[i], self.waypoint_y[i], "-o")
			elif self.waypoint_type[i] == 1:
				plt.plot(self.waypoint_x[i], self.waypoint_y[i], "rx")
			elif self.waypoint_type[i] == 4:
				plt.plot(self.waypoint_x[i], self.waypoint_y[i], "bx")
			elif self.waypoint_type[i] == 4:
				plt.plot(self.waypoint_x[i], self.waypoint_y[i], "*")				
			plt.pause(0.1)


rospy.init_node("ob", anonymous=True)
worker0 = observer()
worker0.run()
