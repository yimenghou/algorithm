#! /usr/bin/env python
# subscribe image and twist, save it to local files

import rospy, tf, os, getpass, math, copy, time, numpy as np, pickle, message_filters, signal
from geometry_msgs.msg import PoseStamped, Twist
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from datetime import datetime
from cv_bridge import CvBridge, CvBridgeError

global exitcode, file_path, spin_interval
exitcode = 0
file_path = os.path.join("/home", getpass.getuser())
spin_interval = 0.2

def signal_handler(signal, frame):
	exitcode = 1

class Imagedatacollector(object):

	def __init__(self):

		# init msg
		self.image = None
		self.velocity = np.zeros(2, dtype=np.float) # [linear.x, angular.z]

		# init pub,sub
		self.image_sub = rospy.Subscriber("/camera_image", Image, callback=self.imageCallback)
		self.twist_sub = rospy.Subscriber("/husky_velocity_controller/odom", Odometry, callback=self.twistCallback)

		# synchronized msg
		# self.image_sub = message_filters.Subscriber('/camera_image', Image)
		# self.twist_sub = message_filters.Subscriber('/husky_velocity_controller/odom', Odometry)
		# ts = message_filters.TimeSynchronizer([self.image_sub, self.twist_sub], 50)
		# ts.registerCallback(self.callback)

		# others
		self.bridge = CvBridge()

		# init ros
		rospy.init_node('image_data_collector')

	def run(self):

		rospy.loginfo("image data collector starts working")
		image_temp, label_temp = [], []
	    # file_path = rospy.get_param('~image_path', os.path.join("/home", getpass.getuser()), images, data)

		while not rospy.is_shutdown() | exitcode == 1:
			if self.image != None:
				print self.velocity
				image_temp.append(self.image.flatten())
				label_temp.append(self.velocity)
			time.sleep(spin_interval)

		self.dumpData(image_temp, label_temp)

	def dumpData(self, image_temp, label_temp):

		# formatting
		time_now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
		file_name = "image_"+time_now
		data_filepath = os.path.join(file_path, file_name)

		print "Making image and label .."

		# making
		image_all = np.vstack(image_temp)
		label_all = np.vstack(label_temp)
		data_dict = { 'dataset':image_all, \
						'labelset':label_all}  

		# dump data              
		with open(data_filepath, 'wb') as f:
			pickle.dump(data_dict , f)	

		print "Collect %d frames in total"%len(image_temp)
		print "Saving to : %s"%data_filepath
		print "image data collector done"

	# callback functions
	def imageCallback(self, img_msg):
		# get image from camera
		self.image = self.bridge.imgmsg_to_cv2(img_msg, "bgr8")

	def twistCallback(self, twist_msg):
		# get twist from odometry
		self.velocity[0] = twist_msg.twist.twist.linear.x
		self.velocity[1] = twist_msg.twist.twist.angular.z

	# def callback(self, img_msg, twist_msg):
	#   # Solve all of perception here...
	# 	self.image = self.bridge.imgmsg_to_cv2(img_msg, "bgr8")
	# 	self.velocity[0] = twist_msg.twist.twist.linear.x
	# 	self.velocity[1] = twist_msg.twist.twist.angular.z

if __name__ == "__main__":

	signal.signal(signal.SIGINT, signal_handler)
	worker0 = Imagedatacollector()
	worker0.run()