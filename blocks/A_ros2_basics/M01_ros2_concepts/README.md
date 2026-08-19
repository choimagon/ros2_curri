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
