
#include <chrono>
#include <algorithm>
#include <iostream>

template <typename T>
inline T mathClamp(const T& x_val, const T& min_val, const T& max_val) {
  return std::max(min_val, std::min(x_val, max_val));
}

class PID {
public:
  explicit PID(const double& p,
               const double& i,
               const double& d) {
    kp = p;
    ki = i;
    kd = d;

    sample_time = 0;
    current_time = TimeNow();
    last_time = current_time;
    Clear();

  }

  virtual ~PID() = default;

  inline void Clear() {
    pterm = 0;
    iterm = 0;
    dterm = 0;
    last_error = 0;
    int_error = 0;
    windup_guard = 20;
    output = 0;
  }

  double Update(const double& fb_value,
                const double& t_value) {

    target_val = t_value;
    double error = target_val - fb_value;
    std::cout << "error: " << error << std::endl;
    current_time = TimeNow();
    double delta_time = current_time - last_time;
    double delta_error = error - last_error;

    if (delta_time >= sample_time) {
      pterm = kp*error;
      iterm += error*delta_time;
      iterm = mathClamp<double>(iterm, -windup_guard, windup_guard);
      dterm = delta_time>0?delta_error/delta_time:0;
      last_time = current_time;
      last_error = error;
      output = pterm + (ki*iterm) + (kd*dterm);
    }
    return output;
  }

  double Update(const double& fb_value) {

    double error = target_val - fb_value;
    current_time = TimeNow();
    double delta_time = current_time - last_time;
    double delta_error = error - last_error;

    if (delta_time > sample_time) {
      pterm = kp*error;
      iterm += error*delta_time;
      iterm = mathClamp<double>(iterm, -windup_guard, windup_guard);
      dterm = delta_time>0?delta_error/delta_time:0;
      last_time = current_time;
      last_error = error;
      output = pterm + (ki*iterm) + (kd*dterm);
    }
    return output;
  }

  inline double GetOutput() const {
    return output;
  }

  inline void SetTarget(const double& val) {
    target_val = val;
  }

  inline void SetKp(const double& proportional_gain) {
    kp = proportional_gain;
  }

  inline void SetKi(const double& integral_gain) {
    ki = integral_gain;
  }

  inline void SetKd(const double& derivative_gain) {
    kd = derivative_gain;
  }

  inline void SetWindUp(const double& windup) {
    windup_guard = windup;
  }

  inline void SetSampleTime(const double& sample_time_val) {
    sample_time = sample_time_val;
  }

  double TimeNow() {
    auto now = std::chrono::system_clock::now();
    auto nano_time_point = std::chrono::time_point_cast<std::chrono::nanoseconds>(now);
    auto epoch = nano_time_point.time_since_epoch();
    uint64_t now_nano = std::chrono::duration_cast<std::chrono::nanoseconds>(epoch).count();
    auto now_double = static_cast<double>(now_nano) / 1000000000UL;
    return now_double;
  }

private:
  double kp, ki, kd;
  double sample_time;
  double target_val;
  double current_time, last_time;
  double pterm, iterm, dterm;
  double last_error;
  double int_error;
  double windup_guard;
  double output;
};