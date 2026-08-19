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

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `colcon build --symlink-install --packages-select agv_control` | `setup.py`의 entry point를 다시 설치합니다. 노드 파일이나 entry point를 바꾼 뒤 실행 가능한 이름을 갱신하는 단계입니다. | 여러 패키지를 함께 수정했다면 패키지 이름을 공백으로 더 적습니다. |
| `ros2 run agv_control counter_publisher` | `setup.py`의 `counter_publisher = agv_control.counter_publisher:main`을 찾아 publisher 노드를 실행합니다. | 코드의 timer 주기(현재 1.0초)와 queue depth(현재 10)를 바꿔 발행 빈도와 버퍼를 비교합니다. |
| `ros2 run agv_control counter_monitor` | `/counter`를 구독하는 별도 프로세스를 실행합니다. publisher보다 나중에 시작해도 다음 메시지부터 수신합니다. | 같은 토픽의 monitor를 두 개 실행해 subscriber 수가 2가 되는지 봅니다. |
| `ros2 run agv_control cmd_test_node --ros-args -p linear_speed:=0.10 -p angular_speed:=0.30` | `/cmd_vel`에 전진·회전 속도를 담은 `Twist`를 냅니다. `-p` 뒤 값은 코드의 ROS parameter를 실행 시점에 덮어씁니다. | 초기에는 `linear_speed`를 0.15 이하, `angular_speed`를 ±0.4 이하로 둡니다. |

## 내부 구현과 실행 뒤 보이는 결과

`counter_publisher.py`는 `Int32` publisher와 `create_timer(1.0, ...)`를 만들고 0, 1, 2…를 `/counter`로 보냅니다. `counter_monitor.py`는 같은 타입·토픽의 subscription callback에서 받은 숫자를 로그로 찍습니다. 두 노드의 마지막 인수 `10`은 저장해 둘 메시지 queue depth입니다.

`cmd_test_node.py`는 0.1초 timer에서 총 30회 명령을 보내므로 설정한 속도는 정확히 약 3초 동안만 유지됩니다. 그 뒤에는 모든 값이 0인 `Twist`가 계속 publish되어, 수동 종료를 잊어도 AGV가 계속 가속하지 않게 했습니다. `velocity_monitor`를 같이 띄우면 `cmd_vel linear.x=0.100 angular.z=0.300`과 마지막 `0.000`을 직접 확인할 수 있습니다.
