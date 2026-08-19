# M19 — Mission State Machine

## 만드는 파일

`agv_ws/src/agv_mission/agv_mission/mission_manager.py`는 `IDLE → SEARCH → APPROACH → AVOID → GOAL → STOP`을 구현할 출발점이고, `agv_ws/src/agv_bringup/config/mission.yaml`은 속도·거리 임계값입니다.

## 만드는 순서

상태 전환을 함수/조건문 여기저기에 흩뜨리지 말고 `set_state()` 한 곳에서 log와 `/mission_state` publish를 합니다. 입력은 detection 유무와 obstacle distance, 출력은 `/cmd_vel_raw`입니다.

```bash
ros2 run agv_mission mission_manager
ros2 topic echo /mission_state
```

## 확인

detection이 없을 때 SEARCH, detection이 들어올 때 APPROACH, LiDAR가 가까울 때 AVOID로 순서대로 log가 바뀌어야 합니다. STOP 상태는 계속 zero Twist를 publish합니다.
