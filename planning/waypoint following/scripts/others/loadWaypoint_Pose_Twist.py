#! /usr/bin/env python
# load: waypoint save file
# publish: waypoint_lane

import rospy, tf, getpass, os, sys
import numpy as np
from waypoint_follower.msg import waypoint, lane
from geometry_msgs.msg import Twist, PoseStamped

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
		self.pose_msg = PoseStamped()
		self.twist_msg = Twist()
		self.parseWaypointFile()

		# pub
		self.waypoint_pub = rospy.Publisher("/final_waypoints", lane, queue_size=10)
		self.twist_pub = rospy.Publisher("/husky_velocity_controller/cmd_vel", Twist, queue_size=10)
		self.pose_pub = rospy.Publisher("/gnss_pose", PoseStamped, queue_size=10)


	def parseWaypointFile(self):

		with open(self.filePath) as f:
		    content = f.readlines()

		num_waypoints = len(content)
		self.waypoint_all = np.zeros((num_waypoints-1, self.num_column), dtype=np.float) # first line exclude

		for line in enumerate(content[1:]):

			waypoint_msg = waypoint()

			waypoint_temp = line[1].strip().split(' ')

			for column_idx in range(self.num_column):
				self.waypoint_all[line[0], column_idx] = float(waypoint_temp[column_idx])

			rosTimeNow = rospy.Time.now()

			waypoint_msg.pose.header.seq = line[0];
			waypoint_msg.pose.header.stamp = rosTimeNow;
			waypoint_msg.pose.header.frame_id = "/map";

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
			waypoint_msg.twist.header.frame_id = "/map";

			waypoint_msg.twist.twist.linear.x = float(waypoint_temp[4])	

			self.waypoint_lane.waypoints.append( waypoint_msg )

		return 1

	def run(self):

		with open(self.filePath) as f:
		    content = f.readlines()

		pub_rate = rospy.Rate(1)

		seq = 0

		try:

			for line in enumerate(content[1:]):

				waypoint_temp = line[1].strip().split(' ')
				rosTimeNow = rospy.Time.now()

				self.pose_msg.header.stamp = rosTimeNow
				self.pose_msg.header.seq = seq
				self.pose_msg.header.frame_id = "/map"
				self.pose_msg.pose.position.x = float(waypoint_temp[0])
				self.pose_msg.pose.position.y = float(waypoint_temp[1])
				self.pose_msg.pose.position.z = float(waypoint_temp[2])

				self.twist_msg.linear.x = float(waypoint_temp[4])	

				self.twist_pub.publish(self.twist_msg)
				self.pose_pub.publish(self.pose_msg)
				self.waypoint_pub.publish( self.waypoint_lane )

				seq += 1
				pub_rate.sleep()

		except KeyboardInterrupt:
			sys.exit()

if __name__ == "__main__":

	rospy.init_node("waypoint_pose_twist_sim")

	w = waypoint_loader()
	rospy.loginfo("Waypoint loader starts working")  
	w.run()