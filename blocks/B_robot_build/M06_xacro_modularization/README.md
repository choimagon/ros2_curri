# M06 — Xacro 모듈화와 파라미터

## 목표

반복되는 바퀴와 센서 정의를 macro로 분리하고, 치수 하나를 변경해도 geometry·joint 위치가 함께 바뀌게 만듭니다.

## 이번 구간에서 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_description/urdf/common.xacro` | material과 관성 계산 macro입니다. |
| `agv_ws/src/agv_description/urdf/wheels.xacro` | left/right가 공유하는 wheel macro입니다. |
| `agv_ws/src/agv_description/urdf/sensors.xacro` | fixed sensor link/joint macro입니다. |
| `agv_ws/src/agv_description/urdf/agv.urdf.xacro` | 세 모듈을 include하고 property를 주입하는 조립 파일입니다. |

## 만드는 순서

1. `common.xacro`에 box/cylinder inertia macro를 둡니다. 질량이 0이면 안 됩니다.
2. `wheels.xacro` macro의 인수는 `side`, `y`, `radius`, `width`로 둡니다.
3. 본체 파일에는 `wheel_radius`, `wheel_base` 같은 property만 두고, 실제 바퀴 link의 중복 코드는 제거합니다.
4. `wheel_radius`를 `0.08`에서 `0.12`로 잠시 바꾼 후 `xacro`를 다시 실행해 바퀴 geometry와 joint 높이가 함께 변하는지 확인하고 원래 값으로 되돌립니다.

## 확인

`xacro ... > /tmp/agv.urdf`가 오류 없이 끝나고 생성 URDF에 `left_wheel_joint`, `right_wheel_joint`가 각각 하나씩 있어야 합니다.
