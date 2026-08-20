# ROS 2 기반 AGV End-to-End 개발 커리큘럼

초보자가 빈 workspace에서 AGV를 처음부터 끝까지 직접 만드는 ROS 2 + Gazebo 실습 저장소입니다. 기준 조합은 **Ubuntu 24.04 LTS + ROS 2 Jazzy + Gazebo Harmonic**입니다.

## 시작 순서

1. 먼저 [설치 및 환경 확인 안내](docs/INSTALL_UBUNTU_24.04_ROS2_JAZZY.md)를 끝까지 실행합니다.
2. 새 터미널에서 `source /opt/ros/jazzy/setup.bash`를 실행합니다.
3. Block A의 M01을 실행한 뒤, M02 PPT의 명령으로 빈 `~/ros2_curri/my_agv_ws`와 첫 package를 직접 만듭니다.
4. 이후 각 PPT에서 `my_agv_ws`에 폴더·파일·코드를 직접 추가하고, 해당 모듈의 build/source/run 검증을 통과한 뒤 다음 Block으로 이동합니다.

## 폴더 안내

| 경로 | 용도 |
| --- | --- |
| `docs/` | ROS 2·Gazebo 설치 및 전체 검증 안내 |
| `blocks/` | A–F 교육 구간과 M01–M22별 README, Starter/Complete, 실제 검증 로그·캡처, 따라 하기 PPT |
| `agv_ws/` | 강의 자료 생성·검증에 쓰는 완성 참고 소스와 Complete의 원본 |
| `~/ros2_curri/my_agv_ws/` | 학습자가 M02부터 빈 상태에서 직접 만드는 개인 workspace (처음에는 없음) |
| `ROS_2_기반_AGV_End-to-End_개발_커리큘럼_전체_통합_따라하기.pptx` | Block A~F와 M01~M22 전체를 순서대로 합친 강의·복습용 PPT |
| `scripts/` | 설치·커리큘럼 상태를 확인하는 점검 스크립트 |
| `tools/` | M01–M22 따라 하기 PPT와 실제 검증 캡처를 다시 생성하는 도구 |

처음 ROS 2 파일을 만드는 사람은 [Python·C++·URDF/Xacro·SDF·YAML·launch 파일 가이드](docs/BEGINNER_FILE_MAKING_GUIDE.md)를 먼저 읽습니다. 이 저장소에는 설명용으로 실제 실행 가능한 C++ 패키지 `agv_cpp_examples`도 포함되어 있습니다.

각 모듈 README에는 다음 네 가지를 반드시 적었습니다.

- 이번 구간의 목표와 선행 조건
- 새로 만들거나 수정할 실제 파일 경로
- 명령어가 실제로 하는 일과 바꿔 볼 수 있는 parameter/설정값
- 코드·URDF/SDF/YAML이 구현하는 구조와 실행 뒤 확인할 결과

PPT의 파일 구현 구간은 단순 코드 덩어리가 아닙니다. 빈 파일을 연 다음, 먼저 실제 코드/태그를 두 줄씩 보며 **이 줄의 뜻**과 **실행하면 어디서 확인되는지**를 설명하고, 이어서 같은 코드를 직접 입력합니다. 예를 들어 ROS publisher는 topic 출력과 `ros2 topic info` 결과를, Gazebo sensor는 sensor 설정과 실제 camera/LiDAR/IMU topic을 한 쌍으로 배웁니다.

실제 Gazebo, RViz, Camera topic 화면은 해당 모듈의 `screenshots/`에 저장합니다. 화면마다 파일명 순서와 source commit을 기록해 PPT의 결과가 어떤 코드 기준인지 추적할 수 있습니다.

## 따라 하기 PPT 사용법

가이드 반영 사항은 [PPT 배포 구조](docs/PPT_FOLLOW_ALONG_DELIVERY.md)에 정리했습니다. 각 M01–M22 폴더에 독립 실행용 PPTX가 있고, 각 Block 루트에는 해당 M 시리즈 전체를 순서대로 합친 `Block_*_M시리즈_통합_따라하기.pptx`가 있습니다. 저장소 루트의 [전체 통합 PPT](ROS_2_기반_AGV_End-to-End_개발_커리큘럼_전체_통합_따라하기.pptx)는 Block A~F의 M01~M22를 한 번에 강의·복습할 때 사용합니다. 이는 예전의 ‘실습 결과 명령어’ PPT가 아니라 개별 M 강의 자료를 모은 통합본입니다. 각 모듈 폴더는 다음 구조를 공통으로 사용합니다.

```text
MXX_module/
├── MXX_*.pptx                 # 강의·실습용 따라 하기 PPT
├── starter/                   # 시작 상태와 선행 조건
├── complete/                  # 막혔을 때 diff·backup 뒤 비교/복구할 핵심 파일 snapshot
├── screenshots/               # 실제 validation terminal / GUI 캡처
├── logs/                      # 실제 검증 명령 출력
└── CHECKSUM_or_TAG.txt        # Complete source SHA-256 manifest
```

| Block | 모듈별 PPT 폴더 |
| --- | --- |
| A — ROS 2 기초 | [M01–M04와 통합 PPT](blocks/A_ros2_basics/) |
| B — 로봇 제작 | [M05–M08와 통합 PPT](blocks/B_robot_build/) |
| C — 주행과 시각화 | [M09–M11와 통합 PPT](blocks/C_drive_visualization/) |
| D — 센서 | [M12–M15와 통합 PPT](blocks/D_sensors/) |
| E — 제어·인지·미션 | [M16–M20와 통합 PPT](blocks/E_autonomy_logic/) |
| F — 통합 | [M21–M22와 통합 PPT](blocks/F_integration/) |

## 커리큘럼 순서

- A — ROS 2 기초: M01–M04
- B — 로봇 제작: M05–M08
- C — 주행과 시각화: M09–M11
- D — 센서: M12–M15
- E — 제어·인지·미션: M16–M20
- F — 통합: M21–M22

## 빠른 상태 점검

```bash
bash scripts/verify_install.sh
bash scripts/verify_curriculum.sh
```

두 스크립트는 파일을 변경하거나 시스템에 설치하지 않습니다. 첫 번째는 ROS/Gazebo 설치 상태를, 두 번째는 M01–M22 안내 파일과 최종 프로젝트 핵심 파일 존재 여부를 확인합니다.

## 중요한 원칙

- 매 모듈을 끝낼 때마다 아래 모듈로 넘어가기 전에 `확인` 명령을 실행합니다.
- 학습자는 `agv_ws/`를 직접 수정하지 않습니다. 실제 구현은 `~/ros2_curri/my_agv_ws/`에서 하고, `complete/`은 오류가 해결되지 않을 때만 비교합니다.
- 이름과 토픽은 문서에 적힌 것을 그대로 사용합니다. 임의로 바꾸면 launch와 bridge 설정도 함께 바꿔야 합니다.
- Gazebo Classic (`gazebo`, `gazebo_ros_pkgs`)이 아니라 modern Gazebo의 `gz sim`, `ros_gz`를 사용합니다.
- YOLO는 선택 의존성입니다. M17 전까지는 설치하지 않아도 ROS/Gazebo 기초 실습을 진행할 수 있습니다.
