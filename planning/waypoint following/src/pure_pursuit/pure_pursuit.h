
#ifndef PURE_PURSUIT_H
#define PURE_PURSUIT_H

// ROS includes
#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/TwistStamped.h>

// User defined includes
#include "waypoint_follower/lane.h"
#include "waypoint_follower/libwaypoint_follower.h"

namespace waypoint_follower
{
class PurePursuit
{
public:
  PurePursuit();
  ~PurePursuit();

  // for setting data
  void setLookaheadDistance(const double &ld)
  {
    lookahead_distance_ = ld;
  }
  void setCurrentVelocity(const double &cur_vel)
  {
    current_linear_velocity_ = cur_vel;
  }
  void setCurrentWaypoints(const std::vector<waypoint_follower::waypoint> &wps)
  {
    current_waypoints_ = wps;
  }
  void setCurrentPose(const geometry_msgs::PoseStampedConstPtr &msg)
  {
    current_pose_ = msg->pose;
  }
  void setLinearInterpolationParameter(const bool &param)
  {
    is_linear_interpolation_ = param;
  }

  // for debug on ROS
  geometry_msgs::Point getPoseOfNextWaypoint() const
  {
    return current_waypoints_.at(next_waypoint_number_).pose.pose.position;
  }
  geometry_msgs::Point getPoseOfNextTarget() const
  {
    return next_target_position_;
  }
  geometry_msgs::Pose getCurrentPose() const
  {
    return current_pose_;
  }
  double getLookaheadDistance() const
  {
    return lookahead_distance_;
  }
  double isFinalwaypointReach() const
  {
    return is_finalwaypoint_reach_flag;
  }
  int getIndexOfNextWaypoint() const
  {
    return next_waypoint_number_;
  }
  int getTotalNumOfWaypoint() const
  {
    return total_waypoint_number_;
  }  

  // processing
  bool canGetCurvature(double *output_kappa);


private:
  // constant
  const double RADIUS_MAX_;
  const double KAPPA_MIN_;

  // variables
  bool is_linear_interpolation_;
  bool is_finalwaypoint_reach_flag;
  int next_waypoint_number_;
  int total_waypoint_number_;
  int lookahead_waypoint_;
  geometry_msgs::Point next_target_position_;
  double lookahead_distance_;
  geometry_msgs::Pose current_pose_;
  double current_linear_velocity_;
  double reach_target_distance_;
  std::vector<waypoint_follower::waypoint> current_waypoints_;

  // functions
  double calcCurvature(geometry_msgs::Point target) const;
  bool interpolateNextTarget(int next_waypoint, geometry_msgs::Point *next_target) const;
  void getNextWaypoint();
};
}  // waypoint_follower

#endif  // PURE_PURSUIT_H
