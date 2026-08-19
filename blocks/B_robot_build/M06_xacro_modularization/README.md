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

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `xacro src/agv_description/urdf/agv.urdf.xacro > /tmp/agv.urdf` | `common.xacro`, `wheels.xacro`, `sensors.xacro`의 include와 macro 호출을 모두 펼쳐 중복 없는 원본이 실제 URDF에서 어떤 link/joint가 되는지 보여 줍니다. | `agv.urdf.xacro`의 `wheel_radius`를 0.08→0.12로 바꿔 다시 생성하고, 원래 값으로 되돌립니다. |
| `rg 'wheel_(link|joint)' /tmp/agv.urdf` | 생성된 URDF에서 바퀴 link/joint 이름이 실제로 몇 번 생겼는지 찾습니다. macro 정의 자체가 아니라 **확장 결과**를 검사합니다. | `left`/`right` 이름이 각각 한 쌍인지 확인합니다. |

## 내부 구현과 실행 뒤 보이는 결과

`common.xacro`는 box/cylinder의 관성을 계산하는 macro, `wheels.xacro`는 `side`, `y`, `radius`, `width` 인수를 받는 바퀴 macro, `sensors.xacro`는 이름·pose·크기를 받는 fixed sensor macro를 담당합니다. 최상위 `agv.urdf.xacro`는 본체 치수와 `wheel_radius`, `wheel_base`만 정의한 뒤 macro에 값을 전달합니다. 즉 왼쪽과 오른쪽 바퀴의 코드 복사본을 수정하는 대신, 한 property가 geometry와 joint 위치를 동시에 결정합니다.

반지름을 0.12로 바꾸면 생성 URDF의 wheel cylinder radius가 0.12가 되고 본체와 센서의 z 위치도 그 값에 맞춰 높아집니다. 바퀴 모양만 커지고 base가 바닥에 묻히면 property 연결이 빠진 것입니다. 이 파일의 값은 이후 SDF `wheel_radius=0.08`, `wheel_separation=0.38`과도 일치시켜야 실제 주행 속도와 odom이 맞습니다.
