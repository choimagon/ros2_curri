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
