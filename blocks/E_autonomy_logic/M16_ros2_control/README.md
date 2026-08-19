# M16 — ros2_control + gz_ros2_control 확장

## 만드는 파일

`agv_ws/src/agv_control/config/controllers.yaml`에 `joint_state_broadcaster`와 `diff_drive_controller` 설정을 둡니다. 이 저장소의 M09는 Gazebo DiffDrive로 먼저 주행하고, M16은 실제 하드웨어로 옮기기 쉬운 controller_manager 구조를 학습하는 확장 단계입니다.

## 만드는 순서와 확인

`wheel_separation`, `wheel_radius`, joint 이름을 URDF/SDF와 일치시킵니다. 다음 명령으로 설치와 controller 목록을 확인합니다.

```bash
ros2 pkg prefix gz_ros2_control
ros2 control list_controllers
```

M16을 실제로 활성화하려면 model SDF에 `gz_ros2_control` plugin과 `<ros2_control>` hardware tag를 추가해야 합니다. 이때 M09의 Gazebo DiffDrive plugin과 동시에 같은 바퀴를 제어하지 않습니다.

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 pkg prefix gz_ros2_control` | `gz_ros2_control` 확장 패키지가 설치되어 있는지와 선택된 경로를 확인합니다. controller를 시작하지는 않습니다. | 경로가 비어 있으면 설치가 필요하며, 현재 M09 DiffDrive 실습은 이 패키지 없이도 동작합니다. |
| `ros2 control list_controllers` | 실행 중인 `controller_manager`에게 controller 목록을 요청합니다. | gz_ros2_control를 아직 SDF에 연결하지 않은 현재 프로젝트에서는 목록이 없거나 service 대기 오류가 정상입니다. |

## 내부 구현과 실행 뒤 보이는 결과

현재 `controllers.yaml`에는 `joint_state_broadcaster`와 `diff_drive_controller`의 **실제 설정 초안**이 있습니다. 좌·우 joint 이름은 `left_wheel_joint`, `right_wheel_joint`, wheel separation은 0.38 m, radius는 0.08 m, publish rate는 50 Hz입니다. 이 값은 URDF와 Gazebo DiffDrive plugin의 기하값과 일치해야 합니다.

다만 현재 실행 모델은 M09의 `gz::sim::systems::DiffDrive`로 바퀴를 제어합니다. `gz_ros2_control` plugin과 `<ros2_control>` hardware interface는 의도적으로 아직 추가하지 않았으므로, 이 문서의 controller list만으로 “활성화 완료”라고 판단하면 안 됩니다. 실제 확장 시에는 DiffDrive plugin을 제거한 뒤 하나의 controller만 같은 joint를 소유하게 해야 이중 명령·진동이 생기지 않습니다.
