#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

// Python의 Node 클래스와 같은 역할을 하는 C++ ROS 2 node입니다.
class StatusPublisher : public rclcpp::Node
{
public:
  StatusPublisher()
  : Node("cpp_status_publisher"), sequence_(0)
  {
    // ros2 run 뒤 --ros-args -p message:=... 로 바꿀 수 있는 parameter입니다.
    this->declare_parameter<std::string>("message", "C++ AGV 상태 정상");

    // String 메시지를 /cpp_status topic으로 publish합니다. 마지막 10은 queue depth입니다.
    publisher_ = this->create_publisher<std_msgs::msg::String>("/cpp_status", 10);
    timer_ = this->create_wall_timer(1s, std::bind(&StatusPublisher::publish_status, this));
  }

private:
  void publish_status()
  {
    auto message = std_msgs::msg::String();
    message.data = this->get_parameter("message").as_string() + " #" + std::to_string(sequence_++);
    publisher_->publish(message);
    RCLCPP_INFO(this->get_logger(), "published: %s", message.data.c_str());
  }

  std::size_t sequence_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<StatusPublisher>());
  rclcpp::shutdown();
  return 0;
}
