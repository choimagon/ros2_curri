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
