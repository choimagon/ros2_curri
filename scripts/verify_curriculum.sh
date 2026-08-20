#!/usr/bin/env bash
# 저장소 내부 파일 구성만 확인합니다. 파일을 바꾸지 않습니다.
set -u

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
missing=0

for module in $(seq -w 1 22); do
  # blocks/<block>/MXX_module/README.md만 찾는다. complete/starter의 README는 제외한다.
  guide=$(find "${root_dir}/blocks" -mindepth 3 -maxdepth 3 -path "*/M${module}_*/README.md" -print -quit)
  if [ -n "${guide}" ]; then
    printf 'OK      M%s %s\n' "${module}" "${guide#${root_dir}/}"
    module_dir="$(dirname "${guide}")"
    deck=$(find "${module_dir}" -maxdepth 1 -type f -name "M${module}_*.pptx" -print -quit)
    for artifact in starter/README.md complete/README.md screenshots/validation_terminal.png logs/validation.log CHECKSUM_or_TAG.txt; do
      if [ -f "${module_dir}/${artifact}" ]; then
        printf 'OK      M%s %s\n' "${module}" "${artifact}"
      else
        printf 'MISSING M%s %s\n' "${module}" "${artifact}"
        missing=1
      fi
    done
    if [ -n "${deck}" ]; then
      printf 'OK      M%s PPTX %s\n' "${module}" "${deck##*/}"
    else
      printf 'MISSING M%s module PPTX\n' "${module}"
      missing=1
    fi
  else
    printf 'MISSING M%s guide\n' "${module}"
    missing=1
  fi
done

for block in A B C D E F; do
  combined=$(find "${root_dir}/blocks" -maxdepth 2 -type f -name "Block_${block}_M시리즈_통합_따라하기.pptx" -print -quit)
  if [ -n "${combined}" ]; then
    printf 'OK      Block %s combined M-series PPTX %s\n' "${block}" "${combined#${root_dir}/}"
  else
    printf 'MISSING Block %s combined M-series PPTX\n' "${block}"
    missing=1
  fi
done

course_deck="${root_dir}/ROS_2_기반_AGV_End-to-End_개발_커리큘럼_전체_통합_따라하기.pptx"
if [ -f "${course_deck}" ]; then
  printf 'OK      Full-course combined PPTX %s\n' "${course_deck#${root_dir}/}"
else
  printf 'MISSING Full-course combined PPTX\n'
  missing=1
fi

for file in \
  docs/BEGINNER_FILE_MAKING_GUIDE.md \
  docs/PPT_FOLLOW_ALONG_DELIVERY.md \
  tools/create_module_presentations.py \
  tools/create_block_combined_presentations.py \
  tools/xwd_to_png.py \
  agv_ws/src/agv_cpp_examples/CMakeLists.txt \
  agv_ws/src/agv_cpp_examples/package.xml \
  agv_ws/src/agv_cpp_examples/src/status_publisher.cpp \
  agv_ws/src/agv_description/urdf/agv.urdf.xacro \
  agv_ws/src/agv_gazebo/worlds/warehouse.sdf \
  agv_ws/src/agv_gazebo/config/bridge.yaml \
  agv_ws/src/agv_control/agv_control/safety_controller.py \
  agv_ws/src/agv_sensors/agv_sensors/lidar_processor.py \
  agv_ws/src/agv_sensors/agv_sensors/odom_path.py \
  agv_ws/src/agv_vision/agv_vision/yolo_node.py \
  agv_ws/src/agv_mission/agv_mission/mission_manager.py \
  agv_ws/src/agv_mission/agv_mission/mission_markers.py \
  agv_ws/src/agv_bringup/launch/agv_sim.launch.py; do
  if [ -f "${root_dir}/${file}" ]; then
    printf 'OK      %s\n' "${file}"
  else
    printf 'MISSING %s\n' "${file}"
    missing=1
  fi
done

exit "${missing}"
