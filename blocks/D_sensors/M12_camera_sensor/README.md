# M12 — Camera Sensor

## 만드는 파일

| 파일 | 역할 |
| --- | --- |
| `agv_ws/src/agv_gazebo/models/agv/model.sdf` | `camera_link`의 camera sensor, resolution, FOV, update rate입니다. |
| `agv_ws/src/agv_gazebo/config/bridge.yaml` | Camera Image/CameraInfo bridge를 추가할 위치입니다. |
| `agv_ws/src/agv_vision/agv_vision/yolo_node.py` | Image를 받아 후속 인식으로 넘기는 node입니다. |

## 만드는 순서와 확인

SDF `camera`의 `width`, `height`, `horizontal_fov`, `update_rate`를 조절합니다. 먼저 `gz topic -l | rg camera`로 실제 Gazebo image topic을 찾고, 그 이름을 bridge YAML에 넣습니다. 이후:

```bash
ros2 topic list | rg camera
ros2 run rqt_image_view rqt_image_view
```

빨간 target이 camera 화면에 보이면 통과입니다. 검은 화면은 World 조명, camera pose, near/far clip, bridge 토픽 순으로 점검합니다.

## 명령어가 하는 일과 바꿔 볼 값

| 명령어 | 실제 동작 | 바꿔 볼 값 |
| --- | --- | --- |
| `gz topic -l \| rg camera` | 실행 중인 Gazebo Transport에서 camera라는 이름을 가진 원본 topic만 찾습니다. 아직 ROS bridge를 거치지 않은 목록입니다. | 출력된 정확한 이름을 `bridge.yaml`의 `gz_topic_name`과 맞춥니다. |
| `ros2 topic list \| rg camera` | bridge 이후 ROS DDS에서 보이는 camera topic을 찾습니다. | `/camera/image_raw`가 없으면 camera sensor보다 bridge YAML·bridge process를 먼저 확인합니다. |
| `ros2 run rqt_image_view rqt_image_view` | Image topic을 구독해 GUI에 그리는 도구입니다. 이미지 생성·인식은 하지 않습니다. | GUI의 topic 선택에서 `/camera/image_raw`를 고릅니다. |
| `ros2 topic hz /camera/image_raw` | Image 메시지 도착 주파수를 계산합니다. | 현재 SDF `update_rate`는 15 Hz이므로 PC 성능에 따라 이 값 근처를 기대합니다. |

## 내부 구현과 실행 뒤 보이는 결과

`model.sdf`의 `camera_link`에는 `type="camera"` sensor가 들어 있습니다. 항상 켜진 상태로 15 Hz, 640×480 RGB, 수평 FOV 1.047 rad(약 60°), near 0.1 m·far 20 m 범위를 사용해 `/camera/image_raw`를 만듭니다. `bridge.yaml`은 `gz.msgs.Image`를 ROS의 `sensor_msgs/msg/Image`로 단방향 변환합니다. `yolo_node.py`는 이 ROS Image를 `cv_bridge`로 OpenCV BGR 이미지로 바꾼 뒤 선택적으로 인식합니다.

정상 결과는 rqt_image_view에 AGV 전방의 World와 빨간 target이 보이는 것입니다. 해상도를 1280×720으로 올리면 작은 물체의 인식에는 유리하지만 bridge 전송량과 YOLO 처리 시간이 함께 늘어납니다. 검은 화면이면 `topic`만 존재하는지와 실제 메시지가 오는지는 별개이므로 `ros2 topic echo /camera/image_raw --once`로 헤더부터 확인합니다.
