#!/usr/bin/env bash
# Capture reproducible, real ROS 2 / Gazebo sensor evidence for the teaching decks.
# It starts the course bringup without autonomy, records ROS CLI output, saves one
# camera frame, and exits cleanly so the captures can be regenerated on the lab PC.

set -o pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUT_DIR="${1:-$ROOT_DIR/blocks/D_sensors/captures}"
LAUNCH_LOG="$OUT_DIR/sensor_only_launch_actual.log"
EVIDENCE_LOG="$OUT_DIR/sensor_topics_actual.log"
CAMERA_PNG="$OUT_DIR/01_camera_image_raw_actual.png"
VISION_PNG="$OUT_DIR/04_vision_debug_actual.png"

mkdir -p "$OUT_DIR"
export PATH=/usr/bin:/bin:$PATH
# The teaching repository is mounted read-only outside the workspace in the
# capture sandbox, so ROS launch logs must not default to ~/.ros/log.
export ROS_LOG_DIR=/tmp/ros2_curri_sensor_logs
mkdir -p "$ROS_LOG_DIR"
source /opt/ros/jazzy/setup.bash
source "$ROOT_DIR/agv_ws/install/setup.bash"

cleanup() {
  if [[ -n "${LAUNCH_PID:-}" ]] && kill -0 "$LAUNCH_PID" 2>/dev/null; then
    kill -TERM -- "-$LAUNCH_PID" 2>/dev/null || true
    wait "$LAUNCH_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

capture_terminal() {
  local window_title="$1"
  local target_png="$2"
  local command="$3"
  local xwininfo_path="/tmp/${window_title}.xwininfo"
  local xwd_path="/tmp/${window_title}.xwd"

  # A literal GNOME Terminal window makes the instruction and the output visible
  # together, instead of presenting a retyped transcript in the slides.
  gnome-terminal --wait --title="$window_title" -- bash -lc "$command; printf '\n[캡처 완료: 이 창의 출력은 실제 실행 결과입니다.]\n'; sleep 8" &
  local terminal_pid=$!
  sleep 4
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

# A separate process group lets cleanup stop Gazebo, bridge and child ROS nodes together.
setsid ros2 launch agv_bringup agv_sim.launch.py autonomy:=false >"$LAUNCH_LOG" 2>&1 &
LAUNCH_PID=$!

ready=0
for _ in $(seq 1 30); do
  if ros2 topic list 2>/dev/null | grep -qx '/camera/image_raw'; then
    ready=1
    break
  fi
  sleep 1
done

if [[ "$ready" -ne 1 ]]; then
  printf 'ERROR: /camera/image_raw was not available within 30 seconds.\n' >"$EVIDENCE_LOG"
  exit 1
fi

{
  printf '$ ros2 topic list | grep -E "camera|scan|imu|clock"\n'
  ros2 topic list | grep -E 'camera|scan|imu|clock' || true
  printf '\n$ ros2 topic info /camera/image_raw\n'
  ros2 topic info /camera/image_raw
  printf '\n$ ros2 topic echo /scan --once\n'
  timeout 8 ros2 topic echo /scan --once || true
  printf '\n$ ros2 topic echo /imu/data --once\n'
  timeout 8 ros2 topic echo /imu/data --once || true
  printf '\n$ ros2 topic echo /clock --once\n'
  timeout 8 ros2 topic echo /clock --once || true
  printf '\n$ ros2 topic hz /camera/image_raw (5 s)\n'
  timeout 5 ros2 topic hz /camera/image_raw || true
  printf '\n$ ros2 topic hz /scan (5 s)\n'
  timeout 5 ros2 topic hz /scan || true
  printf '\n$ ros2 topic hz /imu/data (5 s)\n'
  timeout 5 ros2 topic hz /imu/data || true
} >"$EVIDENCE_LOG" 2>&1

timeout 12 /usr/bin/python3 "$ROOT_DIR/tools/capture_ros_image.py" /camera/image_raw "$CAMERA_PNG" >>"$EVIDENCE_LOG" 2>&1 || true
timeout 12 /usr/bin/python3 "$ROOT_DIR/tools/capture_ros_image.py" /vision/debug_image "$VISION_PNG" >>"$EVIDENCE_LOG" 2>&1 || true

capture_terminal "M12_CAMERA_REAL_TERMINAL" "$OUT_DIR/02_camera_terminal_actual.png" "source /opt/ros/jazzy/setup.bash; source '$ROOT_DIR/agv_ws/install/setup.bash'; printf '$ ros2 topic info /camera/image_raw\\n'; ros2 topic info /camera/image_raw; printf '\\n$ ros2 topic hz /camera/image_raw (4 s)\\n'; timeout 4 ros2 topic hz /camera/image_raw || true"
capture_terminal "M13_LIDAR_REAL_TERMINAL" "$OUT_DIR/05_lidar_terminal_actual.png" "source /opt/ros/jazzy/setup.bash; source '$ROOT_DIR/agv_ws/install/setup.bash'; printf '$ ros2 topic echo /scan --once | grep key fields\\n'; timeout 6 ros2 topic echo /scan --once --qos-reliability best_effort | grep -E 'frame_id:|angle_min:|angle_max:|angle_increment:|range_min:|range_max:'; printf '\\n$ ros2 topic hz /scan (4 s)\\n'; timeout 4 ros2 topic hz /scan || true"
capture_terminal "M14_IMU_REAL_TERMINAL" "$OUT_DIR/06_imu_terminal_actual.png" "source /opt/ros/jazzy/setup.bash; source '$ROOT_DIR/agv_ws/install/setup.bash'; printf '$ ros2 topic echo /imu/data --once | grep key fields\\n'; timeout 6 ros2 topic echo /imu/data --once --qos-reliability best_effort | grep -E 'frame_id:|orientation:|angular_velocity:|linear_acceleration:'; printf '\\n$ ros2 topic hz /imu/data (4 s)\\n'; timeout 4 ros2 topic hz /imu/data || true"

if [[ ! -s "$CAMERA_PNG" ]]; then
  printf 'ERROR: camera PNG was not written. Inspect %s\n' "$LAUNCH_LOG" >>"$EVIDENCE_LOG"
  exit 1
fi

printf 'Saved real sensor evidence in %s\n' "$OUT_DIR"
