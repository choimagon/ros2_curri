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

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `xacro ... > /tmp/agv.urdf` | macro·property·include가 든 xacro를 순수 URDF XML로 펼쳐 표준 출력으로 내보냅니다. `>`는 그 결과를 `/tmp/agv.urdf` 파일에 저장합니다. | 원본 xacro의 `body_length`, `body_width`, `wheel_radius`를 바꾼 뒤 생성 URDF의 `box size`, `cylinder radius`가 함께 바뀌는지 비교합니다. |
| `check_urdf /tmp/agv.urdf` | 펼쳐진 URDF의 XML, parent/child link 연결, joint 구성을 검사하고 root link·segment 수를 출력합니다. Gazebo 물리를 실행하는 명령은 아닙니다. | 오류가 나면 생성된 `/tmp/agv.urdf`를 열어 include/macro 결과부터 확인합니다. |
| `ros2 launch agv_description display.launch.py` | 생성된 모델을 RobotModel과 TF로 시각화합니다. | joint_state_publisher_gui에서 바퀴 joint 값을 조절해 회전축이 맞는지 봅니다. |

## 내부 구현과 실행 뒤 보이는 결과

`agv.urdf.xacro`는 본체를 box, 바퀴를 cylinder, caster를 sphere로 표현합니다. `visual`은 RViz에서 보이는 모양이고, `collision`은 접촉 판단에 쓸 단순 형상이며, `inertial`은 뒤의 물리 시뮬레이션이 쓸 질량·관성입니다. `base_link`의 box는 wheel radius와 body height를 이용해 바닥 위에 올라가도록 origin을 계산합니다.

결과 URDF에는 `base_footprint`, `base_link`, 좌·우 바퀴, caster, lidar/camera/imu와 camera optical frame이 생깁니다. RViz에서는 파란 직육면체 본체, 양옆 원통 바퀴, 앞쪽 센서 형상이 보이고, `check_urdf`는 하나의 root link와 연결된 joint tree를 출력해야 합니다. 보이는 모양만 맞아도 collision 또는 inertial이 빠지면 M07에서 불안정해질 수 있습니다.
