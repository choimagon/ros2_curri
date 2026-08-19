# M10 — ROS–Gazebo Bridge

## 목표와 파일

Gazebo Transport와 ROS 2 DDS를 `ros_gz_bridge`로 연결합니다.

| 파일 | 연결 |
| --- | --- |
| `agv_ws/src/agv_gazebo/config/bridge.yaml` | `/cmd_vel`, `/odom`, `/scan`, `/imu/data`, `/clock`의 타입과 방향 |
| `agv_ws/src/agv_gazebo/launch/gazebo.launch.py` | Gazebo와 parameter_bridge를 한 launch에서 실행 |

## 만드는 순서

각 YAML 항목은 `ros_topic_name`, `gz_topic_name`, ROS/Gazebo 메시지 타입, `direction`이 한 세트입니다. 명령은 ROS에서 Gazebo로(`ROS_TO_GZ`), 센서·odom·clock은 Gazebo에서 ROS로(`GZ_TO_ROS`) 둡니다.

```bash
ros2 launch agv_gazebo gazebo.launch.py
ros2 topic list | sort
ros2 topic echo /odom --once
ros2 topic echo /scan --once
```

토픽이 안 보이면 `gz topic -l | sort`로 **Gazebo 쪽 실제 이름**부터 확인한 뒤 bridge YAML만 수정합니다. ROS topic 이름을 추측해서 바꾸지 마세요.

## 확인

`/clock`, `/cmd_vel`, `/odom`, `/scan`, `/imu/data`가 ROS 목록에 보이고 `/odom`과 `/scan`이 한 메시지 이상 나오면 통과입니다.
