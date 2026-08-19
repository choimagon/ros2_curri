# M01 — ROS 2 기초와 분산 로봇 소프트웨어

## 목표

Node, Topic, Service, Action, Parameter가 한 프로그램의 함수가 아니라 네트워크로 연결된 독립 기능이라는 점을 확인합니다. 이 단계에서는 새 ROS 패키지 파일을 만들지 않고, ROS에 포함된 demo node를 사용합니다.

## 이번 구간의 파일

| 파일 | 이유 |
| --- | --- |
| `README.md` | 이론, 실행 명령, 확인 기준을 기록합니다. |
| `../../../../docs/INSTALL_UBUNTU_24.04_ROS2_JAZZY.md` | ROS 미설치 PC에서 먼저 실행할 설치 안내입니다. |

## 만드는 순서

1. 설치 문서의 **4. 설치 직후 검증**까지 완료합니다.
2. 터미널 1에서 `ros2 run demo_nodes_cpp talker`를 실행합니다.
3. 터미널 2에서 `ros2 run demo_nodes_py listener`를 실행합니다.
4. 터미널 3에서 아래 관찰 명령을 실행합니다.

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 topic list
ros2 topic info /chatter
ros2 topic echo /chatter --once
```

## 확인

`/talker`, `/listener`, `/chatter`가 보이고 listener가 문자열을 출력하면 통과입니다. Topic의 발행자와 구독자를 `ros2 topic info /chatter -v`로 한 번 더 확인하세요.

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `source /opt/ros/jazzy/setup.bash` | 현재 셸의 `PATH`, Python 경로, ament resource 경로에 Jazzy를 추가합니다. 새 터미널마다 한 번 필요합니다. | 여러 로봇을 분리할 때는 실행 전에 `export ROS_DOMAIN_ID=23`처럼 동일한 도메인 번호를 지정합니다. |
| `ros2 run demo_nodes_cpp talker` | 설치된 `demo_nodes_cpp` 패키지에서 `talker` 실행 파일을 찾아 DDS publisher 노드를 시작합니다. | `--ros-args -r __node:=agv_talker`로 노드 이름을 바꿔 그래프 변화를 관찰할 수 있습니다. |
| `ros2 node list` / `ros2 topic list` | DDS discovery로 찾은 노드·토픽 목록을 보여 줍니다. 메시지를 보내는 명령이 아닙니다. | talker/listener를 하나씩 종료해 목록에서 사라지는지 확인합니다. |
| `ros2 topic info /chatter -v` | `/chatter`의 메시지 타입과 publisher/subscriber 수·이름을 보여 줍니다. | `-v`를 빼면 수만 간단히 봅니다. |
| `ros2 topic echo /chatter --once` | subscriber를 임시로 만들고 첫 메시지 한 개를 출력한 뒤 종료합니다. | `--once`를 빼면 Ctrl-C까지 계속 출력됩니다. |

## 내부 구현과 실행 뒤 보이는 결과

talker는 `std_msgs/msg/String` 메시지를 `/chatter`에 주기적으로 publish하고, listener는 **같은 토픽 이름·같은 메시지 타입**으로 subscription을 만들어 callback에서 문자열을 출력합니다. 두 프로그램이 서로 함수를 호출하지 않아도 DDS가 둘을 연결하는 것이 이 실습의 핵심입니다.

정상이라면 talker 쪽에는 `Publishing: 'Hello World: N'`, listener 쪽에는 `I heard: [Hello World: N]`처럼 같은 번호가 순서대로 나타납니다. `ros2 topic echo --once`에도 `data: Hello World: N`이 한 번 출력됩니다. 서로 다른 `ROS_DOMAIN_ID`를 쓰면 같은 PC에서도 이 결과가 보이지 않으므로, 그때는 코드보다 도메인 설정을 먼저 확인합니다.
