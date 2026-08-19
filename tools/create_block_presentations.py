#!/usr/bin/env python3
"""Create Korean Block presentations with terminal captures from real commands."""
from __future__ import annotations

import os
import subprocess
import textwrap
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "agv_ws"
FONT = "Noto Sans CJK KR"
FONT_FILE = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD_FILE = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def shell(command: str) -> str:
    """Run the command on the actual ROS installation and return its terminal text."""
    env_prefix = "export PATH=/usr/bin:/bin:$PATH; source /opt/ros/jazzy/setup.bash; source install/setup.bash; "
    completed = subprocess.run(
        ["bash", "-c", env_prefix + command],
        cwd=WORKSPACE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=45,
        check=False,
    )
    text = completed.stdout.strip()
    return text if text else "(명령은 오류 출력 없이 완료되었습니다.)"


BLOCKS = [
    {
        "key": "A",
        "folder": "blocks/A_ros2_basics",
        "title": "Block A — ROS 2 기초",
        "modules": "M01 ROS 2 개념 · M02 Workspace · M03 Pub/Sub · M04 TF2",
        "goal": "ROS 2 노드·토픽 흐름을 확인하고 AGV의 기본 TF tree를 이해한다.",
        "files": [
            "agv_control/agv_control/counter_publisher.py",
            "agv_control/agv_control/counter_monitor.py",
            "agv_description/urdf/agv.urdf.xacro",
            "agv_description/launch/display.launch.py",
        ],
        "commands": """source /opt/ros/jazzy/setup.bash
cd /home/lab4090/ros2_curri/agv_ws
colcon build --symlink-install --packages-select agv_control agv_description
source install/setup.bash
ros2 run agv_control counter_publisher
# 새 터미널: ros2 run agv_control counter_monitor""",
        "capture_command": """tmp=$(mktemp -d /tmp/agv_ppt_a.XXXXXX); export ROS_LOG_DIR=$tmp; timeout --signal=INT 5s ros2 run agv_control counter_publisher >$tmp/publisher.log 2>&1 & pub=$!; sleep 1; timeout --signal=INT 3s ros2 run agv_control counter_monitor 2>&1 || true; wait $pub || true""",
        "checks": "counter_monitor에 received /counter가 반복되면 publisher·subscriber·DDS 통신이 정상이다. 다음으로 M04에서 RViz Fixed Frame과 TF tree를 확인한다.",
    },
    {
        "key": "B",
        "folder": "blocks/B_robot_build",
        "title": "Block B — AGV 로봇 제작",
        "modules": "M05 URDF · M06 Xacro · M07 물리 · M08 Gazebo World",
        "goal": "body, 바퀴, caster, LiDAR, camera, IMU를 가진 AGV 모델을 URDF/Xacro와 SDF로 만든다.",
        "files": [
            "agv_description/urdf/common.xacro",
            "agv_description/urdf/wheels.xacro",
            "agv_description/urdf/sensors.xacro",
            "agv_gazebo/models/agv/model.sdf",
            "agv_gazebo/worlds/warehouse.sdf",
        ],
        "commands": """cd /home/lab4090/ros2_curri/agv_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
xacro src/agv_description/urdf/agv.urdf.xacro > /tmp/agv.urdf
check_urdf /tmp/agv.urdf
ros2 launch agv_gazebo gazebo.launch.py""",
        "capture_command": """xacro src/agv_description/urdf/agv.urdf.xacro > /tmp/agv_ppt.urdf && check_urdf /tmp/agv_ppt.urdf && gz sdf -k src/agv_gazebo/models/agv/model.sdf""",
        "checks": "check_urdf 출력에 base_footprint → base_link와 두 바퀴·세 센서 link가 보이면 모델 구조가 정상이다. Gazebo에서 바닥 관통이나 진동이 없는지 이어서 확인한다.",
    },
    {
        "key": "C",
        "folder": "blocks/C_drive_visualization",
        "title": "Block C — 주행과 시각화",
        "modules": "M09 Differential Drive · M10 ros_gz_bridge · M11 RViz2",
        "goal": "Gazebo의 DiffDrive에 /cmd_vel을 전달하고 odom·scan을 ROS/RViz에서 확인한다.",
        "files": [
            "agv_gazebo/models/agv/model.sdf",
            "agv_gazebo/config/bridge.yaml",
            "agv_gazebo/launch/gazebo.launch.py",
            "agv_control/agv_control/cmd_test_node.py",
        ],
        "commands": """ros2 launch agv_gazebo gazebo.launch.py
# 새 터미널
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist \\
  \"{linear: {x: 0.15}, angular: {z: 0.0}}\"
ros2 topic echo /odom --once
ros2 topic echo /scan --once
rviz2""",
        "capture_command": """printf 'Gazebo Sim version: '; gz sim --versions; printf '\\nros_gz_bridge prefix: '; ros2 pkg prefix ros_gz_bridge; printf '\\nSDF validation: '; gz sdf -k src/agv_gazebo/models/agv/model.sdf""",
        "checks": "Gazebo Harmonic 버전과 ros_gz_bridge 설치 경로가 출력되면 연동 도구가 준비된 상태다. 실제 주행 후 RViz에서 Fixed Frame=odom, Odometry=/odom, LaserScan=/scan을 설정한다.",
    },
    {
        "key": "D",
        "folder": "blocks/D_sensors",
        "title": "Block D — 센서",
        "modules": "M12 Camera · M13 2D LiDAR · M14 IMU · M15 운영/QoS",
        "goal": "Gazebo 센서를 생성하고 ROS topic, frame_id, /clock, update rate를 관리한다.",
        "files": [
            "agv_gazebo/models/agv/model.sdf",
            "agv_gazebo/config/bridge.yaml",
            "agv_sensors/agv_sensors/lidar_processor.py",
            "agv_sensors/agv_sensors/imu_monitor.py",
            "agv_bringup/config/sensors.yaml",
        ],
        "commands": """ros2 launch agv_bringup agv_sim.launch.py rviz:=false
# 새 터미널
ros2 topic hz /scan
ros2 topic echo /imu/data --once
ros2 run agv_sensors lidar_processor
ros2 topic echo /obstacle_distance
ros2 run rqt_image_view rqt_image_view""",
        "capture_command": """printf 'SDF sensor declarations\\n'; rg -n '<sensor name=|<topic>|<update_rate>' src/agv_gazebo/models/agv/model.sdf; printf '\\nBridge mapping\\n'; cat src/agv_gazebo/config/bridge.yaml""",
        "checks": "SDF에 camera·lidar·imu sensor와 topic/update_rate가, bridge YAML에 ROS 메시지 타입과 방향이 함께 있어야 한다. 실행 중에는 topic hz와 header.frame_id를 반드시 확인한다.",
    },
    {
        "key": "E",
        "folder": "blocks/E_autonomy_logic",
        "title": "Block E — 제어·인지·미션",
        "modules": "M16 ros2_control · M17 YOLO · M18 장애물 인지 · M19 FSM · M20 PID",
        "goal": "센서·detection을 안전 우선순위와 상태머신으로 연결해 /cmd_vel을 만든다.",
        "files": [
            "agv_interfaces/msg/Detection.msg",
            "agv_interfaces/msg/DetectionArray.msg",
            "agv_vision/agv_vision/yolo_node.py",
            "agv_control/agv_control/safety_controller.py",
            "agv_mission/agv_mission/mission_manager.py",
        ],
        "commands": """cd /home/lab4090/ros2_curri/agv_ws
source install/setup.bash
ros2 interface show agv_interfaces/msg/Detection
ros2 run agv_sensors lidar_processor
ros2 run agv_control safety_controller --ros-args -p stop_distance:=0.5
ros2 run agv_mission mission_manager
ros2 topic echo /mission_state""",
        "capture_command": """ros2 interface show agv_interfaces/msg/Detection; printf '\\n--- 실행 파일 ---\\n'; ros2 pkg executables agv_control; ros2 pkg executables agv_mission; ros2 pkg executables agv_vision""",
        "checks": "Detection 메시지 필드와 safety_controller·mission_manager 실행 파일이 출력되면 인지→안전→미션 구조가 빌드됐다. YOLO는 M17 문서의 가상환경 설치 후 enable_yolo=true로 활성화한다.",
    },
    {
        "key": "F",
        "folder": "blocks/F_integration",
        "title": "Block F — 통합·재현·최종 프로젝트",
        "modules": "M21 YAML/Launch/rosbag2 · M22 Final Project",
        "goal": "YAML과 하나의 launch 명령으로 전체 시스템을 재현하고 rosbag으로 주행을 기록한다.",
        "files": [
            "agv_bringup/config/robot.yaml",
            "agv_bringup/config/sensors.yaml",
            "agv_bringup/config/vision.yaml",
            "agv_bringup/config/mission.yaml",
            "agv_bringup/launch/agv_sim.launch.py",
        ],
        "commands": """export PATH=/usr/bin:/bin:$PATH  # Miniconda 사용 시
source /opt/ros/jazzy/setup.bash
cd /home/lab4090/ros2_curri/agv_ws
colcon build --symlink-install --cmake-args -DPython3_EXECUTABLE=/usr/bin/python3
source install/setup.bash
ros2 launch agv_bringup agv_sim.launch.py
ros2 bag record -o ~/agv_bag_01 /scan /imu/data /odom /camera/image_raw""",
        "capture_command": """colcon list; printf '\\n--- 최종 launch 인자 ---\\n'; ros2 launch agv_bringup agv_sim.launch.py --show-args; printf '\\n--- 의존성 ---\\n'; rosdep check --from-paths src --ignore-src --rosdistro jazzy --skip-keys ament_python""",
        "checks": "8개 패키지와 agv_sim.launch.py 인자가 출력되고 rosdep이 All system dependencies have been satisfied를 표시하면 재현 가능한 최종 구조다.",
    },
]


