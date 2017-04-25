#! /usr/bin/env python
# save waypoints file based on time interval
# Subscribe: PoseStamped, Twist
# this version is used for tele control simulation

import rospy, tf, os, getpass, math
from waypoint_follower.msg import waypoint, lane
from geometry_msgs.msg import PoseStamped, Twist
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry

# init parameter
MIN_VELOCITY = 0.001

# init msg
waypoint_msg = waypoint()

# callback functions
def odomCallback(twist_msg):
	waypoint_msg.pose.pose = twist_msg.pose.pose
	waypoint_msg.twist.twist = twist_msg.twist.twist

# init ros
rospy.init_node('waypoint_saver')
waypointFilePath = rospy.get_param('~waypointFilePath', os.path.join("/home", getpass.getuser(), "waypoints.txt"))
pubrate = rospy.get_param('~pubrate', 0.33)

twist_sub = rospy.Subscriber("/odometry/filtered", Odometry, callback=odomCallback)
pub_rate = rospy.Rate(pubrate)

# main function goes here
if __name__ == "__main__":

	rospy.loginfo("waypoint saver starts working")
	rospy.loginfo("filepath: %s, pubrate = %d", waypointFilePath, pubrate)

	cout = 0
	while not rospy.is_shutdown():

		with open(waypointFilePath, 'a') as waypoint_save_file:

			if cout == 0:
				line = "pose_x  pose_y  pose_z  yaw  velocity\n"
			else:
				x = str(waypoint_msg.pose.pose.position.x)
				y = str(waypoint_msg.pose.pose.position.y)
				z = str(waypoint_msg.pose.pose.position.z)

				qx = waypoint_msg.pose.pose.orientation.x
				qy = waypoint_msg.pose.pose.orientation.y
				qz = waypoint_msg.pose.pose.orientation.z
				qw = waypoint_msg.pose.pose.orientation.w
				
				(roll,pitch,yaw) = tf.transformations.euler_from_quaternion([qx, qy, qz, qw])
				yaw = str(yaw)

				if waypoint_msg.twist.twist.linear.x < MIN_VELOCITY:
					velocity = str(0)
				else:
					velocity = str(waypoint_msg.twist.twist.linear.x)

				line = x+" "+y+" "+z+" "+yaw+" "+velocity+"\n"

			waypoint_save_file.write(line)
			rospy.loginfo(line)

		cout += 1
		pub_rate.sleep()

	rospy.loginfo("waypoint saver stops working")