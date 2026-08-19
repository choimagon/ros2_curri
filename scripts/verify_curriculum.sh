#!/usr/bin/env bash
# 저장소 내부 파일 구성만 확인합니다. 파일을 바꾸지 않습니다.
set -u

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
missing=0

for module in $(seq -w 1 22); do
  guide=$(find "${root_dir}/blocks" -path "*/M${module}_*/README.md" -print -quit)
  if [ -n "${guide}" ]; then
    printf 'OK      M%s %s\n' "${module}" "${guide#${root_dir}/}"
  else
    printf 'MISSING M%s guide\n' "${module}"
    missing=1
  fi
done

for file in \
  agv_ws/src/agv_description/urdf/agv.urdf.xacro \
  agv_ws/src/agv_gazebo/worlds/warehouse.sdf \
  agv_ws/src/agv_gazebo/config/bridge.yaml \
  agv_ws/src/agv_control/agv_control/safety_controller.py \
  agv_ws/src/agv_sensors/agv_sensors/lidar_processor.py \
  agv_ws/src/agv_vision/agv_vision/yolo_node.py \
  agv_ws/src/agv_mission/agv_mission/mission_manager.py \
  agv_ws/src/agv_bringup/launch/agv_sim.launch.py; do
  if [ -f "${root_dir}/${file}" ]; then
    printf 'OK      %s\n' "${file}"
  else
    printf 'MISSING %s\n' "${file}"
    missing=1
  fi
done

exit "${missing}"
