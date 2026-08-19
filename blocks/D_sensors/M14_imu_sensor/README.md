# M14 — IMU Sensor

## 만드는 파일

`agv_ws/src/agv_gazebo/models/agv/model.sdf`에 IMU sensor와 noise를, `agv_ws/src/agv_sensors/agv_sensors/imu_monitor.py`에 값 표시 node를 둡니다.

## 만드는 순서와 확인

IMU는 `angular_velocity`, `linear_acceleration`, orientation을 갖습니다. `imu_link`의 축과 `base_link` 축이 같아야 해석이 쉽습니다. 처음에는 작은 Gaussian noise만 두고, 이후 stddev를 키워 알고리즘의 흔들림을 비교합니다.

```bash
ros2 run agv_sensors imu_monitor
ros2 topic echo /imu/data --once
```

정지 상태에서도 gravity 축 가속도는 보일 수 있습니다. 이것은 고장이 아니라 IMU가 중력을 측정하기 때문입니다.

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 run agv_sensors imu_monitor` | `/imu/data`를 SensorDataQoS로 구독하고, gyro z·acceleration z·frame을 1초 간격으로 로그에 표시합니다. | log 값 자체는 parameter가 아니며, noise와 rate는 SDF sensor에서 조절합니다. |
| `ros2 topic echo /imu/data --once` | Imu 한 메시지의 orientation, angular_velocity, linear_acceleration, covariance를 출력한 뒤 종료합니다. | `header.frame_id`가 `imu_link`처럼 TF tree에 있는 frame인지 확인합니다. |
| `ros2 topic hz /imu/data` | IMU 메시지의 실제 입력 rate를 계산합니다. | 현재 모델은 100 Hz입니다. 처리 노드가 많아져 rate가 떨어지면 GUI보다 이 수치로 먼저 확인합니다. |

## 내부 구현과 실행 뒤 보이는 결과

현재 SDF는 `base_link` 아래 IMU sensor를 항상 켜고 100 Hz로 `/imu/data`를 생성합니다. 설정된 예제 noise는 angular velocity의 x축에 Gaussian `stddev=0.001`이며, 다른 축 noise·orientation noise를 추가하면 알고리즘의 견고성을 더 시험할 수 있습니다. `imu_monitor.py`는 매 메시지를 전부 출력하지 않고 `throttle_duration_sec=1.0`으로 로그 양을 제한합니다.

정지해도 `acceleration z`에 중력에 해당하는 값이 남는 것은 정상이며, frame 이름은 `imu_link`여야 합니다. 로봇을 회전하면 `gyro z` 부호와 크기가 변하고, 축을 뒤집어 장착했다면 이 부호가 기대와 반대가 됩니다. 그때는 필터 코드를 보정하기 전에 URDF/SDF의 IMU pose와 TF 축을 확인합니다.
