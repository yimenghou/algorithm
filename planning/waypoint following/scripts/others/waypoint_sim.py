#! /usr/bin/env python
# this scripts is used for generate simulated pose and velocity messages
# for use of waypoint saver
# 2017.03.30 yimeng


'''

# pub /current_velocity
# pub /current_pose

import rospy
from geometry_msgs.msg import TwistStamped, PoseStamped
import numpy as np

pub_twist = rospy.Publisher('/current_velocity', TwistStamped, queue_size=10)
pub_pose = rospy.Publisher('/current_pose', PoseStamped, queue_size=10)

twist_msg = TwistStamped()
pose_msg = PoseStamped()

rospy.init_node('waypoint_sim_gen')

pubrate = rospy.get_param('~pubrate', 100)

r = rospy.Rate(pubrate) # 10hz
i = 0
while not rospy.is_shutdown():

	pose_msg.header.seq += 1
	pose_msg.header.stamp = rospy.Time.now()
	pose_msg.header.frame_id = "/map"
	pose_msg.pose.position.x = i%100
	pose_msg.pose.position.y = i%100
	pose_msg.pose.position.z = i%100
	pose_msg.pose.orientation.x = 0
	pose_msg.pose.orientation.y = 0
	pose_msg.pose.orientation.z = 0
	pose_msg.pose.orientation.w = 1


	twist_msg.header.seq += 1
	twist_msg.header.stamp = rospy.Time.now()
	twist_msg.header.frame_id = "/map"
	twist_msg.twist.linear.x = 40
	twist_msg.twist.linear.y = 0	
	twist_msg.twist.linear.z = 0
	rand_num = np.random.rand(1)
	twist_msg.twist.angular.x = 0
	twist_msg.twist.angular.y = 0	
	twist_msg.twist.angular.z = rand_num[0]

	pub_twist.publish(twist_msg)
	pub_pose.publish(pose_msg)
	r.sleep()
	i += 1

'''

'''

# sub /twist_raw
# pub /husky_velocity_controller/cmd_vel

import rospy
from geometry_msgs.msg import Twist, TwistStamped

rospy.init_node('waypoint_sim_gen')
twist_msg = Twist()

def twistCallback(msg):
	twist_msg.linear.x = msg.twist.linear.x
	twist_msg.angular.z = msg.twist.angular.z
	# twist_msg = msg.twist 

sub_twist = rospy.Subscriber("/twist_raw", TwistStamped, callback=twistCallback)
pub_twist = rospy.Publisher("/husky_velocity_controller/cmd_vel", Twist, queue_size=10)

pubrate = rospy.Rate(10)
while not rospy.is_shutdown():
	print twist_msg
	pub_twist.publish(twist_msg)
	pubrate.sleep()

'''	