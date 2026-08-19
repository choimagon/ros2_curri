# M15 — 센서 운영과 동기화

## 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_bringup/config/sensors.yaml` | update rate, QoS/임계값, `use_sim_time`을 launch 밖으로 분리합니다. |
| `agv_ws/src/agv_sensors/agv_sensors/lidar_processor.py` | SensorDataQoS를 사용합니다. |
| `agv_ws/src/agv_sensors/agv_sensors/imu_monitor.py` | `use_sim_time` 적용 여부를 확인합니다. |

## 만드는 순서

시뮬레이션 노드는 `use_sim_time: true`를 받아 `/clock`을 사용합니다. Camera/LiDAR/IMU는 SensorDataQoS(대체로 best effort)가 맞으며, subscriber QoS가 incompatible이면 메시지가 아예 안 올 수 있습니다.

```bash
ros2 param get /lidar_processor use_sim_time
ros2 topic hz /scan
ros2 topic hz /imu/data
ros2 topic info /scan -v
```

## 확인

Gazebo를 pause하면 ROS node 시간도 멈추고, `topic hz`가 SDF update rate 근처를 보이며 각 메시지 `header.frame_id`가 TF에 존재하면 통과입니다.
