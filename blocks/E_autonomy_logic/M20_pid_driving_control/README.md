# M20 — PID와 주행 제어

## 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_control/agv_control/pid_controller.py` | target error를 `/cmd_vel_raw`로 바꾸는 P 제어 출발점입니다. |
| `agv_ws/src/agv_bringup/config/mission.yaml` | 속도 상한과 목표 거리 같은 튜닝값입니다. |

## 만드는 순서

현재 코드의 P 제어부터 시험합니다. `angular.z = kp * bbox_center_error`를 사용하고 max angular speed로 clamp합니다. 흔들리면 먼저 `kp`를 낮추고, 그 다음 deadband와 D항을 추가합니다. 적분항은 steady-state error가 남을 때만 추가하고 anti-windup을 같이 넣습니다.

## 확인

같은 Gazebo 상황에서 `kp`를 세 값으로 바꿔 overshoot/oscillation을 비교 기록합니다. 어떤 gain도 safety_controller의 stop 조건을 우회해서는 안 됩니다.

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 run agv_control pid_controller` | `/target_error`의 `Twist`를 구독해 제한된 `/cmd_vel_raw`를 publish하는 현재 P-only controller를 시작합니다. | `kp_angular`(기본 0.004), `max_linear_speed`(0.25), `max_angular_speed`(0.8)를 parameter로 덮어쓸 수 있습니다. |
| `ros2 topic pub --rate 10 /target_error geometry_msgs/msg/Twist "{linear: {x: 0.15}, angular: {z: 100.0}}"` | 테스트용 목표 오차를 초당 10회 보냅니다. 현재 코드에서는 `linear.x`를 희망 전진 속도, `angular.z`를 조향 오차로 해석합니다. | 위 예의 각속도는 `100×0.004=0.4 rad/s`가 됩니다. 더 큰 오차는 ±0.8 clamp를 넘지 않습니다. |
| `ros2 topic echo /cmd_vel_raw` | P controller의 실제 계산 결과를 봅니다. | 안전 필터 뒤 `/cmd_vel`과 비교해 안전 정지가 여전히 적용되는지 봅니다. |

## 내부 구현과 실행 뒤 보이는 결과

현재 파일 이름은 PID이지만 구현은 의도적으로 **P 제어만** 합니다. `angular.z = target_error.angular.z × kp_angular`을 계산한 뒤 ±`max_angular_speed`로 자르고, `linear.x`는 0–`max_linear_speed` 사이로 clamp합니다. 적분 누적, 미분, anti-windup은 아직 없으므로 “완성 PID”라고 부르면 안 됩니다.

`kp_angular`이 너무 작으면 target 중앙으로 늦게 돌아가고, 너무 크면 좌우로 반복해 흔들립니다. P값을 0.002, 0.004, 0.008처럼 바꿔 같은 오차 입력에서 `/cmd_vel_raw.angular.z`와 Gazebo 궤적을 기록합니다. 이 출력은 반드시 M18 safety_controller의 입력(`/cmd_vel_raw`)으로 연결해 LiDAR 정지를 우회하지 않게 합니다.
