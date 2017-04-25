#! /usr/bin/env python

from geometry_msgs.msg import Twist
import rospy

rospy.init_node("remapper")

def tCallback(msg):
	t.linear = msg.twist.linear
	t.angular = msg.twist.angular


t_sub = rospy.Subscriber("twist_raw", Twist, callback=tCallback)
t_pub = rospy.Publisher("husky_velocity_controller/cmd_vel", Twist, queue_size=10)
pub_rate = rospy.Rate(10)

t = Twist()

rospy.loginfo("remapper starts working")  
while not rospy.is_shutdown():
	t_pub.publish( t )
	pub_rate.sleep()