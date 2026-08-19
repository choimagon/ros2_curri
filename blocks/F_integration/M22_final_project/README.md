# M22 — Final Project: 가상 AGV 자율 미션

## 필수 파일과 제출 기준

최종 구조는 `agv_ws/src/`의 `agv_description`, `agv_gazebo`, `agv_control`, `agv_sensors`, `agv_vision`, `agv_mission`, `agv_interfaces`, `agv_bringup` 여덟 패키지입니다. `agv_bringup/launch/agv_sim.launch.py` 하나로 실행합니다.

| 마일스톤 | 증명 |
| --- | --- |
| 모델/TF | RViz RobotModel과 `view_frames` 결과 |
| 물리/주행 | Gazebo spawn과 `/cmd_vel` 주행 |
| 센서 | `/scan`, `/imu/data`, `/camera/image_raw` topic 확인 |
| 인지/안전 | detection, `/obstacle_distance`, 정지 log |
| 미션 | 최소 4개 상태가 전환되는 `/mission_state` log |
| 재현 | 단일 launch와 rosbag 1회 |

## 최종 실행

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_curri/agv_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch agv_bringup agv_sim.launch.py
```

처음에는 `enable_yolo: false`로 센서·안전·FSM 구조부터 통과시키고, 마지막에 YOLO를 켭니다. 문제 발생 시 launch 전체를 끄기 전 `ros2 node list`, `ros2 topic info -v`, `ros2 run tf2_tools view_frames`로 첫 단절 지점을 찾습니다.

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `colcon build --symlink-install` | `src/` 아래 8개 패키지와 interface message를 의존성 순서로 build/install합니다. | 수정한 패키지만 빠르게 볼 때는 `--packages-select 패키지명`을 쓰지만 최종 제출 전에는 전체 build를 실행합니다. |
| `source install/setup.bash` | 최종 실행이 이 workspace의 최신 launch·YAML·console script를 선택하도록 overlay를 올립니다. | 새 터미널/재빌드 뒤에는 다시 source합니다. |
| `ros2 launch agv_bringup agv_sim.launch.py` | 최종 AGV 시스템을 한 명령으로 조립합니다. | 첫 통합은 `rviz:=false` 또는 `enable_yolo: false` YAML로 부하를 줄인 뒤, 마지막에 UI·YOLO를 켭니다. |
| `ros2 node list` / `ros2 topic info -v` / `view_frames` | 실행 결과를 차례로 node, DDS topic/QoS, TF 연결 관점에서 진단합니다. | 처음 끊긴 계층만 고쳐 재시작하면 launch 전체를 추측으로 바꾸는 일을 줄일 수 있습니다. |

## 실제 구현 구조와 기대 결과

실제 흐름은 `Gazebo camera/LiDAR/IMU → ros_gz_bridge → ROS sensor node → mission_manager(/cmd_vel_raw) → safety_controller(/cmd_vel) → Gazebo DiffDrive`입니다. 모델 형상과 정적 sensor frame은 `agv_description`, Gazebo world·물리·sensor·bridge는 `agv_gazebo`, 사용자 메시지는 `agv_interfaces`, 단일 실행 조립은 `agv_bringup`이 담당합니다. 이 분리 덕분에 센서나 제어 코드만 바꿔도 URDF와 world 파일까지 함께 수정할 필요가 없습니다.

기본 `enable_yolo: false`에서는 camera image는 흐르지만 detection은 빈 배열이고 FSM은 `SEARCH` 상태로 회전합니다. LiDAR 전방에 장애물이 들어오면 safety controller가 `/cmd_vel`을 zero로 바꾸는 것이 현재 실제 통합 안전 동작입니다. YOLO 거리 추정·GOAL/STOP 완성은 후속 구현 항목이므로, 현재 결과와 확장 목표를 분리해 기록합니다.
