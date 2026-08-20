# Block A — ROS 2 기초 (M01–M04)

이 Block의 종료 조건은 Python과 C++ node가 각각 메시지를 publish하는 구조를 설명하고, AGV의 기본 TF tree를 RViz2에서 설명할 수 있는 것입니다. C++ 예제는 최종 AGV 기능이 아니라 `.py`와 `.cpp` 패키지 파일 구성을 비교하기 위한 실습입니다.

공통 시작 명령:

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_curri/agv_ws
colcon build --symlink-install --packages-select agv_control agv_cpp_examples agv_description
source install/setup.bash
```

## Block 커리큘럼 요약

| 순서 | 핵심 결과 | 다음 단계로 넘기는 것 |
| --- | --- | --- |
| M01 | node·topic·message를 CLI로 관찰 | ROS 환경 source 습관 |
| M02 | Python/C++ 패키지를 colcon으로 빌드 | workspace·overlay |
| M03 | timer 기반 pub/sub 작성 | `/counter`, `/cmd_vel` 이해 |
| M04 | `map → odom → base_link` TF 관계 | URDF link/joint 기준 |

Block 전체 강의·복습은 [M 시리즈 통합 PPT](Block_A_M시리즈_통합_따라하기.pptx)를, 직접 실습은 M01 → M04 개별 PPT를 사용합니다.
