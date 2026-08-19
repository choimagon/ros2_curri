# M07 — Gazebo용 물리 모델링

## 목표

보이는 URDF와 움직이는 Gazebo 모델의 차이를 이해하고 collision, inertial, mass, friction을 검사합니다.

## 이번 구간에서 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_description/urdf/common.xacro` | body/wheel inertia를 계산합니다. |
| `agv_ws/src/agv_gazebo/models/agv/model.sdf` | Gazebo가 실제 물리를 계산할 SDF 모델입니다. |

## 만드는 순서

1. URDF의 모든 움직이는 link에 `inertial`을 넣습니다. `mass=0`이나 모든 inertia가 0이면 물리 엔진이 불안정합니다.
2. visual보다 collision shape를 단순하게 유지합니다. 처음에는 box/cylinder가 가장 안전합니다.
3. SDF의 wheel collision 표면에 friction을 설정합니다.
4. Gazebo에서 로봇이 뜨거나 떨리면 collision끼리 겹치지 않는지, wheel 중심 높이가 반지름과 맞는지, 질량 중심이 너무 높은지 순서대로 봅니다.

## 확인

M08의 Gazebo를 실행한 뒤 10초 동안 AGV가 바닥을 뚫거나 폭발하지 않으면 통과입니다. 문제가 있으면 무작정 mass를 크게 하지 말고 collision 겹침부터 수정합니다.

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `gz sdf -k src/agv_gazebo/models/agv/model.sdf` | Gazebo SDF 파일의 XML 구조와 schema를 검사합니다. 모델을 화면에 띄우지 않고 태그 오류를 먼저 잡습니다. | 수정할 때마다 실행해 sensor, plugin, collision 태그의 오타를 Gazebo 시작 전 확인합니다. |
| `ros2 launch agv_gazebo gazebo.launch.py` | World와 SDF AGV를 실제 물리 엔진에 올려 질량·관성·collision·마찰이 함께 작동하는지 봅니다. | 정지 상태를 비교할 때는 명령을 보내지 않고 10초 관찰합니다. |

## 내부 구현과 실행 뒤 보이는 결과

URDF는 주로 TF/RViz용 모델이고, Gazebo가 계산하는 물리 모델은 `model.sdf`입니다. 이 SDF는 base_link 질량 12.0 kg, 좌우 바퀴 질량 0.6 kg, 각각의 inertia tensor와 충돌 원통을 정의합니다. 바퀴 collision의 `mu`, `mu2`는 현재 1.0으로, 바닥과의 종·횡방향 마찰을 정합니다. visual은 파란 body를 보이게 하지만 물리적인 접촉은 `collision` 형상으로 처리됩니다.

`gz sdf -k`가 조용히 끝나면 문법상 유효한 SDF입니다. 실행 결과에서는 AGV가 바닥 위에서 정지하며, `/cmd_vel`을 주기 전에는 바퀴가 임의로 돌아가거나 본체가 튀지 않아야 합니다. 차체가 흔들리면 mass만 키우기보다 먼저 바퀴·caster collision이 floor와 처음부터 겹치는지, wheel 중심 z가 반지름과 맞는지를 확인합니다.
