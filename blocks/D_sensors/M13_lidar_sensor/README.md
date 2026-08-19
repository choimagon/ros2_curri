# M13 — 2D LiDAR / LaserScan

## 만드는 파일

`agv_ws/src/agv_gazebo/models/agv/model.sdf`의 `gpu_lidar`와 `agv_ws/src/agv_sensors/agv_sensors/lidar_processor.py`를 만듭니다. 전자는 scan을 생성하고, 후자는 전방 ±15°의 최단 거리를 `/obstacle_distance`로 publish합니다.

## 만드는 순서

1. horizontal `samples`, min/max angle, min/max range, update rate를 설정합니다.
2. `/scan` bridge가 동작하는지 먼저 `ros2 topic echo /scan --once`로 봅니다.
3. processor는 `angle_min + index * angle_increment`로 각 range의 방향을 계산하고, `inf`/`nan`을 버립니다.

```bash
ros2 run agv_sensors lidar_processor
ros2 topic echo /obstacle_distance
ros2 topic hz /scan
```

## 확인

AGV 앞에 obstacle이 있을 때 `/obstacle_distance`가 실제 거리 근처로 내려가고 RViz LaserScan에도 반사점이 보이면 통과입니다.
