# ROS 2 + Gazebo AGV 실습 커리큘럼

워드 원본 `ROS2_Gazebo_AGV_교육_커리큘럼.docx`를 실제로 따라 만들 수 있는 실습 저장소입니다. 기준 조합은 **Ubuntu 24.04 LTS + ROS 2 Jazzy + Gazebo Harmonic**입니다.

## 시작 순서

1. 먼저 [설치 및 환경 확인 안내](docs/INSTALL_UBUNTU_24.04_ROS2_JAZZY.md)를 끝까지 실행합니다.
2. 새 터미널에서 `source /opt/ros/jazzy/setup.bash`를 실행합니다.
3. `cd agv_ws && colcon build --symlink-install`으로 워크스페이스를 빌드합니다.
4. `source install/setup.bash` 후 아래 Block 순서대로 실습합니다.

## 폴더 안내

| 경로 | 용도 |
| --- | --- |
| `docs/` | ROS 2·Gazebo 설치 및 전체 검증 안내 |
| `blocks/` | A–F 교육 구간과 M01–M22별 README, Starter/Complete, 실제 검증 로그·캡처, 따라 하기 PPT |
| `agv_ws/` | 빌드하여 실행하는 AGV ROS 2 패키지 소스 |
| `scripts/` | 설치·커리큘럼 상태를 확인하는 점검 스크립트 |
| `tools/` | M01–M22 따라 하기 PPT와 실제 검증 캡처를 다시 생성하는 도구 |

처음 ROS 2 파일을 만드는 사람은 [Python·C++·URDF/Xacro·SDF·YAML·launch 파일 가이드](docs/BEGINNER_FILE_MAKING_GUIDE.md)를 먼저 읽습니다. 이 저장소에는 설명용으로 실제 실행 가능한 C++ 패키지 `agv_cpp_examples`도 포함되어 있습니다.

각 모듈 README에는 다음 네 가지를 반드시 적었습니다.

- 이번 구간의 목표와 선행 조건
- 새로 만들거나 수정할 실제 파일 경로
- 명령어가 실제로 하는 일과 바꿔 볼 수 있는 parameter/설정값
- 코드·URDF/SDF/YAML이 구현하는 구조와 실행 뒤 확인할 결과

M08에는 실제 Gazebo AGV 화면, M11에는 실제 RViz AGV·센서 frame 화면을 각 모듈의 `screenshots/`와 PPTX에 포함했습니다.

## 따라 하기 PPT 사용법

제작 기준은 저장소 루트의 `ROS2_Gazebo_AGV_따라하기형_PPT_제작_가이드.docx`이며, 가이드 반영 사항은 [PPT 배포 구조](docs/PPT_FOLLOW_ALONG_DELIVERY.md)에 정리했습니다. 각 M01–M22 폴더에 독립 실행용 PPTX가 있으며, Block별 결과 요약 PPT는 제공하지 않습니다. 각 모듈 폴더는 다음 구조를 공통으로 사용합니다.

```text
MXX_module/
├── MXX_*.pptx                 # 강의·실습용 따라 하기 PPT
├── starter/                   # 시작 상태와 선행 조건
├── complete/                  # PPT에서 만든 핵심 파일 snapshot
├── screenshots/               # 실제 validation terminal / GUI 캡처
├── logs/                      # 실제 검증 명령 출력
└── CHECKSUM_or_TAG.txt        # Complete source SHA-256 manifest
```

| Block | 모듈별 PPT 폴더 |
| --- | --- |
| A — ROS 2 기초 | [M01–M04](blocks/A_ros2_basics/) |
| B — 로봇 제작 | [M05–M08](blocks/B_robot_build/) |
| C — 주행과 시각화 | [M09–M11](blocks/C_drive_visualization/) |
| D — 센서 | [M12–M15](blocks/D_sensors/) |
| E — 제어·인지·미션 | [M16–M20](blocks/E_autonomy_logic/) |
| F — 통합 | [M21–M22](blocks/F_integration/) |

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
- 이름과 토픽은 문서에 적힌 것을 그대로 사용합니다. 임의로 바꾸면 launch와 bridge 설정도 함께 바꿔야 합니다.
- Gazebo Classic (`gazebo`, `gazebo_ros_pkgs`)이 아니라 modern Gazebo의 `gz sim`, `ros_gz`를 사용합니다.
- YOLO는 선택 의존성입니다. M17 전까지는 설치하지 않아도 ROS/Gazebo 기초 실습을 진행할 수 있습니다.
