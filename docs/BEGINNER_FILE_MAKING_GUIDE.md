# 처음 만드는 ROS 2 파일 가이드

이 문서는 각 Block의 README와 PPT를 보기 전에 읽는 “파일 지도”입니다. ROS 2 프로젝트는 한 파일을 실행하는 방식이 아니라, **패키지 선언 → 코드/모델 → 빌드 설정 → build → source → 실행** 순서로 동작합니다.

## 1. Python 노드 (`.py`) 만들기

실제 예제: `agv_ws/src/agv_control/agv_control/counter_publisher.py`

1. `agv_control/agv_control/` 안에 Python 파일을 만듭니다.
2. `Node`를 상속하고 publisher/subscriber/timer를 만듭니다.
3. `setup.py`의 `console_scripts`에 `실행이름 = 패키지.파일:main`을 등록합니다.
4. workspace 최상위에서 build한 뒤 source하고 `ros2 run`으로 실행합니다.

```python
# counter_publisher.py의 핵심 구조
self.publisher = self.create_publisher(Int32, '/counter', 10)
self.create_timer(1.0, self.publish_counter)
```

`/counter`는 다른 노드와 약속한 topic 이름, `Int32`는 메시지 타입, `10`은 subscriber가 잠시 늦어도 보관할 queue depth입니다. timer의 `1.0`은 1초마다 callback을 호출한다는 뜻입니다.

```bash
cd ~/ros2_curri/agv_ws
colcon build --symlink-install --packages-select agv_control
source install/setup.bash
ros2 run agv_control counter_publisher
```

## 2. C++ 노드 (`.cpp`) 만들기

실제 예제: `agv_ws/src/agv_cpp_examples/src/status_publisher.cpp`

1. `ros2 pkg create --build-type ament_cmake 패키지이름 --dependencies rclcpp std_msgs`로 뼈대를 만듭니다.
2. `src/파일이름.cpp`에 `rclcpp::Node`를 상속한 클래스를 작성합니다.
3. `CMakeLists.txt`에 `add_executable`, `ament_target_dependencies`, `install`을 모두 적습니다.
4. `package.xml`의 `<depend>`도 CMake 의존성과 맞춥니다.

```cpp
publisher_ = this->create_publisher<std_msgs::msg::String>("/cpp_status", 10);
timer_ = this->create_wall_timer(1s, std::bind(&StatusPublisher::publish_status, this));
```

Python의 `create_publisher`·`create_timer`와 같은 역할이지만, C++은 타입을 컴파일할 때 검사합니다. `CMakeLists.txt`의 `install(TARGETS ... DESTINATION lib/${PROJECT_NAME})`이 빠지면 컴파일에 성공해도 `ros2 run`은 실행 파일을 찾지 못합니다.

```bash
cd ~/ros2_curri/agv_ws
colcon build --packages-select agv_cpp_examples
source install/setup.bash
ros2 run agv_cpp_examples status_publisher --ros-args -p message:='C++ 노드 시작'
```

다른 터미널에서 `ros2 topic echo /cpp_status`를 실행하면 `data: C++ 노드 시작 #0`처럼 보입니다.

## 3. URDF/Xacro 로봇 파일 (`.urdf.xacro`) 만들기

실제 예제: `agv_ws/src/agv_description/urdf/agv.urdf.xacro`

- **URDF**는 RViz와 TF가 읽는 로봇 조립 설명입니다.
- **link**는 몸체·바퀴·센서와 그 좌표계입니다.
- **joint**는 parent link와 child link의 연결·위치·회전 방식입니다.
- **xacro**는 반복되는 바퀴·센서 코드를 macro와 property로 줄이는 URDF 전처리기입니다.

```xml
<xacro:property name="wheel_radius" value="0.08"/>
<xacro:agv_wheel side="left" y="${wheel_base/2}"
                 radius="${wheel_radius}" width="${wheel_width}"/>
```

먼저 `wheel_radius` 같은 한 곳의 값을 정하고 macro에 전달합니다. 바퀴의 모양과 joint 높이가 같은 값을 쓰므로 크기만 바뀌고 바닥에 묻히는 실수를 줄일 수 있습니다.

```bash
xacro src/agv_description/urdf/agv.urdf.xacro > /tmp/agv.urdf
check_urdf /tmp/agv.urdf
ros2 launch agv_description display.launch.py
```

`xacro`는 사람이 쓰기 편한 파일을 순수 URDF로 변환하고, `check_urdf`는 link/joint tree를 검사하며, 마지막 launch는 RViz에서 결과를 보여 줍니다.

## 4. Gazebo SDF 파일 (`.sdf`) 만들기

실제 예제: `agv_ws/src/agv_gazebo/models/agv/model.sdf`

- **SDF**는 Gazebo가 실제 물리와 sensor를 계산할 모델입니다.
- `visual`은 보이는 모양, `collision`은 접촉 판정, `inertial`은 질량·관성입니다.
- `sensor`는 camera/LiDAR/IMU 데이터를 만들고, `plugin`은 DiffDrive 같은 동작을 추가합니다.

```xml
<sensor name="lidar" type="gpu_lidar">
  <topic>/scan</topic><update_rate>10</update_rate>
  <lidar><scan><horizontal><samples>720</samples></horizontal></scan></lidar>
</sensor>
```

위 설정은 Gazebo에서 10 Hz, 720개 방향의 LiDAR scan을 만든다는 뜻입니다. sensor topic을 만든 뒤에는 `bridge.yaml`에 ROS 타입과 변환 방향을 적어야 ROS 노드가 받을 수 있습니다.

```bash
gz sdf -k src/agv_gazebo/models/agv/model.sdf
ros2 launch agv_gazebo gazebo.launch.py
```

첫 명령은 SDF 문법 검사, 둘째 명령은 World·모델·bridge를 실제로 실행합니다.

## 5. YAML 설정과 launch 파일 만들기

실제 예제: `agv_ws/src/agv_bringup/config/*.yaml`, `agv_ws/src/agv_bringup/launch/agv_sim.launch.py`

YAML에는 실험 중 자주 바꾸는 숫자·경로·기능 on/off를 두고, Python 코드에는 계산 로직만 둡니다.

```yaml
mission_manager:
  ros__parameters:
    stop_distance: 0.50
    search_speed: 0.25
```

launch 파일은 여러 Node와 Gazebo launch를 한 명령으로 조립합니다. `rviz` 같은 launch argument를 만들면 `ros2 launch agv_bringup agv_sim.launch.py rviz:=false`로 GUI만 끄고 문제를 빠르게 분리할 수 있습니다.

## 공통 확인 순서

1. 파일을 수정한 패키지를 build합니다.
2. 새 터미널마다 `source /opt/ros/jazzy/setup.bash`와 `source install/setup.bash`를 실행합니다.
3. `ros2 pkg prefix 패키지`, `ros2 node list`, `ros2 topic info -v 토픽` 순서로 파일·실행·통신을 따로 확인합니다.
4. 모델은 `check_urdf`/`gz sdf -k`, 화면은 RViz/Gazebo, 센서는 `echo`/`hz`로 확인합니다.
