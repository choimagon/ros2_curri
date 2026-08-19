# agv_cpp_examples — C++ ROS 2 첫 파일

이 패키지는 최종 AGV의 필수 구성요소가 아니라, Python 패키지와 C++ 패키지의 파일 구성을 비교하기 위한 교육용 예제입니다.

```bash
cd ~/ros2_curri/agv_ws
colcon build --packages-select agv_cpp_examples
source install/setup.bash
ros2 run agv_cpp_examples status_publisher --ros-args -p message:='C++ 노드 시작'
# 다른 터미널: ros2 topic echo /cpp_status
```

`status_publisher.cpp`는 1초마다 `std_msgs/msg/String`을 `/cpp_status`로 publish합니다. `CMakeLists.txt`의 `add_executable`과 `install`이 빠지면 컴파일되더라도 `ros2 run`으로 실행할 수 없습니다.
