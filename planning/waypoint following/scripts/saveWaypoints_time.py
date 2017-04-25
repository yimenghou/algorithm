#! /usr/bin/env python
# save waypoints file based on time interval
# Subscribe: PoseStamped, Twist

import rospy, tf, os, getpass, math
from waypoint_follower.msg import waypoint, lane
from geometry_msgs.msg import PoseStamped, Twist
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry

# init parameter
MIN_VELOCITY = 0.001

# init msg
waypoint_current = waypoint()
waypoint_previous = waypoint()

# lane_array = lane()
imu_msg = Imu()

# callback functions
def poseCallback(pose_msg):
	waypoint_current.pose = pose_msg

def twistCallback(twist_msg):
	waypoint_current.twist.twist = twist_msg.twist.twist

def imuCallback(orientation_msg):
	imu_msg.orientation = orientation_msg.orientation

# init ros
rospy.init_node('waypoint_saver')
waypointFilePath = rospy.get_param('~waypointFilePath', os.path.join("/home", getpass.getuser(), "waypoints.txt"))
pubrate = rospy.get_param('~pubrate', 10)

# waypoint_pub = rospy.Publisher("waypoint", waypoint, queue_size=10)
# waypoint_array_pub = rospy.Publisher("waypoint/lane", lane, queue_size=10)
pose_sub = rospy.Subscriber("/gnss_pose", PoseStamped, callback=poseCallback)
twist_sub = rospy.Subscriber("/husky_velocity_controller/odom", Odometry, callback=twistCallback)
imu_sub = rospy.Subscriber("/imu/data", Imu, callback=imuCallback)
pub_rate = rospy.Rate(pubrate)

# main function goes here
if __name__ == "__main__":

	rospy.loginfo("waypoint saver starts working")
	rospy.loginfo("filepath: %s, pubrate = %d", waypointFilePath, pubrate)

	cout = 0
	while not rospy.is_shutdown():

		# lane_array.waypoints.append( waypoint_current )
		# waypoint_pub.publish(waypoint_current)
		# waypoint_array_pub.publish(lane_array)

		with open(waypointFilePath, 'a') as waypoint_save_file:

			if cout == 0:
				line = "pose_x  pose_y  pose_z  yaw  velocity\n"
			else:
				x = str(waypoint_current.pose.pose.position.x)
				y = str(waypoint_current.pose.pose.position.y)
				z = str(waypoint_current.pose.pose.position.z)
				qx = imu_msg.orientation.x
				qy = imu_msg.orientation.y
				qz = imu_msg.orientation.z
				qw = imu_msg.orientation.w
				(roll,pitch,yaw) = tf.transformations.euler_from_quaternion([qx, qy, qz, qw])
				yaw = str(yaw)

				if waypoint_current.twist.twist.linear.x < MIN_VELOCITY:
					velocity = str(0)
				else:
					velocity = str(waypoint_current.twist.twist.linear.x)

				line = x+" "+y+" "+z+" "+yaw+" "+velocity+"\n"

			waypoint_save_file.write(line)
			rospy.loginfo(line)

		cout += 1
		pub_rate.sleep()

	rospy.loginfo("waypoint saver stops working")