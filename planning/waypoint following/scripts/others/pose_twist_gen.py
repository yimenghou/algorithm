#! /usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped, Twist

pose_msg = PoseStamped()
twist_msg = Twist()

# -2.58290033318 0.40028065504
pose_msg.pose.position.x = -1508621.69758
pose_msg.pose.position.y = -421288.89287
pose_msg.pose.position.z = -1.18591356277

twist_msg.linear.x = 0.40028065504

rospy.init_node("pose_twist_gen")
PosePubliser = rospy.Publisher('/nav/pose/autoware', PoseStamped, queue_size=100)
TwistPublisher = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=100)

pub_rate = rospy.Rate(30)
while not rospy.is_shutdown():
	PosePubliser.publish(pose_msg)
	TwistPublisher.publish(twist_msg)
	pub_rate.sleep()


