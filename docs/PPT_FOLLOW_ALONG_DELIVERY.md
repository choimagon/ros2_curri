# 따라 하기형 PPT 배포 구조

`ROS2_Gazebo_AGV_따라하기형_PPT_제작_가이드.docx`를 기준으로 M01~M22 각각을 독립 PPT로 배포한다. 실제 수업에서는 각 모듈 폴더의 `MXX_*.pptx`를 순서대로 사용한다. 각 Block 루트의 `Block_*_M시리즈_통합_따라하기.pptx`는 해당 M 시리즈를 순서대로 합친 보기용 자료이며, 별도의 ‘실습 결과 명령어’ 요약 PPT는 배포하지 않는다.

## 공통 구성

모듈 PPT는 다음 순서를 사용한다.

1. 표지와 기준 환경
2. 이전 Complete → 현재 모듈 → 다음 Starter 로드맵
3. 시작 상태와 완료 조건
4. 개념 흐름도와 파일 변화
5. 이번 기능이 전체 AGV 프로젝트에 추가하는 역할과 완성 결과 미리보기
6. package 생성 → 폴더 생성 → 빈 파일 열기
7. 파일마다 핵심 코드/태그를 2개씩 읽기: **뜻**과 **실행에서 보이는 변화**를 먼저 말해 보기
8. 파일별 코드 블록 입력·저장
9. build → source → run과 실제 결과 확인
10. 객관적 검증 명령, 대표 오류, 미니 실습
11. 막혔을 때만 Complete와 diff·backup·복구
12. 내 workspace checkpoint와 공식 참고 자료

코드 슬라이드는 `~/ros2_curri/my_agv_ws/src/...`의 빈 파일을 먼저 열고, 해당 파일의 코드 블록을 위에서 아래로 직접 입력·저장하게 한다. 입력 전에는 실제 코드/태그 두 개를 한 페이지에 놓고 `뜻`과 `실행에서`를 설명한다. 즉 `create_publisher()`는 “어느 topic에 내보낼지 만든다”와 “`ros2 topic info`에서 publisher가 보인다”를, `<sensor>`는 “Gazebo sensor를 붙인다”와 “sensor topic이 생긴다”를 연결한다. 저장소의 `agv_ws/`는 참고 구현이며 학습자가 직접 고치지 않는다. 길면 `입력 1/N`처럼 이어지며 `...`로 생략하지 않는다. `complete/`는 먼저 복사하는 정답지가 아니라, 오류가 해결되지 않을 때 `diff`로 비교하고 backup 뒤 복구하는 안전망이다. 제목은 30 pt 이상, 본문은 18 pt 이상, 코드/명령은 14 pt, 하단 주석은 10 pt 이상으로 생성한다. 발표자 노트에는 설명·실행·확인·멈춤·오류를 넣는다.

## 모듈별 자료

각 `blocks/**/MXX_*/` 폴더에는 다음이 있다.

- `starter/README.md`: 시작 상태와 선행 Complete
- `complete/`: PPT에서 다루는 실제 핵심 소스 snapshot
- `screenshots/validation_terminal.png`: 생성 시점에 실제 ROS 2 환경에서 수집한 검증 화면
- `logs/validation.log`: 위 캡처의 원본 텍스트
- `CHECKSUM_or_TAG.txt`: Complete와 대조할 SHA-256 manifest

M08에는 실제 Gazebo 화면, M11에는 실제 RViz2 화면도 `screenshots/`에 함께 둔다. 모델링 M05~M08에는 실제 `check_urdf`·Xacro·SDF·World 검사 GNOME Terminal 화면을, 센서 M12~M15에는 실제 Gazebo Camera frame, vision debug frame, Camera/LiDAR/IMU GNOME Terminal 화면을 추가한다. 각 캡처의 PPT 하단에는 교육생이 찾아야 할 값도 적는다.

## 다시 만들기

PPT와 배포 자료는 다음 명령으로 다시 만든다.

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_curri
/tmp/agv_pptx_env/bin/python tools/create_module_presentations.py
```

`tools/capture_modeling_evidence.sh`와 `tools/capture_sensor_evidence.sh`는 실제 Ubuntu GUI 세션에서 증거 화면을 다시 만들고, `tools/create_module_presentations.py`는 각 모듈의 `complete/` snapshot, validation log, terminal/GUI capture와 PPTX를 다시 만든다. 센서 캡처 스크립트는 `~/.ros`가 아닌 `/tmp`에 ROS launch log를 기록한다.
