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

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `ros2 run agv_vision yolo_node --ros-args -p enable_yolo:=true` | node를 시작하면서 YAML의 `enable_yolo` 값을 이 실행에 한해 true로 덮어씁니다. 시작 시 `ultralytics.YOLO(model_path)`를 로드합니다. | `-p model_path:=/절대/경로/model.pt`, `-p confidence_threshold:=0.70`처럼 모델·threshold를 함께 바꿀 수 있습니다. |
| `ros2 topic echo /detections --once` | 한 프레임의 `DetectionArray` 메시지를 받아 class·confidence·box 중심·크기를 확인합니다. | `--once`를 빼면 매 camera frame의 결과를 계속 봅니다. |
| `colcon build --packages-select agv_interfaces agv_vision` | 사용자 메시지 패키지를 먼저 생성하고 vision node가 그 메시지를 import하도록 빌드합니다. | `Detection.msg` 필드를 바꿨다면 두 패키지를 함께 다시 build/source합니다. |

## 내부 구현과 실행 뒤 보이는 결과

`yolo_node.py`는 `/camera/image_raw`의 header를 보존한 `DetectionArray`를 매 frame publish합니다. YOLO가 켜져 있으면 Image를 BGR OpenCV 배열로 변환하고, 각 box의 confidence가 `confidence_threshold` 이상일 때만 `class_name`, confidence, `center_x/center_y`, width/height를 채웁니다. `estimated_distance`는 현재 0.0으로 고정되어 있으므로 실제 거리 센서 융합은 아직 구현하지 않은 확장 과제입니다.

`enable_yolo: false`에서는 모델 파일이나 GPU가 없어도 **빈 detection 배열**이 계속 publish됩니다. 이것이 camera bridge와 message pipeline만 먼저 검증하는 안전한 기본값입니다. true인데 `ultralytics is not installed` 오류가 나면 코드가 fallback 추론을 하는 것이 아니라 모델을 비활성 상태로 두므로, 설치 후 재시작해야 class/box 결과가 생깁니다.
