# Block A — ROS 2 기초 (M01–M04)

이 Block의 종료 조건은 Python과 C++ node가 각각 메시지를 publish하는 구조를 설명하고, AGV의 기본 TF tree를 RViz2에서 설명할 수 있는 것입니다. C++ 예제는 최종 AGV 기능이 아니라 `.py`와 `.cpp` 패키지 파일 구성을 비교하기 위한 실습입니다.

공통 시작 명령:

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_curri/agv_ws
colcon build --symlink-install --packages-select agv_control agv_cpp_examples agv_description
source install/setup.bash
```

순서대로 M01 → M04를 진행하고, 각 README의 `확인`을 통과한 뒤 다음 모듈로 갑니다.
