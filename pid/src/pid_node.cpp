#include "ros/ros.h"
#include "std_msgs/Float64MultiArray.h"
#include "std_msgs/Float64.h"
#include "pid/pid.h"

#include <iostream>

static std_msgs::Float64 msg_pub;
static ros::Publisher pub;
static PID pid(1,0.1,0.2);

static void Callback(const std_msgs::Float64MultiArray::ConstPtr& msg) {
  std::cout << "Receive callback: " << msg->data[0] << ", " << msg->data[1] << std::endl;
  auto output = pid.Update(msg->data[0], msg->data[1]);
  msg_pub.data = output;
  pub.publish(msg_pub);
}

int main(int argc, char **argv) {
  ros::init(argc, argv, "pid_talker");
  ros::NodeHandle n;
  pub = n.advertise<std_msgs::Float64>("/pid_feedback", 1000);
  ros::Subscriber sub = n.subscribe("/pid_target", 1000, Callback);
  ros::spin();
  return 0;
}