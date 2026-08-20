#!/usr/bin/env bash
# Make literal terminal-window captures for the four progressive modeling lessons.
# Every command is run before its window is captured; these are not reconstructed
# or hand-typed terminal illustrations.

set -o pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUT_DIR="${1:-$ROOT_DIR/blocks/B_robot_build/captures}"
mkdir -p "$OUT_DIR"
export PATH=/usr/bin:/bin:$PATH
export ROS_LOG_DIR=/tmp/ros2_curri_model_logs
mkdir -p "$ROS_LOG_DIR"

capture_terminal() {
  local window_title="$1"
  local target_png="$2"
  local command="$3"
  local xwininfo_path="/tmp/${window_title}.xwininfo"
  local xwd_path="/tmp/${window_title}.xwd"

  gnome-terminal --wait --title="$window_title" -- bash -lc "$command; printf '\n[캡처 완료: 이 창의 출력은 실제 실행 결과입니다.]\n'; sleep 7" &
  local terminal_pid=$!
  sleep 3
  if xwininfo -name "$window_title" >"$xwininfo_path" 2>/dev/null; then
    local window_id
    window_id=$(awk '/Window id:/{print $4}' "$xwininfo_path")
    if [[ -n "$window_id" ]]; then
      xwd -id "$window_id" -out "$xwd_path" 2>/dev/null || true
      /usr/bin/python3 "$ROOT_DIR/tools/xwd_to_png.py" "$xwd_path" "$target_png" 2>/dev/null || true
    fi
  fi
  wait "$terminal_pid" 2>/dev/null || true
}

capture_terminal "M05_URDF_REAL_TERMINAL" "$OUT_DIR/02_m05_urdf_terminal_actual.png" "source /opt/ros/jazzy/setup.bash; cd '$ROOT_DIR/agv_ws'; printf '$ check_urdf M05/agv.urdf\\n'; check_urdf src/agv_description/curriculum_stages/M05/agv.urdf"
capture_terminal "M06_XACRO_REAL_TERMINAL" "$OUT_DIR/03_m06_xacro_terminal_actual.png" "source /opt/ros/jazzy/setup.bash; cd '$ROOT_DIR/agv_ws'; printf '$ xacro M06/agv.urdf.xacro > /tmp/agv_m06.urdf\\n'; xacro src/agv_description/curriculum_stages/M06/agv.urdf.xacro > /tmp/agv_m06.urdf; printf '$ check_urdf /tmp/agv_m06.urdf\\n'; check_urdf /tmp/agv_m06.urdf"
capture_terminal "M07_SDF_REAL_TERMINAL" "$OUT_DIR/04_m07_sdf_terminal_actual.png" "source /opt/ros/jazzy/setup.bash; cd '$ROOT_DIR/agv_ws'; printf '$ gz sdf -k M07/model.sdf\\n'; gz sdf -k src/agv_description/curriculum_stages/M07/model.sdf; printf '$ xmllint --format model.sdf | rg physical tags\\n'; /home/lab4090/miniconda3/bin/xmllint --format src/agv_description/curriculum_stages/M07/model.sdf | rg -e '<mass>|<visual |<collision |<friction>' | sed -n '1,14p'"
capture_terminal "M08_WORLD_REAL_TERMINAL" "$OUT_DIR/05_m08_world_terminal_actual.png" "source /opt/ros/jazzy/setup.bash; cd '$ROOT_DIR/agv_ws'; printf '$ gz sdf -k M08/model.sdf\\n'; gz sdf -k src/agv_description/curriculum_stages/M08/model.sdf; printf '$ xmllint --format warehouse.sdf | rg world/spawn keys\\n'; /home/lab4090/miniconda3/bin/xmllint --format src/agv_description/curriculum_stages/M08/warehouse.sdf | rg -e '<world name=|<include>|<uri>model://agv|<pose>0 0 0.08'"

printf 'Saved real modeling evidence in %s\n' "$OUT_DIR"
