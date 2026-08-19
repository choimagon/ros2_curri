# M21 — Parameter, YAML, Launch, rosbag2

## 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_bringup/config/robot.yaml` | 공통 `use_sim_time`입니다. |
| `agv_ws/src/agv_bringup/config/sensors.yaml` | LiDAR/IMU 파라미터입니다. |
| `agv_ws/src/agv_bringup/config/vision.yaml` | YOLO 모델과 threshold입니다. |
| `agv_ws/src/agv_bringup/config/mission.yaml` | 상태머신 속도·정지 거리입니다. |
| `agv_ws/src/agv_bringup/launch/agv_sim.launch.py` | 최종 단일 실행 진입점입니다. |

## 만드는 순서와 확인

코드에 숫자를 박지 말고 YAML로 이동합니다. launch는 Gazebo → bridge → robot_state_publisher → sensor/vision/mission/safety 순서를 한 LaunchDescription에 담습니다.

```bash
ros2 launch agv_bringup agv_sim.launch.py
ros2 bag record -o ~/agv_bag_01 /scan /imu/data /odom /camera/image_raw
# Ctrl-C로 기록 종료 후
ros2 bag info ~/agv_bag_01
ros2 bag play ~/agv_bag_01 --clock
```

bag 재생 중 처리 노드는 `use_sim_time: true`여야 합니다. `ros2 bag info`에 topic과 메시지 수가 보이면 통과입니다.

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 launch agv_bringup agv_sim.launch.py` | 한 LaunchDescription에서 Gazebo+bridge, robot_state_publisher, LiDAR/IMU/vision/mission/safety node, 기본 RViz를 시작합니다. | `rviz:=false`를 붙이면 RViz만 제외해 느린 PC에서 Gazebo·sensor pipeline만 시험할 수 있습니다. |
| `ros2 bag record -o ~/agv_bag_01 ...` | 적은 topic을 새 bag 디렉터리와 SQLite/metadata로 기록합니다. 메시지를 변환하거나 재생하지 않습니다. | 저장 공간을 줄이려면 필요한 topic만 기록하고, `-o` 이름으로 실험 회차를 구분합니다. |
| `ros2 bag info ~/agv_bag_01` | bag의 길이, 메시지 수, topic type을 읽기 전용으로 요약합니다. | 첫 기록 뒤 topic 하나라도 0건이면 launch/bridge를 고친 뒤 다시 기록합니다. |
| `ros2 bag play ~/agv_bag_01 --clock` | 저장한 순서대로 message를 재발행하고 `/clock`도 내보냅니다. | playback 처리 노드는 `use_sim_time: true`여야 기록 시간 기준으로 동작합니다. |

## 내부 구현과 실행 뒤 보이는 결과

`agv_sim.launch.py`는 먼저 Gazebo launch를 include하고, xacro 결과를 `robot_description`으로 넘기는 robot_state_publisher를 시작합니다. 그 뒤 sensors.yaml을 받는 LiDAR/IMU, vision.yaml의 yolo node, mission.yaml의 FSM과 safety controller를 실행하며, `rviz` launch argument가 true일 때만 RViz2를 추가합니다. 숫자는 코드에 박지 않고 robot/sensors/vision/mission YAML의 node 이름 아래 `ros__parameters`로 전달합니다.

정상 launch 로그에는 Gazebo와 `parameter_bridge`, `robot_state_publisher`, `lidar_processor`, `imu_monitor`, `yolo_node`, `mission_manager`, `safety_controller`가 각각 시작되었다고 나옵니다. bag 재생 때 `/clock`을 쓰지 않으면 node의 현재 시간이 recorded message의 header 시간과 어긋나므로, 재현 실험에서는 sim time과 `--clock`을 한 쌍으로 사용합니다.
