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
| `blocks/` | A–F 교육 구간별 README, 명령어 해설·설정값·구현 결과, 실제 실행 캡처, 발표 자료 |
| `agv_ws/` | 빌드하여 실행하는 AGV ROS 2 패키지 소스 |
| `scripts/` | 설치·커리큘럼 상태를 확인하는 점검 스크립트 |
| `tools/` | Block별 실행 캡처와 PPTX를 다시 생성하는 도구 |

각 모듈 README에는 다음 네 가지를 반드시 적었습니다.

- 이번 구간의 목표와 선행 조건
- 새로 만들거나 수정할 실제 파일 경로
- 명령어가 실제로 하는 일과 바꿔 볼 수 있는 parameter/설정값
- 코드·URDF/SDF/YAML이 구현하는 구조와 실행 뒤 확인할 결과

Block B와 C에는 실제 실행한 Gazebo AGV 화면과 RViz AGV·센서 frame 화면도 각 폴더의 `captures/`와 PPTX에 포함했습니다.

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
