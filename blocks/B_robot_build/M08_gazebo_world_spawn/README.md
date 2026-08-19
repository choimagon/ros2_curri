# M08 — Gazebo World와 AGV Spawn

## 목표

SDF World에 바닥·벽·장애물·목표물을 두고 AGV 모델을 Gazebo Harmonic에서 실행합니다.

## 이번 구간에서 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_gazebo/worlds/warehouse.sdf` | 조명, 물리, 바닥, 벽, 장애물이 있는 World입니다. |
| `agv_ws/src/agv_gazebo/models/agv/model.config` | Gazebo model URI가 읽는 모델 메타데이터입니다. |
| `agv_ws/src/agv_gazebo/models/agv/model.sdf` | AGV 물리·센서·DiffDrive plugin 모델입니다. |
| `agv_ws/src/agv_gazebo/launch/gazebo.launch.py` | World와 resource path를 ROS launch에서 시작합니다. |

## 만드는 순서

1. World에 `Physics`, `UserCommands`, `SceneBroadcaster`, `Sensors` system plugin을 넣습니다.
2. model 폴더를 패키지 share로 설치하고 launch에서 `GZ_SIM_RESOURCE_PATH`에 models 경로를 추가합니다.
3. World의 `<include><uri>model://agv</uri></include>`가 `models/agv/model.config`를 찾습니다.
4. Gazebo 창이 열리면 Inspector에서 `agv` model과 wheel joint를 확인합니다.

```bash
cd ~/ros2_curri/agv_ws
colcon build --symlink-install --packages-select agv_gazebo agv_description
source install/setup.bash
ros2 launch agv_gazebo gazebo.launch.py
```

## 확인

Gazebo에서 floor, 벽, 빨간 target, AGV가 모두 보이고 실행 직후 AGV가 안정적으로 바닥에 놓이면 통과입니다.
