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
