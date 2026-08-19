# Block E — 제어·인지·미션 (M16–M20)

이 Block은 “센서가 보인다”에서 끝나지 않고 perception 결과가 안전 우선순위를 거쳐 `/cmd_vel`로 연결되게 만듭니다. 처음에는 YOLO 없이 빈 detection과 LiDAR만으로 상태머신을 검증한 후 M17의 선택 의존성을 켭니다.
