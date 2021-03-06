
#include "pure_pursuit.h"

namespace waypoint_follower
{
// Constructor
PurePursuit::PurePursuit()
  : RADIUS_MAX_(9e10)
  , KAPPA_MIN_(1 / RADIUS_MAX_)
  , is_linear_interpolation_(true)
  , is_finalwaypoint_reach_flag(false)
  , next_waypoint_number_(0) //-1
  , lookahead_waypoint_(3)
  , lookahead_distance_(0)
  , current_linear_velocity_(0)
  , reach_target_distance_(0.4)
{
}

// Destructor
PurePursuit::~PurePursuit()
{
}

double PurePursuit::calcCurvature(geometry_msgs::Point target) const
{
  double kappa;
  double denominator = pow(getPlaneDistance(target, current_pose_.position), 2);
  double numerator = 2 * calcRelativeCoordinate(target, current_pose_).y;

  if (denominator != 0)
    kappa = numerator / denominator;
  else
  {
    if (numerator > 0)
      kappa = KAPPA_MIN_;
    else
      kappa = -KAPPA_MIN_;
  }
  ROS_INFO("kappa : %lf", kappa);
  return kappa;
}

// linear interpolation of next target
bool PurePursuit::interpolateNextTarget(int next_waypoint, geometry_msgs::Point *next_target) const
{
  constexpr double ERROR = pow(10, -5);  // 0.00001

  // int path_size = static_cast<int>(current_waypoints_.size());
  if (next_waypoint == total_waypoint_number_ - 1)
  {
    *next_target = current_waypoints_.at(next_waypoint).pose.pose.position;
    return true;
  }
  double search_radius = lookahead_distance_;
  geometry_msgs::Point zero_p;
  geometry_msgs::Point end = current_waypoints_.at(next_waypoint).pose.pose.position;
  geometry_msgs::Point start = current_waypoints_.at(next_waypoint - 1).pose.pose.position;

  // let the linear equation be "ax + by + c = 0"
  // if there are two points (x1,y1) , (x2,y2), a = "y2-y1, b = "(-1) * x2 - x1" ,c = "(-1) * (y2-y1)x1 + (x2-x1)y1"
  double a = 0;
  double b = 0;
  double c = 0;
  double get_linear_flag = getLinearEquation(start, end, &a, &b, &c);
  if (!get_linear_flag)
    return false;

  // let the center of circle be "(x0,y0)", in my code , the center of circle is vehicle position
  // the distance  "d" between the foot of a perpendicular line and the center of circle is ...
  //    | a * x0 + b * y0 + c |
  // d = -------------------------------
  //          √( a~2 + b~2)
  double d = getDistanceBetweenLineAndPoint(current_pose_.position, a, b, c);

  // ROS_INFO("a : %lf ", a);
  // ROS_INFO("b : %lf ", b);
  // ROS_INFO("c : %lf ", c);
  // ROS_INFO("distance : %lf ", d);

  if (d > search_radius)
    return false;

  // unit vector of point 'start' to point 'end'
  tf::Vector3 v((end.x - start.x), (end.y - start.y), 0);
  tf::Vector3 unit_v = v.normalize();

  // normal unit vectors of v
  tf::Vector3 unit_w1 = rotateUnitVector(unit_v, 90);   // rotate to counter clockwise 90 degree
  tf::Vector3 unit_w2 = rotateUnitVector(unit_v, -90);  // rotate to counter clockwise 90 degree

  // the foot of a perpendicular line
  geometry_msgs::Point h1;
  h1.x = current_pose_.position.x + d * unit_w1.getX();
  h1.y = current_pose_.position.y + d * unit_w1.getY();
  h1.z = current_pose_.position.z;

  geometry_msgs::Point h2;
  h2.x = current_pose_.position.x + d * unit_w2.getX();
  h2.y = current_pose_.position.y + d * unit_w2.getY();
  h2.z = current_pose_.position.z;

  // ROS_INFO("error : %lf", error);
  // ROS_INFO("whether h1 on line : %lf", h1.y - (slope * h1.x + intercept));
  // ROS_INFO("whether h2 on line : %lf", h2.y - (slope * h2.x + intercept));

  // check which of two foot of a perpendicular line is on the line equation
  geometry_msgs::Point h;
  if (fabs(a * h1.x + b * h1.y + c) < ERROR)
  {
    h = h1;
    //   ROS_INFO("use h1");
  }
  else if (fabs(a * h2.x + b * h2.y + c) < ERROR)
  {
    //   ROS_INFO("use h2");
    h = h2;
  }
  else
  {
    return false;
  }

  // get intersection[s]
  // if there is a intersection
  if (d == search_radius)
  {
    *next_target = h;
    return true;
  }
  else
  {
    // if there are two intersection
    // get intersection in front of vehicle
    double s = sqrt(pow(search_radius, 2) - pow(d, 2));
    geometry_msgs::Point target1;
    target1.x = h.x + s * unit_v.getX();
    target1.y = h.y + s * unit_v.getY();
    target1.z = current_pose_.position.z;

    geometry_msgs::Point target2;
    target2.x = h.x - s * unit_v.getX();
    target2.y = h.y - s * unit_v.getY();
    target2.z = current_pose_.position.z;

    // ROS_INFO("target1 : ( %lf , %lf , %lf)", target1.x, target1.y, target1.z);
    // ROS_INFO("target2 : ( %lf , %lf , %lf)", target2.x, target2.y, target2.z);
    // displayLinePoint(a, b, c, target1, target2, h);  // debug tool

    // check intersection is between end and start
    double interval = getPlaneDistance(end, start);
    if (getPlaneDistance(target1, end) < interval)
    {
      // ROS_INFO("result : target1");
      *next_target = target1;
      return true;
    }
    else if (getPlaneDistance(target2, end) < interval)
    {
      // ROS_INFO("result : target2");
      *next_target = target2;
      return true;
    }
    else
    {
      // ROS_INFO("result : false ");
      return false;
    }
  }
}

void PurePursuit::getNextWaypoint()
{
  total_waypoint_number_ = static_cast<int>(current_waypoints_.size());
  int waypoint_number_end;
  float temp_dist = 0.0;
  float shortest_dist = 1000000;

  // if waypoints are not given, do nothing.
  if (total_waypoint_number_ == 0)
  {
    next_waypoint_number_ = -1;
    return;
  }

  waypoint_number_end = next_waypoint_number_+lookahead_waypoint_ < total_waypoint_number_? 
                        next_waypoint_number_+lookahead_waypoint_ :total_waypoint_number_;

  for (int i = next_waypoint_number_; i < waypoint_number_end; i++) //next_waypoint_number_+lookahead_waypoint_
  {

    temp_dist = getPlaneDistance(current_waypoints_.at(i).pose.pose.position, current_pose_.position);
    // temp_dist = sqrt(
    //         pow(current_waypoints_.at(i).pose.pose.position.y - current_pose_.position.y, 2)
    //                 + pow(current_waypoints_.at(i).pose.pose.position.x - current_pose_.position.x,
    //                         2));

    // std::cout << "current waypoint pose: " << current_waypoints_.at(i).pose.pose.position.x << " " <<
    //               current_waypoints_.at(i).pose.pose.position.y << std::endl; 

    // std::cout << "distance: " << temp_dist << std::endl;
    // std::cout << "lookahead distance: " << lookahead_distance_ << std::endl;     
    // std::cout << "shortest distance: " << shortest_dist << std::endl;

    if (temp_dist > lookahead_distance_ && (temp_dist-shortest_dist) < 0.001 )
    {
      // std::cout << "changed" << std::endl;
      // std::cout << "i" << i << std::endl;
      shortest_dist = temp_dist;
      next_waypoint_number_ = i;

    }
    // std::cout << "plane distance: " << temp_dist << std::endl;
    // std::cout << "look ahead distance: " << lookahead_distance_ <<  std::endl;
    // std::cout << "shortest_dist: " << shortest_dist <<  std::endl;

  }

  // std::cout << "######################################" << std::endl;
  // std::cout << "current pose: "<< current_pose_.position.x << " " << current_pose_.position.y << std::endl;
  // std::cout << "next waypoint index: " << next_waypoint_number_ << std::endl;;
  // std::cout << "total number of waypoints: " << static_cast<int>(current_waypoints_.size()) << std::endl;;

  if (next_waypoint_number_ == (total_waypoint_number_ - 1))
    {
      if (temp_dist < reach_target_distance_)
      {
        is_finalwaypoint_reach_flag = true;        
      }
      ROS_INFO("search waypoint is the last");
      return;
    }
  else
    return;

  // if this program reaches here , it means we lost the waypoint!
  next_waypoint_number_ = -1;

  return;
}

bool PurePursuit::canGetCurvature(double *output_kappa)
{
  // search next waypoint
  getNextWaypoint();

  if (next_waypoint_number_ == -1)
  {
    ROS_INFO("lost next waypoint");
    return false;
  }

  // if is_linear_interpolation_ is false or next waypoint is first or last
  if (!is_linear_interpolation_ || next_waypoint_number_ == 0 ||
      next_waypoint_number_ == (static_cast<int>(current_waypoints_.size() - 1)))
  
  {
    next_target_position_ = current_waypoints_.at(next_waypoint_number_).pose.pose.position;
    *output_kappa = calcCurvature(next_target_position_);
    return true;
  }

  // linear interpolation and calculate angular velocity
  bool interpolation = interpolateNextTarget(next_waypoint_number_, &next_target_position_);

  if (!interpolation)
  {
    ROS_INFO_STREAM("lost target! ");
    return false;
  }

  // ROS_INFO("next_target : ( %lf , %lf , %lf)", next_target.x, next_target.y,next_target.z);

  *output_kappa = calcCurvature(next_target_position_);
  return true;
}

}  // waypoint_follower