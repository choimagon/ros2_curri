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

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist "..."` | CLI publisher가 지정한 `Twist` 메시지를 초당 10회 `/cmd_vel`에 계속 보냅니다. `--rate`가 없으면 한 번만 보내므로 주행 plugin이 곧 멈출 수 있습니다. | `linear.x`는 직진(+)/후진(-) m/s, `angular.z`는 좌회전(+)/우회전(-) rad/s입니다. 초기에는 0.15 m/s, ±0.4 rad/s 이내로 둡니다. |
| `ros2 topic echo /odom --once` | DiffDrive가 계산한 위치·자세·속도 한 샘플을 받아 확인합니다. | 주행 전후 `pose.pose.position`을 비교하면 직진·회전 결과를 수치로 확인할 수 있습니다. |
| `ros2 run agv_control cmd_test_node --ros-args -p ...` | 코드로 만든 3초 제한 시험 명령을 publish합니다. | `linear_speed`, `angular_speed`를 동시에 주면 곡선 주행을 만듭니다. |

## 내부 구현과 실행 뒤 보이는 결과

SDF의 `gz::sim::systems::DiffDrive` plugin은 `left_wheel_joint`, `right_wheel_joint`를 받아 `wheel_radius=0.08`, `wheel_separation=0.38`로 차동 구동 운동학을 계산합니다. `/cmd_vel`은 plugin 입력, `/odom`은 계산 결과이고 `frame_id=odom`, `child_frame_id=base_link`로 publish됩니다. 이 두 기하 값이 URDF와 `controllers.yaml`에서 다르면 실제 바퀴 모양·주행 거리·odom이 서로 어긋납니다.

직진에서는 양쪽 바퀴가 같은 방향·비슷한 속도로 돌고, 제자리 회전에서는 서로 반대 방향으로 돕니다. `linear.x=0.15`, `angular.z=0.4`를 같이 주면 바깥쪽 바퀴가 더 빨라져 호를 그립니다. CLI publisher를 Ctrl-C로 멈춘 뒤에는 아래처럼 zero Twist를 한 번 보내 마지막 속도를 명시적으로 지울 수 있습니다.

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{}'
```
