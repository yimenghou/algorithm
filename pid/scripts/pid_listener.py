#!/usr/bin/env python
# license removed for brevity
import rospy, copy
import numpy as np
import matplotlib.pylab as plt
from std_msgs.msg import Float64MultiArray, Float64

class pid_evalulator(object):

  target_list = []
  output_list = []
  feedback_list = []
  target_val = 0
  feedback_val = 0
  buf_len = 100

  def __init__(self):
    rospy.Subscriber("/pid_feedback", Float64, self.callback)
    self.pub = rospy.Publisher("/pid_target", Float64MultiArray, queue_size=10)

  def callback(self, data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    # if len(self.output_list) > self.buf_len:
    #   self.output_list.pop(0)
    #   self.target_list.pop(0)
    self.output_list.append(data.data)

    print("Receive from callback")

  def run(self):

    plt.figure()
    plt.ion()
    plt.show()

    self.rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():

      if self.target_val < 50:
        self.target_val += 1

      if self.target_val >= 10:
        if self.target_val < 50:
          self.feedback_val = self.target_val - 10
        else:
          self.feedback_val += np.random.rand(1)
          if np.abs(self.feedback_val - self.target_val) < 1:
            self.feedback_val = self.target_val 
      else:
        self.feedback_val = 0

      print(self.target_val, self.feedback_val)

      msg_send = Float64MultiArray()
      msg_send.data.append(self.feedback_val)
      msg_send.data.append(self.target_val)
      self.pub.publish(msg_send)
      self.target_list.append(copy.deepcopy(self.target_val))
      self.feedback_list.append(copy.deepcopy(self.feedback_val))

      plt.plot(self.output_list, ".r")
      plt.plot(self.target_list, ".b")
      plt.plot(self.feedback_list, ".g")
      plt.xlim((-10, 200))
      plt.ylim((0, 100))
      plt.xlabel('time')
      plt.ylabel('PID')

      plt.grid(True)
      plt.pause(0.001)
      self.rate.sleep()


if __name__ == "__main__":
  rospy.init_node('pid_listener', anonymous=True)
  worker0 = pid_evalulator()
  worker0.run()