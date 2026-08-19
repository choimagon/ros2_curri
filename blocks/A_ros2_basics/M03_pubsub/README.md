# M03 — Publisher / Subscriber 직접 작성

## 목표

Timer 기반 publisher, callback 기반 subscriber, `geometry_msgs/msg/Twist` 메시지를 직접 사용합니다.

## 이번 구간에서 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_control/agv_control/counter_publisher.py` | 1초마다 `/counter`에 `Int32`를 publish합니다. |
| `agv_ws/src/agv_control/agv_control/counter_monitor.py` | `/counter`를 받아 로그로 표시합니다. |
| `agv_ws/src/agv_control/agv_control/cmd_test_node.py` | `/cmd_vel`에 안전한 짧은 `Twist` 명령을 publish합니다. |
| `agv_ws/src/agv_control/agv_control/velocity_monitor.py` | `/cmd_vel`의 선속도·각속도를 표시합니다. |
| `agv_ws/src/agv_control/setup.py` | 네 파일의 console script entry point를 등록합니다. |

## 만드는 순서

1. `counter_publisher.py`에서 `create_publisher(Int32, '/counter', 10)`과 `create_timer(1.0, ...)`를 만듭니다.
2. `counter_monitor.py`에서 같은 타입과 토픽의 `create_subscription`을 만듭니다.
3. `cmd_test_node.py`에서 `Twist.linear.x`, `Twist.angular.z`만 설정합니다. 나머지 축은 기본값 0을 유지합니다.
4. `setup.py`의 `entry_points`에 `counter_publisher`, `counter_monitor`, `cmd_test_node`, `velocity_monitor`를 추가합니다.
5. 빌드 후에는 반드시 다시 source합니다.

```bash
cd ~/ros2_curri/agv_ws
colcon build --symlink-install --packages-select agv_control
source install/setup.bash
ros2 run agv_control counter_publisher
```

다른 터미널에서 `source install/setup.bash` 후 `ros2 run agv_control counter_monitor`를 실행합니다. Twist 노드는 아직 Gazebo가 없어도 `cmd_test_node`와 `velocity_monitor`를 함께 실행하여 확인할 수 있습니다.

## 확인

`ros2 topic echo /counter --once`가 정수를 출력하고, `ros2 topic info /cmd_vel -v`에서 publisher/subscriber가 보이면 통과입니다.
