# M04 — TF2와 로봇 좌표계

## 목표

`map → odom → base_link → sensor`가 각 데이터의 기준 좌표라는 점을 이해하고, URDF에서 만든 link/joint로 TF tree를 만듭니다.

## 이번 구간에서 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_description/urdf/agv.urdf.xacro` | `base_link`, 바퀴, camera/lidar/imu frame과 joint를 정의합니다. |
| `agv_ws/src/agv_description/launch/display.launch.py` | xacro를 `robot_description`으로 변환하고 `robot_state_publisher`를 시작합니다. |
| `agv_ws/src/agv_description/rviz/agv.rviz` | RViz의 Fixed Frame과 RobotModel 표시 설정입니다. |

## 만드는 순서

1. URDF의 link는 **좌표계**, joint는 부모와 자식 좌표계의 연결이라고 생각합니다.
2. 고정 센서는 `fixed joint`, 구동 바퀴는 `continuous joint`로 `base_link`에 연결합니다.
3. camera의 실제 영상 축은 `camera_optical_frame`으로 별도 fixed joint를 둡니다.
4. `display.launch.py`에서 xacro 명령 결과를 `robot_state_publisher` 파라미터 `robot_description`으로 넘깁니다.

```bash
cd ~/ros2_curri/agv_ws
colcon build --symlink-install --packages-select agv_description
source install/setup.bash
ros2 launch agv_description display.launch.py
```

다른 터미널에서 `ros2 run tf2_tools view_frames`를 실행하면 `frames.pdf`가 생성됩니다.

## 확인

RViz Fixed Frame을 `base_link`로 설정했을 때 RobotModel이 보이고, `base_link` 아래에 `left_wheel_link`, `right_wheel_link`, `camera_link`, `lidar_link`, `imu_link`가 연결되어야 합니다.

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 launch agv_description display.launch.py` | launch 파일이 xacro를 URDF 문자열로 확장해 `robot_state_publisher`에 넘기고, `joint_state_publisher_gui`, RViz2를 함께 시작합니다. | RViz가 필요 없으면 launch 파일에서 RViz Node만 잠시 주석 처리해 TF만 관찰할 수 있습니다. |
| `ros2 run tf2_tools view_frames` | 일정 시간 `/tf`, `/tf_static`을 수집해 좌표계 연결을 `frames.pdf`로 그립니다. 로봇을 움직이는 명령은 아닙니다. | `base_link`가 아니라 `odom`을 Fixed Frame으로 쓰려면 Gazebo/odometry TF도 필요합니다. |
| RViz Fixed Frame | 모든 표시를 비교하는 기준 좌표계를 정합니다. 존재하지 않는 frame을 고르면 화면이 비거나 경고가 납니다. | 정적 모델은 `base_link`, 주행 중 모델은 `odom`을 선택합니다. |

## 내부 구현과 실행 뒤 보이는 결과

`agv.urdf.xacro`의 각 `link`는 좌표계 이름이 되고, 각 `joint`의 parent/child와 origin은 두 좌표계 사이의 변환이 됩니다. `robot_state_publisher`는 fixed joint는 `/tf_static`으로 한 번, 바퀴처럼 움직일 수 있는 joint는 `joint_state_publisher_gui`가 보낸 값에 따라 `/tf`로 계산합니다. `camera_optical_frame`은 카메라 영상에서 쓰는 축 방향을 맞추기 위해 `camera_link` 아래에 한 단계 더 둔 frame입니다.

정상 결과는 `base_footprint → base_link` 아래에 두 바퀴·caster·LiDAR·camera·IMU가 이어진 트리입니다. GUI에서 바퀴 joint 슬라이더를 움직이면 RViz의 바퀴만 회전하고 본체·센서 frame은 고정되어 보입니다. 이 차이가 fixed joint와 continuous joint 구현의 결과입니다.
