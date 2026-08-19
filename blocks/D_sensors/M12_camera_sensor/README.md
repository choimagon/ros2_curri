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
