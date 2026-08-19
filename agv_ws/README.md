# AGV ROS 2 workspace

이 폴더가 실제 빌드 대상입니다. ROS 2 Jazzy 설치 후 다음을 실행합니다.

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_curri/agv_ws
rosdep install --from-paths src --ignore-src -r -y --skip-keys ament_python
colcon build --symlink-install
source install/setup.bash
```

`src/`의 패키지는 워드 문서의 최종 디렉터리 구조를 따라가되, 수업 초반에도 빌드할 수 있도록 Python 중심으로 구성했습니다. `agv_cpp_examples`는 최종 AGV에 필수인 패키지가 아니라 Python과 비교하며 C++ ROS 2 파일 구성을 배우는 실행 가능한 교육용 예제입니다. 각 패키지를 바꾼 뒤에는 전체 빌드보다 먼저 해당 패키지만 `--packages-select`로 빌드해 첫 오류를 좁히세요.

`ament_python`은 ROS 패키지의 build type 이름이며, 이 Ubuntu/rosdep 조합에는 별도 apt rosdep key가 없습니다. ROS 2 Jazzy의 `ros-dev-tools`가 이미 제공하므로 위 명령에서만 `--skip-keys ament_python`을 사용합니다.
