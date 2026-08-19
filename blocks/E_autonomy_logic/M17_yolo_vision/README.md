# M17 — Camera + YOLO Vision Node

## 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_interfaces/msg/Detection.msg` | class, confidence, bounding box, 거리 추정값 한 개입니다. |
| `agv_ws/src/agv_interfaces/msg/DetectionArray.msg` | 한 프레임의 detection 배열입니다. |
| `agv_ws/src/agv_vision/agv_vision/yolo_node.py` | ROS Image → cv_bridge → YOLO → `/detections`입니다. |
| `agv_ws/src/agv_bringup/config/vision.yaml` | 모델 경로와 confidence를 코드 밖에 둡니다. |

## 만드는 순서

1. 설치 안내의 **5. YOLO 선택 설치**를 실행합니다.
2. `enable_yolo: false` 상태에서 node가 빈 `DetectionArray`를 publish하는지 먼저 확인합니다.
3. 모델 파일을 준비한 뒤 YAML에서 `enable_yolo: true`, `model_path`를 설정합니다.
4. YOLO box 중심 `center_x`와 영상 중심의 차이를 조향 오차로 사용합니다.

```bash
cd ~/ros2_curri/agv_ws && colcon build --symlink-install --packages-select agv_interfaces agv_vision
source install/setup.bash
ros2 run agv_vision yolo_node --ros-args -p enable_yolo:=true
ros2 topic echo /detections --once
```

## 확인

대상 물체가 보일 때 class/confidence/bounding box를 가진 detection이 나오면 통과입니다. GPU가 없어도 작은 모델과 낮은 camera FPS로 CPU 실습은 가능합니다.
