
#ifndef PURE_PURSUIT_CORE_H
#define PURE_PURSUIT_CORE_H

// ROS includes
#include <ros/ros.h>
#include <geometry_msgs/TwistStamped.h>
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/PoseStamped.h>
#include <visualization_msgs/Marker.h>

// User defined includes
#include "waypoint_follower/lane.h"
#include "waypoint_follower/ControlCommandStamped.h"
#include "pure_pursuit_viz.h"
#include "pure_pursuit.h"

namespace waypoint_follower
{

class PurePursuitNode
{
public:
  PurePursuitNode();
  ~PurePursuitNode();

  void run();

private:
  // handle
  ros::NodeHandle nh_;
  ros::NodeHandle private_nh_;

  // class
  PurePursuit pp_;

  // publisher
  ros::Publisher pub1_, pub2_, pub11_, pub12_, pub13_, pub14_, pub15_;

  // subscriber
  ros::Subscriber sub1_, sub2_, sub3_;

  // constant
  const int LOOP_RATE_;  // processing frequency

  // variables
  bool is_linear_interpolation_, publishes_for_steering_robot_;
  bool is_waypoint_set_, is_pose_set_, is_velocity_set_, is_final_waypoint_reached;
  double current_linear_velocity_;
  double wheel_base_;

  double lookahead_distance_ratio_;
  double minimum_lookahead_distance_;  // the next waypoint must be outside of this threshold.

  // callbacks
  void callbackFromCurrentPose(const geometry_msgs::PoseStampedConstPtr &msg);
  void callbackFromCurrentVelocity(const nav_msgs::OdometryConstPtr &msg);
  void callbackFromWayPoints(const waypoint_follower::laneConstPtr &msg);

  // initializer
  void initForROS();

  // functions
  void publishTwist(const bool &can_get_curvature, const double &kappa) const;
  void publishControlCommandStamped(const bool &can_get_curvature, const double &kappa) const;

  double computeLookaheadDistance() const;
  double computeVelocity() const;
};

double convertCurvatureToSteeringAngle(const double &wheel_base, const double &kappa);

inline double kmph2mps(double velocity_kmph)
{
  return (velocity_kmph * 1000) / (60 * 60);
}

}  // waypoint_follower

#endif  // PURE_PURSUIT_CORE_H
