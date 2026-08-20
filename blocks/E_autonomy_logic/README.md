# Block E — 제어·인지·미션 (M16–M20)

이 Block은 “센서가 보인다”에서 끝나지 않고 perception 결과가 안전 우선순위를 거쳐 `/cmd_vel`로 연결되게 만듭니다. M17은 설치된 YOLO 모델을 우선 사용하며, 설치 전에는 Gazebo의 빨간 목표물을 보여 주는 교육용 fallback 검출기를 사용해 동일한 `/detections`·미션 인터페이스를 검증합니다.

## Block 커리큘럼 요약

| 순서 | 핵심 결과 | 시각화 topic |
| --- | --- | --- |
| M16 | controller 설정과 wheel interface | `/joint_states`, controller 상태 |
| M17 | Image → detection → debug image | `/detections`, `/vision/debug_image` |
| M18 | LiDAR 기반 STOP 우선순위 | `/obstacle_distance`, `/agv_markers` |
| M19 | SEARCH·APPROACH·AVOID·GOAL FSM | `/mission_state`, text Marker |
| M20 | error → 제한된 Twist 제어 | `/target_error`, `/cmd_vel_raw`, `/path` |

[M 시리즈 통합 PPT](Block_E_M시리즈_통합_따라하기.pptx)로 제어·인지·미션의 데이터 흐름을 한 번에 강의하거나 복습할 수 있습니다.
