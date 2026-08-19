# Block A — ROS 2 기초 (M01–M04)

이 Block의 종료 조건은 두 개의 Python 노드가 메시지를 주고받고, AGV의 기본 TF tree를 RViz2에서 설명할 수 있는 것입니다.

공통 시작 명령:

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_curri/agv_ws
colcon build --symlink-install --packages-select agv_control agv_description
source install/setup.bash
```

순서대로 M01 → M04를 진행하고, 각 README의 `확인`을 통과한 뒤 다음 모듈로 갑니다.
