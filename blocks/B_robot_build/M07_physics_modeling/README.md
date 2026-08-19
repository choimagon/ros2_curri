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
