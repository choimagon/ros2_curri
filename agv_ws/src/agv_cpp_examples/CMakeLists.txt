cmake_minimum_required(VERSION 3.8)
project(agv_cpp_examples)

# ament_cmake가 ROS 2 패키지를 빌드·설치하는 기본 도구입니다.
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# src/status_publisher.cpp를 실행 파일 하나로 컴파일합니다.
add_executable(status_publisher src/status_publisher.cpp)
ament_target_dependencies(status_publisher rclcpp std_msgs)

# ros2 run agv_cpp_examples status_publisher가 찾는 설치 경로입니다.
install(TARGETS
  status_publisher
  DESTINATION lib/${PROJECT_NAME})

ament_package()
