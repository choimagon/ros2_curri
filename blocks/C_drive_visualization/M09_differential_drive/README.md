# M09 — Differential Drive 구동

## 목표와 파일

`agv_ws/src/agv_gazebo/models/agv/model.sdf`의 `DiffDrive` plugin이 `/cmd_vel`을 받고, `agv_ws/src/agv_control/agv_control/cmd_test_node.py`가 `Twist`를 보냅니다. `wheel_radius=0.08`, `wheel_separation=0.38`은 SDF와 `controllers.yaml`에서 반드시 일치시킵니다.

## 만드는 순서

1. `model.sdf`에 left/right joint 이름, 바퀴 반지름, wheel separation, `/cmd_vel`, `/odom`을 적습니다.
2. `cmd_test_node.py`는 3초간만 저속 직진 후 zero Twist를 보내도록 만들었습니다. 초기 실습에서는 `linear_speed`를 0.15 이상으로 높이지 마세요.
3. `ros2 topic pub`으로도 한 번 검증합니다.

```bash
ros2 launch agv_gazebo gazebo.launch.py
# 다른 터미널
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.15}, angular: {z: 0.0}}"
```

## 확인

직진, 제자리 회전(`linear.x=0`, `angular.z=0.4`), 곡선 주행을 각각 해 보고 Gazebo에서 좌우 바퀴의 상대 속도 차이를 관찰합니다. 멈출 때는 Ctrl-C 뒤 zero Twist를 한 번 보냅니다.
