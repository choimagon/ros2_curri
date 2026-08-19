# 이 컴퓨터용 설치·검증 가이드

## 이 컴퓨터에서 먼저 확인한 값

| 항목 | 확인값 | 의미 |
| --- | --- | --- |
| 운영체제 | Ubuntu 24.04.4 LTS (Noble) | ROS 2 Jazzy의 공식 대상 OS입니다. |
| CPU 아키텍처 | amd64 | 공식 apt 바이너리 패키지를 사용할 수 있습니다. |
| 기본 locale | `C.UTF-8` | UTF-8이지만 ROS 권장 locale로 한 번 정리합니다. |
| ROS 2 / colcon / Gazebo | 미설치 | 아래 설치를 처음부터 실행해야 합니다. |

이 조합은 Gazebo 공식 문서가 권장하는 ROS 2 Jazzy + Gazebo Harmonic 조합입니다. ROS와 Gazebo는 독립 프로젝트이므로, ROS 저장소 등록 뒤 `ros-jazzy-ros-gz`를 설치해 검증된 조합을 함께 받습니다.

## 0. 설치 전 준비

터미널을 열고 아래를 한 줄씩 실행합니다. `sudo`에서 나오는 비밀번호 입력은 화면에 보이지 않는 것이 정상입니다.

```bash
sudo apt-get update
sudo apt-get install -y locales software-properties-common curl
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
locale
sudo add-apt-repository -y universe
```

마지막 `locale` 출력에 `UTF-8`이 보이면 통과입니다. `export`는 **현재 터미널에만** 적용되며, 새 터미널은 아래 ROS 환경 설정까지 끝낸 뒤 다시 엽니다.

## 1. 공식 ROS 2 저장소 등록

아래 명령은 ROS에서 관리하는 `ros2-apt-source` 패키지를 내려받아 apt 키와 저장소를 함께 설정합니다. 키 파일을 직접 복사하는 오래된 설치법보다 이 방법을 사용합니다.

```bash
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F 'tag_name' | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt-get update
```

### 저장소 확인

```bash
apt-cache policy ros-jazzy-desktop
```

`Candidate:` 아래에 버전이 보이면 성공입니다. `Candidate: (none)`이면 인터넷 연결, `sudo dpkg -i` 오류, 또는 이전 명령의 다운로드 실패를 먼저 확인합니다.

## 2. ROS 2, Gazebo, 개발 도구 설치

아래 한 번의 설치는 데스크톱 도구(RViz2 포함), 빌드 도구, `ros_gz`/Gazebo Harmonic 연동, 이 커리큘럼에서 바로 쓰는 URDF·TF·영상 도구를 설치합니다.

```bash
sudo apt-get install -y \
  ros-jazzy-desktop \
  ros-dev-tools \
  ros-jazzy-ros-gz \
  ros-jazzy-xacro \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-tf2-tools \
  ros-jazzy-rqt-image-view \
  ros-jazzy-image-transport \
  ros-jazzy-cv-bridge \
  ros-jazzy-vision-opencv \
  ros-jazzy-ros2-control \
  ros-jazzy-ros2-controllers \
  ros-jazzy-gz-ros2-control \
  python3-opencv python3-venv
```

`ros-jazzy-ros-gz`가 Jazzy에 맞는 Gazebo Harmonic vendor 패키지와 ROS–Gazebo bridge를 설치합니다. 별도의 Gazebo Classic 설치는 하지 마세요.

## 3. 셸 환경 설정

현재 터미널에서 즉시 적용합니다.

```bash
source /opt/ros/jazzy/setup.bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

`~/.bashrc`에는 한 번만 추가해야 합니다. 이미 같은 줄이 있으면 다시 추가하지 마세요. 워크스페이스를 빌드한 뒤에는 아래 줄도 한 번 추가합니다.

```bash
echo "source ~/ros2_curri/agv_ws/install/setup.bash" >> ~/.bashrc
```

프로젝트를 다른 위치로 옮겼다면 위 경로도 실제 경로로 바꿉니다. ROS 기본 환경을 먼저 source하고, 그 다음 오버레이 워크스페이스를 source하는 순서가 중요합니다.

## 4. 설치 직후 검증

각 명령은 오류 없이 끝나야 합니다.

```bash
source /opt/ros/jazzy/setup.bash
ros2 --help
ros2 pkg prefix ros_gz_bridge
colcon --help
gz sim --versions
ros2 doctor --report
```

다음으로 ROS 통신 자체를 검증합니다. 터미널 1:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp talker
```

