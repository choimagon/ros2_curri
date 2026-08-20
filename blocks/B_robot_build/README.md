# Block B — AGV 로봇 제작 (M05–M08)

종료 조건은 직접 만든 AGV가 link/joint/inertial/collision 정보를 가지고 Gazebo World에 들어가는 것입니다.

## Block 커리큘럼 요약

| 순서 | 이번 단계에서 처음 만드는 것 | 아직 넣지 않는 것 |
| --- | --- | --- |
| M05 | Xacro 없는 단일 `agv.urdf` | macro/property |
| M06 | Xacro property·wheel macro | Gazebo 구동·센서 |
| M07 | visual/collision/inertia/friction SDF | drive plugin·Camera·LiDAR·IMU |
| M08 | warehouse World와 AGV spawn | `/cmd_vel`, `/odom`, 모든 센서 |

이렇게 만든 기준선은 M09에서 Differential Drive를 추가하는 출발점입니다. [M 시리즈 통합 PPT](Block_B_M시리즈_통합_따라하기.pptx)에는 M05 → M08 개별 PPT 전체가 순서대로 들어 있습니다.
