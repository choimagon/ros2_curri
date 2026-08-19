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

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 run agv_control safety_controller --ros-args -p stop_distance:=0.5` | `/scan`과 `/cmd_vel_raw`를 구독해 안전한 `/cmd_vel`만 publish하는 필터를 시작합니다. | `stop_distance`는 정지 거리(m), `front_half_angle_deg`는 검사할 전방 반각(기본 ±15°)입니다. |
| `ros2 topic pub --rate 10 /cmd_vel_raw geometry_msgs/msg/Twist "{linear: {x: 0.10}}"` | 미션 노드 대신 테스트 CLI가 원시 전진 명령을 초당 10회 보냅니다. | `linear.x`가 0 이하(정지/후진)이면 현재 safety code는 장애물이 있어도 통과시킵니다. |
| `ros2 topic echo /cmd_vel` | safety filter 뒤의 실제 Gazebo 입력 명령을 봅니다. | 장애물 안에서는 모든 값이 0인 `Twist`가 출력되는지 확인합니다. |

## 내부 구현과 실행 뒤 보이는 결과

`safety_controller.py`는 `/obstacle_distance`를 직접 읽지 않고, `/scan`에서 다시 전방 sector의 유한 range 최소값을 계산합니다. 그 값이 `stop_distance`보다 작고 원시 명령이 전진이면 warning을 남기고 새로 만든 zero `Twist`를 `/cmd_vel`로 보냅니다. 그렇지 않으면 원시 명령을 그대로 전달합니다. 즉 vision에서 target을 봐도 LiDAR 정지 조건이 항상 우선입니다.

전방 0.5 m 안에 box가 있을 때에는 `obstacle at 0.42 m: stopping forward command` 같은 로그와 `linear.x: 0.0` 결과가 나와야 합니다. obstacle이 측면에만 있으면 기본 ±15° sector 밖이라 정지하지 않습니다. 통로 폭에 맞춰 sector를 30°로 넓히면 조기 정지는 늘지만 좁은 옆 장애물에 과민해질 수 있습니다.