def trim(text: str, max_lines: int = 20, max_width: int = 100) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        lines.extend(textwrap.wrap(line, width=max_width, replace_whitespace=False) or [""])
    if len(lines) > max_lines:
        lines = lines[: max_lines - 1] + ["… (출력 일부 생략)"]
    return "\n".join(lines)


def terminal_capture(path: Path, title: str, command: str, output: str) -> None:
    width, height = 1920, 1080
    image = Image.new("RGB", (width, height), "#10151f")
    draw = ImageDraw.Draw(image)
    bold = ImageFont.truetype(FONT_BOLD_FILE, 32)
    regular = ImageFont.truetype(FONT_FILE, 20)
    small = ImageFont.truetype(FONT_FILE, 18)
    draw.rounded_rectangle((45, 35, width - 45, height - 35), radius=26, fill="#171f2e", outline="#34415b", width=2)
    draw.ellipse((75, 69, 93, 87), fill="#ff6258")
    draw.ellipse((104, 69, 122, 87), fill="#f5bf4f")
    draw.ellipse((133, 69, 151, 87), fill="#58c051")
    draw.text((180, 56), title + " — 실제 터미널 실행 캡처", font=bold, fill="#f2f5fb")
    draw.text((80, 130), "$ " + command.replace("\n", "\n$ "), font=small, fill="#8fd7ff", spacing=7)
    divider_y = 280
    draw.line((80, divider_y, width - 80, divider_y), fill="#41506e", width=2)
    draw.text((80, divider_y + 28), trim(output), font=regular, fill="#e6edf7", spacing=8)
    draw.text((80, height - 90), "캡처 생성 시각: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), font=small, fill="#9aa9c1")
    image.save(path)


def add_textbox(slide, left, top, width, height, text, size=14, bold=False, color=RGBColor(33, 43, 61), bullet=False):
    box = slide.shapes.add_textbox(left, top, width, height)
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.vertical_anchor = MSO_ANCHOR.TOP
    for index, line in enumerate(text.splitlines() or [""]):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = line
        paragraph.font.name = FONT
        paragraph.font.size = Pt(max(size, 10))
        paragraph.font.bold = bold
        paragraph.font.color.rgb = color
        paragraph.space_after = Pt(5)
        if bullet and line:
            paragraph.level = 0
            paragraph.text = "• " + line
    return box


def add_header(slide, title: str, subtitle: str) -> None:
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.82))
    banner.fill.solid(); banner.fill.fore_color.rgb = RGBColor(23, 62, 111); banner.line.fill.background()
    add_textbox(slide, Inches(0.45), Inches(0.15), Inches(8.8), Inches(0.35), title, 25, True, RGBColor(255, 255, 255))
    add_textbox(slide, Inches(9.1), Inches(0.20), Inches(3.8), Inches(0.28), subtitle, 10, False, RGBColor(220, 234, 252))
    add_textbox(slide, Inches(0.45), Inches(7.17), Inches(12.3), Inches(0.18), "ROS 2 + Gazebo AGV 실습 · 모든 텍스트 최소 10pt", 10, False, RGBColor(102, 112, 128))


