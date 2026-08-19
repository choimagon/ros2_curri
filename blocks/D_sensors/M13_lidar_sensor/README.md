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

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 run agv_sensors lidar_processor` | `setup.py`에 등록된 processor 노드를 시작해 `/scan`을 구독하고 `/obstacle_distance`를 publish합니다. | `--ros-args -p front_half_angle_deg:=30.0`으로 전방 검사 폭을 ±30°로 넓힐 수 있습니다. |
| `ros2 topic echo /obstacle_distance` | 계산된 `std_msgs/msg/Float32`를 계속 출력합니다. | 장애물이 없으면 `inf`, 장애물이 있으면 가장 가까운 유효 range(m)가 나오는지 봅니다. |
| `ros2 topic hz /scan` | scan의 실제 수신 주기를 계산합니다. | SDF의 `update_rate`(현재 10 Hz)를 바꾼 뒤 처리 주기가 같이 바뀌는지 확인합니다. |

## 내부 구현과 실행 뒤 보이는 결과

SDF의 `gpu_lidar`는 720 samples로 -π부터 +π까지 한 바퀴를 스캔하고, 0.12–12.0 m range를 10 Hz로 `/scan`에 publish합니다. bridge가 이를 ROS `LaserScan`으로 바꿉니다. `lidar_processor.py`는 `angle_min + index * angle_increment`로 각 sample의 방향을 복원한 뒤, 기본값 ±15° 안의 유한한 값만 고르고 최소값을 `Float32`로 냅니다. SensorDataQoS를 쓰는 이유는 시뮬레이터 센서의 best-effort 전달 방식과 호환하기 위해서입니다.

예를 들어 전방 0.48 m에 상자를 두면 `/obstacle_distance`는 약 `0.48`이 됩니다. 전방 영역에 유효한 range가 전혀 없으면 코드가 `inf`를 publish하므로, 그 값은 0 m 장애물이 아니라 “검사할 측정값 없음”입니다. samples를 늘리면 각도 해상도는 좋아지지만 메시지 크기와 연산량도 증가합니다.
