# -*- coding: UTF-8 -*-

from init import *

ctrl_msg = control_cmd_pb2.ControlCommand()
ctrl_msg.throttle = 0
ctrl_msg.brake = 0

pose_msg = pose_pb2.Pose()
pose_msg.heading = 0

bag = rosbag.Bag('test.bag', 'w')

for i in range(10):
	ctrl_msg.throttle += 0.1
	ctrl_msg.brake += 0.2
	pose_msg.heading += 0.3
	bag.write('/ctrl', ctrl_msg)
	bag.write('/pose', pose_msg)
	time.sleep(1)
bag.close()