def add_bullets(slide, title: str, lines: list[str]) -> None:
    add_textbox(slide, Inches(0.65), Inches(1.05), Inches(12), Inches(0.45), title, 21, True, RGBColor(23, 62, 111))
    add_textbox(slide, Inches(0.8), Inches(1.65), Inches(11.7), Inches(4.9), "\n".join(lines), 15, False, bullet=True)


def add_code_slide(slide, block: dict) -> None:
    add_header(slide, block["title"], "명령어 실행 순서")
    add_textbox(slide, Inches(0.65), Inches(1.02), Inches(12), Inches(0.35), "권장 실행 순서", 21, True, RGBColor(23, 62, 111))
    code = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), Inches(1.55), Inches(12.0), Inches(4.95))
    code.fill.solid(); code.fill.fore_color.rgb = RGBColor(20, 28, 42); code.line.color.rgb = RGBColor(64, 80, 110)
    frame = code.text_frame; frame.clear(); frame.margin_left = Inches(0.26); frame.margin_top = Inches(0.20)
    for index, line in enumerate(block["commands"].splitlines()):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = line
        paragraph.font.name = FONT
        paragraph.font.size = Pt(11)
        paragraph.font.color.rgb = RGBColor(223, 237, 255)
        paragraph.space_after = Pt(7)
    add_textbox(slide, Inches(0.75), Inches(6.66), Inches(11.8), Inches(0.28), "명령은 Block README의 순서와 동일합니다. 새 터미널에서도 ROS와 workspace를 source해야 합니다.", 10, False, RGBColor(80, 92, 112))


