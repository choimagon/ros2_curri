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
