
#include "pure_pursuit_core.h"

namespace waypoint_follower
{
// Constructor
PurePursuitNode::PurePursuitNode()
  : private_nh_("~")
  , pp_()
  , LOOP_RATE_(10) // 30
  , is_waypoint_set_(false)
  , is_pose_set_(false)
  , is_velocity_set_(false)
  , is_final_waypoint_reached(false)
  , current_linear_velocity_(0)
  , lookahead_distance_ratio_(1.0)
  , minimum_lookahead_distance_(1.0) // 6.0
{
  initForROS();

  // initialize for PurePursuit
  pp_.setLinearInterpolationParameter(is_linear_interpolation_);
}

// Destructor
PurePursuitNode::~PurePursuitNode()
{
}

void PurePursuitNode::initForROS()
{
  // ros parameter settings
  private_nh_.param("is_linear_interpolation", is_linear_interpolation_, bool(false));
  private_nh_.param("vehicle_info/wheel_base", wheel_base_, double(2.7));
  private_nh_.param("linear_velocity", current_linear_velocity_, double(0.4));

  // setup subscriber
  sub1_ = nh_.subscribe("/final_waypoints", 10, &PurePursuitNode::callbackFromWayPoints, this);
  sub2_ = nh_.subscribe("/gnss_pose", 10, &PurePursuitNode::callbackFromCurrentPose, this);
  sub3_ = nh_.subscribe("/husky_velocity_controller/odom", 10, &PurePursuitNode::callbackFromCurrentVelocity, this);

  // setup publisher
  pub1_ = nh_.advertise<geometry_msgs::Twist>("/cmd_vel", 10);
  pub2_ = nh_.advertise<waypoint_follower::ControlCommandStamped>("/ctrl_cmd", 10);

  // setup viz publisher
  pub11_ = nh_.advertise<visualization_msgs::Marker>("next_waypoint_mark", 0);
  pub12_ = nh_.advertise<visualization_msgs::Marker>("next_target_mark", 0);
  pub13_ = nh_.advertise<visualization_msgs::Marker>("search_circle_mark", 0);
  pub14_ = nh_.advertise<visualization_msgs::Marker>("line_point_mark", 0);  // debug tool
  pub15_ = nh_.advertise<visualization_msgs::Marker>("trajectory_circle_mark", 0);

}

void PurePursuitNode::run()
{
  ROS_INFO_STREAM("pure pursuit start");
  ros::Rate loop_rate(LOOP_RATE_);
  while (ros::ok())
  {
    ros::spinOnce();

    if (pp_.isFinalwaypointReach())
    {
      break;
    }

    // ROS_INFO("  pose   subscribed: %i", is_pose_set_);
    // ROS_INFO("velocity subscribed: %i", is_velocity_set_);
    // ROS_INFO("waypoint subscribed: %i", is_waypoint_set_);
    if (!is_pose_set_ || !is_waypoint_set_ || !is_velocity_set_)
    {
      ROS_WARN("Necessary topics are not subscribed yet ... ");
      loop_rate.sleep();
      continue;
    }

    pp_.setLookaheadDistance(computeLookaheadDistance());

    double kappa = 0;
    bool can_get_curvature = pp_.canGetCurvature(&kappa);
    publishTwist(can_get_curvature, kappa);
    publishControlCommandStamped(can_get_curvature, kappa);

    // for visualization with Rviz
    pub11_.publish(displayNextWaypoint(pp_.getPoseOfNextWaypoint()));
    pub13_.publish(displaySearchRadius(pp_.getCurrentPose().position, pp_.getLookaheadDistance()));
    pub12_.publish(displayNextTarget(pp_.getPoseOfNextTarget()));
    pub15_.publish(displayTrajectoryCircle(
        waypoint_follower::generateTrajectoryCircle(pp_.getPoseOfNextTarget(), pp_.getCurrentPose())));

    is_pose_set_ = false;
    is_velocity_set_ = false;
    is_waypoint_set_ = false;
    loop_rate.sleep();

    // std::cout << current_linear_velocity_ << std::endl;
  }

  ROS_INFO_STREAM("pure pursuit done");  

}

void PurePursuitNode::publishTwist(const bool &can_get_curvature, const double &kappa) const
{
  geometry_msgs::Twist ts;
  ts.linear.x = can_get_curvature ? computeVelocity() : 0;
  ts.angular.z = can_get_curvature ? kappa * ts.linear.x : 0;
  pub1_.publish(ts);
}

void PurePursuitNode::publishControlCommandStamped(const bool &can_get_curvature, const double &kappa) const
{

  waypoint_follower::ControlCommandStamped ccs;
  ccs.header.stamp = ros::Time::now();
  ccs.cmd.linear_velocity = can_get_curvature ? computeVelocity() : 0;
  ccs.cmd.steering_angle = can_get_curvature ? convertCurvatureToSteeringAngle(wheel_base_, kappa) : 0;

  pub2_.publish(ccs);
}

double PurePursuitNode::computeLookaheadDistance() const
{

  double maximum_lookahead_distance = current_linear_velocity_ * 10;
  double ld = current_linear_velocity_ * lookahead_distance_ratio_;
  double returned_ld = ld < minimum_lookahead_distance_ ? minimum_lookahead_distance_
        : ld > maximum_lookahead_distance ? maximum_lookahead_distance
        : ld;

  // std::cout << "returned ld: " << returned_ld << std::endl;

  return returned_ld;
}

double PurePursuitNode::computeVelocity() const
{
  if (pp_.getIndexOfNextWaypoint() == 0)
  {
    return current_linear_velocity_*0.5;
  }
  if (pp_.getIndexOfNextWaypoint() == (pp_.getTotalNumOfWaypoint()-1))
  {
    return current_linear_velocity_*0.5;  
  }
  
  return current_linear_velocity_;
}

void PurePursuitNode::callbackFromCurrentPose(const geometry_msgs::PoseStampedConstPtr &msg)
{
  pp_.setCurrentPose(msg);
  is_pose_set_ = true;
}

void PurePursuitNode::callbackFromCurrentVelocity(const nav_msgs::OdometryConstPtr &msg)
{
  // current_linear_velocity_ = 0.4;
  pp_.setCurrentVelocity(current_linear_velocity_);
  is_velocity_set_ = true;
}

void PurePursuitNode::callbackFromWayPoints(const waypoint_follower::laneConstPtr &msg)
{
  pp_.setCurrentWaypoints(msg->waypoints);
  is_waypoint_set_ = true;
}

double convertCurvatureToSteeringAngle(const double &wheel_base, const double &kappa)
{
  return atan(wheel_base * kappa);
}

}  // waypoint_follower