def create_presentation(block: dict, capture: Path) -> None:
    ppt = Presentation()
    ppt.slide_width = Inches(13.333)
    ppt.slide_height = Inches(7.5)
    blank = ppt.slide_layouts[6]

    cover = ppt.slides.add_slide(blank)
    cover.background.fill.solid(); cover.background.fill.fore_color.rgb = RGBColor(244, 248, 253)
    stripe = cover.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
    stripe.fill.solid(); stripe.fill.fore_color.rgb = RGBColor(23, 62, 111); stripe.line.fill.background()
    add_textbox(cover, Inches(0.75), Inches(1.65), Inches(11.8), Inches(0.7), block["title"], 34, True, RGBColor(23, 62, 111))
    add_textbox(cover, Inches(0.78), Inches(2.52), Inches(11.6), Inches(0.4), block["modules"], 17, False, RGBColor(63, 83, 115))
    add_textbox(cover, Inches(0.78), Inches(3.4), Inches(11.4), Inches(0.8), block["goal"], 20, False, RGBColor(33, 43, 61))
    add_textbox(cover, Inches(0.78), Inches(6.45), Inches(11.4), Inches(0.35), "실제 실행 결과 캡처 포함 · 한국어 작성 · 최소 글꼴 크기 10pt", 12, False, RGBColor(89, 104, 126))

    overview = ppt.slides.add_slide(blank)
    add_header(overview, block["title"], "만들어진 파일")
    add_bullets(overview, "이 Block에서 실제로 만든 핵심 파일", block["files"])
    add_textbox(overview, Inches(0.8), Inches(5.85), Inches(11.7), Inches(0.55), "모듈별 만드는 방법과 상세 확인 기준은 이 폴더의 Mxx/README.md에 정리되어 있습니다.", 13, False, RGBColor(63, 83, 115))

    commands = ppt.slides.add_slide(blank)
    add_code_slide(commands, block)

    result = ppt.slides.add_slide(blank)
    add_header(result, block["title"], "실제 실행 결과")
    result.shapes.add_picture(str(capture), Inches(0.45), Inches(1.02), width=Inches(12.43), height=Inches(5.93))

    checklist = ppt.slides.add_slide(blank)
    add_header(checklist, block["title"], "확인 기준과 다음 단계")
    add_bullets(checklist, "통과 기준", [block["checks"], "문제가 생기면 README의 '확인' 명령부터 다시 실행하고, 첫 오류 메시지를 기준으로 수정합니다."])

    output = ROOT / block["folder"] / f"Block_{block['key']}_실습결과_명령어.pptx"
    ppt.save(output)


def main() -> None:
    for block in BLOCKS:
        block_dir = ROOT / block["folder"]
        capture_dir = block_dir / "captures"
        capture_dir.mkdir(exist_ok=True)
        output = shell(block["capture_command"])
        command_display = block["capture_command"].replace("; ", ";\n")
        capture = capture_dir / f"block_{block['key'].lower()}_actual_terminal.png"
        terminal_capture(capture, block["title"], command_display, output)
        create_presentation(block, capture)
        ppt_name = f"Block_{block['key']}_실습결과_명령어.pptx"
        print(f"created {capture.relative_to(ROOT)}")
        print(f"created {(block_dir / ppt_name).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
