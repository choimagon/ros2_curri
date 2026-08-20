# M05~M14 단계별 모델 기준선

이 폴더는 최종 `urdf/`, `agv_gazebo/models/agv/`를 덮어쓰지 않는 **수업용 Complete snapshot**이다.
각 M 모듈은 바로 앞 단계 파일을 복사해 한 기능만 추가한다. M14를 완료한 뒤에는 최종 통합 모델을 단일 기준선으로 사용한다.

- M05: 매크로가 없는 단일 `agv.urdf`
- M06: 처음으로 Xacro property/macro 도입
- M07: 물리 요소만 있는 SDF
- M08: World와 spawn만, 센서/구동 plugin 없음
- M09: DiffDrive만 추가
- M12: Camera 추가, M13: LiDAR 추가, M14: IMU 추가

각 단계의 파일은 PPT `complete/`에도 같은 경로로 복사된다. 실제 통합 실행은 최종 `agv_gazebo/models/agv/model.sdf`를 사용한다.
