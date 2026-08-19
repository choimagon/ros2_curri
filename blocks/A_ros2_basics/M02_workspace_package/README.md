# M02 — Workspace와 ament_python 패키지

## 목표

`agv_ws`가 ROS 기본 설치와 분리된 오버레이 workspace라는 것을 이해하고, 패키지의 `package.xml`, `setup.py`, Python 모듈, `resource/` 파일 역할을 익힙니다.

## 이번 구간에서 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_control/package.xml` | 패키지 이름과 ROS 의존성을 선언합니다. |
| `agv_ws/src/agv_control/setup.py` | Python 모듈과 실행 명령(entry point)을 등록합니다. |
| `agv_ws/src/agv_control/setup.cfg` | ROS 2가 Python 실행 파일을 찾는 설치 경로입니다. |
| `agv_ws/src/agv_control/resource/agv_control` | ament resource index용 빈 표식 파일입니다. |
| `agv_ws/src/agv_control/agv_control/__init__.py` | Python 패키지 표식입니다. |

## 만드는 순서

현재 저장소에는 위 파일의 완성 뼈대가 있습니다. 새 패키지를 직접 만들고 싶다면 다음으로 시작한 뒤, 기존 파일과 비교합니다.

```bash
source /opt/ros/jazzy/setup.bash
mkdir -p ~/ros2_curri/agv_ws/src
cd ~/ros2_curri/agv_ws/src
ros2 pkg create --build-type ament_python agv_control --dependencies rclpy std_msgs geometry_msgs sensor_msgs
```

그 다음 이 저장소의 `agv_control` 파일로 교체하거나 필요한 노드만 추가합니다. workspace 최상위에서 빌드합니다.

```bash
cd ~/ros2_curri/agv_ws
colcon build --symlink-install --packages-select agv_control
source install/setup.bash
ros2 pkg prefix agv_control
```

## 확인

마지막 명령이 `.../agv_ws/install/agv_control`을 출력하면 overlay package가 정상입니다. `src` 안에서 빌드하지 않는 점이 핵심입니다.

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 pkg create --build-type ament_python ...` | `package.xml`, `setup.py`, `setup.cfg`, `resource/`, Python package 폴더를 한 번에 만드는 뼈대 생성기입니다. `--dependencies`에 적은 이름은 `package.xml` 의존성으로 추가됩니다. | 새 실습 패키지는 `agv_control` 대신 소문자·밑줄 이름을 쓰고, 필요한 메시지 패키지만 `--dependencies`에 넣습니다. |
| `colcon build --packages-select agv_control` | workspace 최상위에서 선택한 패키지와 필요한 선행 패키지를 빌드해 `build/`, `install/`, `log/`에 결과를 만듭니다. | 전체 패키지를 확인할 때만 `--packages-select`를 뺍니다. Python 파일을 바로 반영하며 실습하려면 `--symlink-install`을 유지합니다. |
| `source install/setup.bash` | ROS 기본 설치 위에 방금 만든 `install/` overlay를 올립니다. 이 명령 전에는 `ros2 run`이 새 패키지를 찾지 못합니다. | 소스 파일만 읽을 때는 필요 없지만, 빌드 결과를 실행할 때는 새 셸마다 필요합니다. |
| `ros2 pkg prefix agv_control` | 실행 파일을 돌리지 않고, ROS가 실제로 선택한 패키지 설치 경로를 출력합니다. | 경로가 `/opt/ros/...`이면 로컬 overlay가 아닌 다른 패키지를 보고 있는 것이므로 다시 build/source합니다. |

## 내부 구현과 실행 뒤 보이는 결과

`package.xml`은 ROS 의존성과 패키지 이름을 선언하고, `setup.py`의 `console_scripts`는 `ros2 run agv_control counter_publisher` 같은 명령을 Python의 `모듈:main` 함수로 연결합니다. `resource/agv_control`과 `setup.cfg`는 ament가 설치된 Python 패키지를 검색할 수 있게 하는 표식과 설치 경로입니다. 따라서 Python 파일만 있어도 `setup.py`에 entry point가 없으면 `ros2 run`으로 실행할 수 없습니다.

정상 빌드 뒤에는 `install/agv_control/lib/agv_control/`에 console script가 생기고, `ros2 pkg prefix agv_control`은 `.../agv_ws/install/agv_control`을 출력합니다. `src/` 안에서 build하면 이 overlay 구조가 만들어지지 않아 패키지 탐색과 재빌드가 꼬일 수 있습니다.
