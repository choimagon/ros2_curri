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
