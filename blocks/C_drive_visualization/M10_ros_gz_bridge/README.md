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

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 launch agv_gazebo gazebo.launch.py` | Gazebo와 함께 `ros_gz_bridge parameter_bridge`를 실행하고 `bridge.yaml`의 모든 항목을 bridge 규칙으로 등록합니다. | 새 토픽을 추가할 때 실행 명령을 바꾸는 것이 아니라 YAML에 한 항목을 추가한 뒤 launch를 다시 시작합니다. |
| `ros2 topic list \| sort` | ROS DDS 쪽에서 bridge된 토픽을 이름순으로 보여 줍니다. `sort`는 보기 좋게 정렬할 뿐 토픽 동작을 바꾸지 않습니다. | Gazebo가 시작된 뒤 실행해 `/clock`, `/scan` 등이 ROS로 넘어왔는지 확인합니다. |
| `ros2 topic echo /scan --once` | LaserScan 한 개를 받은 뒤 종료합니다. 센서 데이터가 실제로 흐르는지 확인하는 최소 검사입니다. | 계속 흐름을 보려면 `--once`를 빼고, 주기는 `ros2 topic hz /scan`으로 봅니다. |
| `gz topic -l` | Gazebo Transport 쪽 원본 이름을 나열합니다. | ROS 출력이 비면 이 이름을 YAML의 `gz_topic_name`과 먼저 맞춥니다. |

## 내부 구현과 실행 뒤 보이는 결과

`bridge.yaml`의 한 항목은 ROS 이름, Gazebo 이름, 양쪽 메시지 타입, 방향을 묶은 변환 계약입니다. `/cmd_vel`은 ROS 명령을 Gazebo plugin으로 넘겨야 하므로 `ROS_TO_GZ`이고, `/odom`, `/scan`, `/imu/data`, `/camera/image_raw`, `/clock`은 Gazebo가 생성하므로 `GZ_TO_ROS`입니다. 예를 들어 `sensor_msgs/msg/LaserScan`과 `gz.msgs.LaserScan`이 정확히 짝지어지지 않으면 같은 이름이어도 변환할 수 없습니다.

정상 결과에서는 ROS 쪽 `ros2 topic list`에 여섯 토픽이 나타나고 `/scan`에는 `angle_min`, `ranges`, `header.frame_id`가, `/odom`에는 위치·자세·속도가 출력됩니다. `/cmd_vel`만 보이고 센서 메시지가 없으면 방향을 반대로 준 것이 아니라 Gazebo 센서 topic 또는 메시지 타입을 확인해야 합니다.
