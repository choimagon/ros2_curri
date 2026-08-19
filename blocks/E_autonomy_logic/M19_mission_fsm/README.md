# M19 — Mission State Machine

## 만드는 파일

`agv_ws/src/agv_mission/agv_mission/mission_manager.py`는 `IDLE`로 시작해 실제 실행에서는 `SEARCH`, `APPROACH`, `AVOID`, `GOAL`을 전환하는 출발점이고, `agv_ws/src/agv_bringup/config/mission.yaml`은 속도·거리 임계값입니다. `STOP` 상태는 아직 구현하지 않은 확장 항목입니다.

## 만드는 순서

상태 전환을 함수/조건문 여기저기에 흩뜨리지 말고 `set_state()` 한 곳에서 log와 `/mission_state` publish를 합니다. 입력은 detection 유무와 obstacle distance, 출력은 `/cmd_vel_raw`입니다.

```bash
ros2 run agv_mission mission_manager
ros2 topic echo /mission_state
```

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 run agv_mission mission_manager` | 0.1초 timer(10 Hz)로 detection·장애물 입력을 읽어 state와 `/cmd_vel_raw`를 publish합니다. | YAML 또는 `--ros-args -p search_speed:=0.15 -p stop_distance:=0.70`으로 전환 속도·거리를 바꿉니다. |
| `ros2 topic echo /mission_state` | `std_msgs/msg/String`으로 publish되는 현재 state를 구독합니다. | `SEARCH`, `APPROACH`, `AVOID`, `GOAL` 변화와 terminal log를 함께 비교합니다. |
| `ros2 topic echo /cmd_vel_raw` | FSM이 의도한 원시 속도를 확인합니다. | 이 topic은 safety_controller를 거쳐 `/cmd_vel`로 전달되므로 둘을 구분해 관찰합니다. |

## 내부 구현과 실행 뒤 보이는 결과

`mission_manager.py`는 우선순위를 **가까운 장애물 → target 없음 → 목표 거리 도달 → target 접근** 순서로 둡니다. 장애물이 가까우면 `AVOID`와 `search_speed` 회전, target이 없으면 `SEARCH` 회전, target이 있으면 `APPROACH` 전진과 이미지 중심 오차 기반 회전(`-0.004 * error`, ±0.6 clamp)을 냅니다. state가 달라질 때만 log를 남기고 매 tick `/mission_state`를 publish합니다.

현재 YOLO node는 `estimated_distance=0.0`을 넣으므로 camera detection만으로는 `GOAL` 조건에 도달하지 않습니다. 거리 추정(깊이 카메라, LiDAR association, known-size 계산)을 추가했을 때만 0보다 크고 `stop_distance`보다 작은 값으로 `GOAL`을 시험할 수 있습니다. 따라서 지금 실제 결과는 보통 `SEARCH`이고, detection 주입 시 `APPROACH`, 전방 LiDAR 장애물 시 `AVOID`까지가 구현·검증 범위입니다.

## 확인

detection이 없을 때 SEARCH, detection이 들어올 때 APPROACH, LiDAR가 가까울 때 AVOID로 log가 바뀌어야 합니다. GOAL/STOP을 이미 구현된 것처럼 제출하지 말고, GOAL에는 거리 추정 추가가 필요하고 STOP은 후속 확장임을 기록합니다.
