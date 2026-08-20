# Block C — 주행과 시각화 (M09–M11)

이 Block에서는 Gazebo의 AGV를 `/cmd_vel`로 움직이고, 같은 상태를 ROS 2 topic과 RViz에서 확인합니다. ROS 명령은 먼저 `source ~/ros2_curri/agv_ws/install/setup.bash`를 실행한 터미널에서 사용하세요.

## Block 커리큘럼 요약

| 순서 | 핵심 연결 | 눈으로 확인할 결과 |
| --- | --- | --- |
| M09 | `/cmd_vel` → DiffDrive → `/odom` | 직진·회전·곡선과 odometry |
| M10 | ROS 2 ↔ Gazebo message bridge | topic 이름·타입·방향 |
| M11 | RobotModel·TF·Odom·LaserScan·Path | 같은 `odom` 기준의 RViz |

[M 시리즈 통합 PPT](Block_C_M시리즈_통합_따라하기.pptx)는 구동 전후와 RViz 검증을 한 파일에서 복습할 수 있게 합친 자료입니다.
