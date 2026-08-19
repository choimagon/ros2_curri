#!/usr/bin/env bash
# 읽기 전용 설치 상태 점검. 관리자 권한과 네트워크가 필요하지 않습니다.
set -u

printf 'OS: '
. /etc/os-release
printf '%s %s (%s)\n' "${NAME}" "${VERSION_ID}" "${VERSION_CODENAME:-unknown}"
printf 'Architecture: '
dpkg --print-architecture
printf 'Locale: '
locale | awk -F= '/^LANG=/{print $2}'

check_command() {
  local command_name="$1"
  if command -v "${command_name}" >/dev/null 2>&1; then
    printf 'OK      %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"
  else
    printf 'MISSING %s\n' "${command_name}"
  fi
}

check_command ros2
check_command colcon
check_command gz

if [ -f /opt/ros/jazzy/setup.bash ]; then
  printf 'OK      /opt/ros/jazzy/setup.bash\n'
else
  printf 'MISSING /opt/ros/jazzy/setup.bash\n'
fi

if [ -e /etc/apt/sources.list.d/ros2.sources ] || [ -f /etc/apt/sources.list.d/ros2.list ] || [ -f /etc/apt/sources.list.d/ros2-latest.list ]; then
  printf 'OK      ROS 2 apt source file\n'
else
  printf 'MISSING ROS 2 apt source file\n'
fi

printf '\nNext: source /opt/ros/jazzy/setup.bash, then run the commands in docs/INSTALL_UBUNTU_24.04_ROS2_JAZZY.md.\n'
