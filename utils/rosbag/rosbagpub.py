# -*- coding: UTF-8 -*-

from init import *

ctrl_msg = control_cmd_pb2.ControlCommand()
ctrl_msg.throttle = 99
ctrl_msg.brake = 1
pose_msg = pose_pb2.Pose()

pub = rospy.Publisher('topic_name', control_cmd_pb2.ControlCommand, queue_size=10)
rospy.init_node('node_name')
r = rospy.Rate(10) # 10hz
while not rospy.is_shutdown():
   pub.publish(pb_msg)
   r.sleep()
