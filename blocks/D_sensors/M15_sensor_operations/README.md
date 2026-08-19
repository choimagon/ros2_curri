# M15 — 센서 운영과 동기화

## 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_bringup/config/sensors.yaml` | update rate, QoS/임계값, `use_sim_time`을 launch 밖으로 분리합니다. |
| `agv_ws/src/agv_sensors/agv_sensors/lidar_processor.py` | SensorDataQoS를 사용합니다. |
| `agv_ws/src/agv_sensors/agv_sensors/imu_monitor.py` | `use_sim_time` 적용 여부를 확인합니다. |

## 만드는 순서

시뮬레이션 노드는 `use_sim_time: true`를 받아 `/clock`을 사용합니다. Camera/LiDAR/IMU는 SensorDataQoS(대체로 best effort)가 맞으며, subscriber QoS가 incompatible이면 메시지가 아예 안 올 수 있습니다.

```bash
ros2 param get /lidar_processor use_sim_time
ros2 topic hz /scan
ros2 topic hz /imu/data
ros2 topic info /scan -v
```

## 확인

Gazebo를 pause하면 ROS node 시간도 멈추고, `topic hz`가 SDF update rate 근처를 보이며 각 메시지 `header.frame_id`가 TF에 존재하면 통과입니다.

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 param get /lidar_processor use_sim_time` | 실행 중인 node의 parameter 값을 service로 질의합니다. 값이 `true`이면 ROS wall clock 대신 bridge의 `/clock`을 사용합니다. | launch YAML에서 processor와 imu_monitor에만 이 값을 설정했으므로, 새 노드를 추가할 때도 같은 YAML 구조를 넣습니다. |
| `ros2 topic hz /scan` / `... /imu/data` | subscriber가 받은 메시지 간격을 바탕으로 평균 Hz를 계산합니다. | LiDAR는 10 Hz, IMU는 100 Hz 근처인지 비교합니다. |
| `ros2 topic info /scan -v` | topic type, publisher/subscriber 수와 QoS profile을 상세 출력합니다. | QoS incompatibility가 의심되면 reliability와 durability를 publisher·subscriber 양쪽에서 비교합니다. |

## 내부 구현과 실행 뒤 보이는 결과

`sensors.yaml`은 코드 밖에서 `use_sim_time: true`와 LiDAR 전방 각도 `front_half_angle_deg: 15.0`을 node 이름별로 전달합니다. LiDAR와 IMU subscriber는 `qos_profile_sensor_data`를 사용합니다. 이 profile은 일반적으로 best effort라서 센서처럼 최신 샘플이 중요한 데이터에 맞고, 신뢰성(reliable)을 강제한 subscription과는 연결되지 않을 수 있습니다.

Gazebo를 pause하면 `/clock`도 멈추므로 sim time을 쓰는 node의 ROS 시간도 멈춥니다. 반대로 `use_sim_time`이 false이면 simulation이 pause여도 wall clock 기준 timer/log는 계속 흐릅니다. `frame_id`가 없거나 TF tree에 없으면 RViz가 scan·IMU 방향을 변환할 수 없으므로, rate가 정상이어도 시각화는 실패할 수 있습니다.
