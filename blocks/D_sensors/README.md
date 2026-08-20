# Block D — 센서 (M12–M15)

종료 조건은 Camera·2D LiDAR·IMU가 Gazebo에서 생성되어 ROS topic으로 들어오고, update rate·frame_id·`use_sim_time`을 설명할 수 있는 것입니다.

## Block 커리큘럼 요약

| 순서 | 입력 | 처리·확인 포인트 |
| --- | --- | --- |
| M12 | `/camera/image_raw` | Gazebo 장착, rqt/RViz Image, hz |
| M13 | `/scan` | LaserScan·전방 최소거리·안전 sector |
| M14 | `/imu/data` | IMU 축·gyro·acceleration |
| M15 | `/clock`과 세 sensor | QoS·frame_id·`use_sim_time`·rate |

센서별 정상·오류 화면과 Complete source를 확인한 다음 M16으로 진행합니다. [M 시리즈 통합 PPT](Block_D_M시리즈_통합_따라하기.pptx)는 M12 → M15를 한 파일로 묶은 강의용 자료입니다.
