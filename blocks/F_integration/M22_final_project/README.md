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
