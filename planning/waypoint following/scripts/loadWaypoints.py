#! /usr/bin/env python
# load: waypoint save file
# publish: waypoint_lane

import rospy, tf, getpass, os
import numpy as np
from waypoint_follower.msg import waypoint, lane

class waypoint_loader(object):

	def __init__(self):

		# getting parameter from ROS server
		try:
			self.filePath = rospy.get_param('~waypointFilePath')
		except:
			self.filePath = os.path.join("/home", getpass.getuser(), "waypoints.txt")

		self.waypoint_all = None
		self.num_column = 5 # pose_x, pose_y, pose_z, yaw, velocity
		self.waypoint_lane = lane()

		self.parseWaypointFile()

	def parseWaypointFile(self):

		with open(self.filePath) as f:
		    content = f.readlines()

		num_waypoints = len(content)
		self.waypoint_all = np.zeros((num_waypoints-1, self.num_column), dtype=np.float) # first line exclude

		for line in enumerate(content[1:]):

			if line[1] == "\n":
				continue

			waypoint_temp = line[1].strip().split(' ')
			waypoint_msg = waypoint()

			for column_idx in range(self.num_column):
				self.waypoint_all[line[0], column_idx] = float(waypoint_temp[column_idx])

			rosTimeNow = rospy.Time.now()

			waypoint_msg.pose.header.seq = line[0];
			waypoint_msg.pose.header.stamp = rosTimeNow;
			waypoint_msg.pose.header.frame_id = "/odom";

			waypoint_msg.pose.pose.position.x = float(waypoint_temp[0])
			waypoint_msg.pose.pose.position.y = float(waypoint_temp[1])
			waypoint_msg.pose.pose.position.z = float(waypoint_temp[2])
			q = tf.transformations.quaternion_from_euler(0,0,float(waypoint_temp[3]))	

			waypoint_msg.pose.pose.orientation.x = q[0]
			waypoint_msg.pose.pose.orientation.y = q[1]
			waypoint_msg.pose.pose.orientation.z = q[2]
			waypoint_msg.pose.pose.orientation.w = q[3]

			waypoint_msg.twist.header.seq = line[0];
			waypoint_msg.twist.header.stamp = rosTimeNow;
			waypoint_msg.twist.header.frame_id = "/odom";

			waypoint_msg.twist.twist.linear.x = float(waypoint_temp[4])	

			self.waypoint_lane.waypoints.append( waypoint_msg )

		return 1

if __name__ == "__main__":

	rospy.init_node("waypoint_loader")
	waypoint_pub = rospy.Publisher("/final_waypoints", lane, queue_size=10)
	pub_rate = rospy.Rate(10)

	w = waypoint_loader()

	rospy.loginfo("Waypoint loader starts working")
	rospy.loginfo("Filepath: %s", w.filePath)

	while not rospy.is_shutdown():
		waypoint_pub.publish( w.waypoint_lane )
		pub_rate.sleep()
		
	rospy.loginfo("Shutting down")  