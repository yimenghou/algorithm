#! /usr/bin/env python
# save waypoints file
# Subscribe: PoseStamped, Twist
# this version of save waypoints save waypoints based on fixed distance rather than time interval

import rospy, tf, os, getpass, math, copy, time
from waypoint_follower.msg import waypoint, lane
from geometry_msgs.msg import PoseStamped, Twist
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry

class saveWP(object):

	def __init__(self):

		# init parameter
		self.MIN_VELOCITY = 0.001
		self.MAX_VELOCITY = 1.0

		# init msg
		self.waypoint_current = waypoint()
		self.waypoint_previous = waypoint()

		# init pub,sub
		self.twist_sub = rospy.Subscriber("/odometry/filtered", Odometry, callback=self.odomCallback)

		# others
		self.publish_flag = True
		self.point_stay = [0,0,0]

		# init ros
		rospy.init_node('waypoint_saver')
		self.waypointFilePath = rospy.get_param('~waypointFilePath', os.path.join("/home", getpass.getuser(), "waypoints.txt"))
		self.waypointInverval = rospy.get_param('~waypointInverval', 2.0)

	def run(self):

		rospy.loginfo("waypoint saver starts working")
		rospy.loginfo("filepath: %s, waypoint interval = %f", self.waypointFilePath, self.waypointInverval)

		with open(self.waypointFilePath, 'a') as waypoint_save_file:
			title_line = "pose_x  pose_y  pose_z  yaw  velocity\n"
			waypoint_save_file.write(title_line)

		while not rospy.is_shutdown():

			self.waypoint_previous = copy.deepcopy(self.waypoint_current)
			with open(self.waypointFilePath, 'a') as waypoint_save_file:
				line = self.setWaypoint()

				if self.publish_flag:
					waypoint_save_file.write(line)

		rospy.loginfo("waypoint saver stops working")

	# callback functions
	def odomCallback(self, twist_msg):
		self.waypoint_current.pose.pose = twist_msg.pose.pose
		self.waypoint_current.twist.twist = twist_msg.twist.twist

	def setWaypoint(self):

		if self.publish_flag == False:
			pose_x_prev = self.point_stay[0]
			pose_y_prev = self.point_stay[1]
			pose_z_prev = self.point_stay[2]
		else:
			pose_x_prev = self.waypoint_previous.pose.pose.position.x
			pose_y_prev = self.waypoint_previous.pose.pose.position.y
			pose_z_prev = self.waypoint_previous.pose.pose.position.z

		pose_x_now = self.waypoint_current.pose.pose.position.x
		pose_y_now = self.waypoint_current.pose.pose.position.y
		pose_z_now = self.waypoint_current.pose.pose.position.z

		planeDistance = math.sqrt( (pose_x_prev - pose_x_now)**2 + (pose_y_prev - pose_y_now)**2 )

		if planeDistance < self.waypointInverval:
			self.publish_flag = False
			self.point_stay[0] = pose_x_prev
			self.point_stay[1] = pose_y_prev
			self.point_stay[2] = pose_z_prev
			return ''

		else:
			print "current  waypoint x,y,z: %.4f, %.4f, %.4f"%(pose_x_now, pose_y_now, pose_z_now)
			print "previous waypoint x,y,z: %.4f, %.4f, %.4f"%(pose_x_prev, pose_y_prev, pose_z_prev)
			print "waypoint space: %.4f"%planeDistance
			self.publish_flag = True

		qx = self.waypoint_current.pose.pose.orientation.x
		qy = self.waypoint_current.pose.pose.orientation.y
		qz = self.waypoint_current.pose.pose.orientation.z
		qw = self.waypoint_current.pose.pose.orientation.w
		(roll,pitch,yaw) = tf.transformations.euler_from_quaternion([qx, qy, qz, qw])
		yaw = str(yaw)

		if self.waypoint_current.twist.twist.linear.x < self.MIN_VELOCITY:
			velocity = str(self.MIN_VELOCITY)
		elif self.waypoint_current.twist.twist.linear.x > self.MAX_VELOCITY:
			velocity = str(self.MAX_VELOCITY)
		else:
			velocity = str(self.waypoint_current.twist.twist.linear.x)

		line = str(pose_x_now)+" "+str(pose_y_now)+" "+str(pose_z_now)+" "+yaw+" "+velocity+"\n"

		return line


if __name__ == "__main__":

	wp_saver = saveWP()
	wp_saver.run()