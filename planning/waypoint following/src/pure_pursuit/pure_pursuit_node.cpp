
#include <ros/ros.h>
#include "pure_pursuit_core.h"

int main(int argc, char **argv)
{
  ros::init(argc, argv, "pure_pursuit");
  waypoint_follower::PurePursuitNode ppn;
  ppn.run();

  return 0;
}