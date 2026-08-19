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
