# 따라 하기형 PPT 배포 구조

`ROS2_Gazebo_AGV_따라하기형_PPT_제작_가이드.docx`를 기준으로 M01~M22 각각을 독립 PPT로 배포한다. Block별 요약 PPT는 빠른 개요용이며, 실제 수업에서는 각 모듈 폴더의 `MXX_*.pptx`를 순서대로 사용한다.

## 공통 구성

모듈 PPT는 다음 순서를 사용한다.

1. 표지와 기준 환경
2. 이전 Complete → 현재 모듈 → 다음 Starter 로드맵
3. 시작 상태와 완료 조건
4. 개념 흐름도와 파일 변화
5. 한 장 한 행동의 명령·전체 코드
6. build → source → run
7. 실제 validation terminal 또는 Gazebo/RViz 화면
8. 객관적 검증 명령, 대표 오류, 미니 실습
9. Complete checkpoint와 공식 참고 자료

모든 코드 슬라이드는 `~/agv_ws/src/...` 전체 경로와 파일 전체를 제공한다. 길면 `파일 전체 1/N`처럼 이어지며 `...`로 생략하지 않는다. 제목은 30 pt 이상, 본문은 18 pt 이상, 코드/명령은 14 pt, 하단 주석은 10 pt 이상으로 생성한다. 발표자 노트에는 설명·실행·확인·멈춤·오류를 넣는다.

## 모듈별 자료

각 `blocks/**/MXX_*/` 폴더에는 다음이 있다.

- `starter/README.md`: 시작 상태와 선행 Complete
- `complete/`: PPT에서 다루는 실제 핵심 소스 snapshot
- `screenshots/validation_terminal.png`: 생성 시점에 실제 ROS 2 환경에서 수집한 검증 화면
- `logs/validation.log`: 위 캡처의 원본 텍스트
- `CHECKSUM_or_TAG.txt`: Complete와 대조할 SHA-256 manifest

M08에는 실제 Gazebo 화면, M11에는 실제 RViz2 화면도 `screenshots/`에 함께 둔다. GUI가 아닌 모듈은 패키지·interface·Xacro/SDF·launch·parameter 검증 명령을 실제로 실행한 terminal 화면을 사용한다.

## 다시 만들기

PPT와 배포 자료는 다음 명령으로 다시 만든다.

```bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_curri
/tmp/agv_pptx_env/bin/python tools/create_module_presentations.py
```

스크립트는 기존 source를 변경하지 않는다. 각 모듈의 `complete/` snapshot, validation log, terminal capture와 PPTX만 새로 만든다.
