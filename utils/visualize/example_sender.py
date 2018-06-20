
#!/usr/bin/env python

import rosbag, os, argparse, rospy, time
from std_msgs.msg import *
import numpy as np
import matplotlib.pylab as plt
from matplotlib.ticker import FormatStrFormatter

num0 = 0;
num1 = 0;
c = 0;
a = 10;
pub0 = rospy.Publisher('trajectory0', Float32, queue_size=10)
pub1 = rospy.Publisher('trajectory1', Float32, queue_size=10)
rospy.init_node('talker', anonymous=True)
rate = rospy.Rate(10) # 10hz
while not rospy.is_shutdown():
	num0 = a*np.sin(2*np.pi*0.01*c)
	num1 = a*np.cos(2*np.pi*0.01*c)
	c+=1
	c = c%100
	pub0.publish(num0)
	pub1.publish(num1)
	rate.sleep()