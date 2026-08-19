# M11 — RViz2 통합 검증

## 목표와 파일

`agv_description/rviz/agv.rviz`는 RobotModel/TF의 출발점이고, `agv_bringup/launch/agv_sim.launch.py`는 최종적으로 RViz를 같이 실행합니다.

## 만드는 순서

1. Gazebo launch를 실행합니다.
2. 별도 터미널에서 `rviz2`를 실행하고 Fixed Frame을 먼저 `odom`으로 정합니다.
3. Add 메뉴로 RobotModel, TF, Odometry(`/odom`), LaserScan(`/scan`), Image를 추가합니다.
4. RobotModel이 TF와 맞지 않으면 M04의 `robot_state_publisher`도 실행해야 합니다.

```bash
ros2 run tf2_tools view_frames
ros2 topic hz /scan
ros2 topic echo /odom --once
```

## 확인

RViz에서 RobotModel, TF, Odometry, LaserScan 네 개가 같은 위치를 가리키는지 봅니다. 데이터는 오는데 화면이 비면 `Fixed Frame`, 메시지 `frame_id`, TF tree 순으로 검사합니다.