터미널 2:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_py listener
```

listener에 `I heard: [Hello World: ...]`가 반복되면 ROS 2 DDS 통신까지 정상입니다. 마지막으로 아래 명령을 실행해 Gazebo 창이 열리는지 확인합니다.

```bash
gz sim shapes.sdf
```

창이 열리지 않고 렌더링 오류가 나면 그래픽 드라이버 또는 원격 데스크톱 환경 문제일 수 있습니다. `gz sim -s shapes.sdf`는 GUI 없이 서버만 실행하므로 물리/토픽 실습을 계속할 수 있습니다.

## 5. YOLO 선택 설치 — M17 직전에만

M17 전에는 필요 없습니다. Ubuntu 시스템 Python을 건드리지 않도록 가상 환경을 사용합니다.

```bash
python3 -m venv --system-site-packages ~/.venvs/agv-vision
source ~/.venvs/agv-vision/bin/activate
python -m pip install --upgrade pip
python -m pip install ultralytics
python -c "from ultralytics import YOLO; print('ultralytics import OK')"
```

각 YOLO 실습 터미널에서는 ROS를 source한 뒤 이 가상 환경을 활성화합니다.

```bash
source /opt/ros/jazzy/setup.bash
source ~/.venvs/agv-vision/bin/activate
```

## 실패했을 때 순서

1. `source /opt/ros/jazzy/setup.bash`를 빼먹지 않았는지 확인합니다.
2. `apt-cache policy ros-jazzy-desktop`으로 Jazzy 패키지 후보가 있는지 확인합니다.
3. `ros2 doctor --report`와 `bash scripts/verify_install.sh` 결과를 저장합니다.
4. Gazebo만 문제면 `gz sim --versions`와 `echo $GZ_SIM_RESOURCE_PATH`를 확인합니다.
5. 워크스페이스만 문제면 `cd agv_ws && rm -rf build install log` 대신, 먼저 `colcon build --event-handlers console_direct+`의 **첫 오류**를 읽습니다. 삭제 빌드는 마지막 수단입니다.

### 이 PC에서 실제로 만난 Miniconda 충돌

이 PC에는 Miniconda의 Python 3.13이 활성화되어 있었습니다. ROS 2 Jazzy deb 패키지는 Ubuntu의 Python 3.12로 설치되므로, `colcon build`가 Miniconda를 잡으면 `ModuleNotFoundError: No module named 'em'` 같은 오류가 납니다. 아래 둘 중 하나로 표준 Python을 선택합니다.

```bash
conda deactivate
source /opt/ros/jazzy/setup.bash
cd ~/ros2_curri/agv_ws
colcon build --symlink-install --cmake-clean-cache --cmake-args -DPython3_EXECUTABLE=/usr/bin/python3
```

또는 conda를 유지해야 한다면 현재 터미널에만 다음을 적용합니다.

```bash
export PATH=/usr/bin:/bin:$PATH
source /opt/ros/jazzy/setup.bash
```

## 공식 근거

- [ROS 2 Jazzy Ubuntu 설치 문서](https://docs.ros.org/en/jazzy/Installation/Alternatives/Ubuntu-Install-Binary.html) — Ubuntu Noble 지원과 `ros2-apt-source` 등록 방식을 확인했습니다.
- [Gazebo의 ROS 설치 조합 문서](https://gazebosim.org/docs/harmonic/ros_installation/) — Jazzy + Harmonic이 권장 조합이며 `ros-${ROS_DISTRO}-ros-gz`로 기본 조합을 설치한다고 안내합니다.
- [ros_gz_bridge 공식 사용법](https://gazebosim.org/docs/harmonic/ros2_integration/) — bridge YAML의 필드와 방향 설정을 확인합니다.
