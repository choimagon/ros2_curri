# M05 — URDF 기본 AGV 모델

## 목표

CAD 없이 box·cylinder·sphere만으로 body, 구동 바퀴 2개, caster, camera, LiDAR, IMU를 가진 AGV를 만듭니다.

## 이번 구간에서 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_description/urdf/agv.urdf.xacro` | 로봇의 link·joint·치수와 조립 순서입니다. |
| `agv_ws/src/agv_description/launch/display.launch.py` | RViz와 robot_state_publisher를 실행합니다. |
| `agv_ws/src/agv_description/rviz/agv.rviz` | RobotModel/TF를 보여 주는 RViz 기본 설정입니다. |

## 만드는 순서

1. `base_link`에 visual과 collision box를 같은 크기로 정의합니다.
2. 좌우 바퀴 link를 cylinder로 만들고 `continuous joint`로 연결합니다.
3. caster는 단순 sphere와 fixed joint로 시작합니다.
4. 세 센서는 physical link와 fixed joint를 만들고, camera에는 optical frame을 하나 더 둡니다.
5. 다음 명령으로 xacro 문법과 TF/RViz를 확인합니다.

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_curri/agv_ws
colcon build --symlink-install --packages-select agv_description
source install/setup.bash
xacro src/agv_description/urdf/agv.urdf.xacro > /tmp/agv.urdf
check_urdf /tmp/agv.urdf
ros2 launch agv_description display.launch.py
```

## 확인

`check_urdf`가 root link와 joint 수를 출력하고, RViz RobotModel에서 body·두 바퀴·세 센서가 보이면 통과입니다.
