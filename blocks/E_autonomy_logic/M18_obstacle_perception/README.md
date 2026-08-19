# M18 — LiDAR 장애물 감지와 Perception 결합

## 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_sensors/agv_sensors/lidar_processor.py` | 전방 sector 최소거리 `/obstacle_distance`를 계산합니다. |
| `agv_ws/src/agv_control/agv_control/safety_controller.py` | `/cmd_vel_raw`를 안전 확인 후 `/cmd_vel`로 전달합니다. |
| `agv_ws/src/agv_mission/agv_mission/mission_manager.py` | detection과 obstacle을 상태 전환에 함께 사용합니다. |

## 만드는 순서와 확인

LiDAR는 vision보다 안전 우선입니다. `/obstacle_distance < stop_distance`면 target이 보이더라도 forward command는 0이어야 합니다.

```bash
ros2 run agv_sensors lidar_processor
ros2 run agv_control safety_controller --ros-args -p stop_distance:=0.5
ros2 topic echo /obstacle_distance
ros2 topic echo /cmd_vel
```

박스를 AGV 전방 0.5m 안으로 옮겼을 때 safety_controller의 warning과 zero Twist가 나오면 통과입니다.
