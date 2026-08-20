"""M16 isolated launch: gz_ros2_control, two active controllers, and a physical AGV."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, SetEnvironmentVariable, TimerAction
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    gazebo = get_package_share_directory('agv_gazebo')
    models = os.path.join(gazebo, 'models')
    world = os.path.join(gazebo, 'worlds', 'warehouse_ros2_control.sdf')
    description = get_package_share_directory('agv_description')
    gz_launch = os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
    previous = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    simulator = IncludeLaunchDescription(PythonLaunchDescriptionSource(gz_launch), launch_arguments={'gz_args': '-r ' + world}.items())
    robot_description = ParameterValue(Command(['xacro ', os.path.join(description, 'urdf', 'agv_ros2_control.urdf.xacro')]), value_type=str)
    jsb = Node(package='controller_manager', executable='spawner', arguments=['joint_state_broadcaster', '-c', '/controller_manager'], output='screen')
    drive = Node(package='controller_manager', executable='spawner', arguments=['diff_drive_controller', '-c', '/controller_manager'], output='screen')
    return LaunchDescription([
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', models + (':' + previous if previous else '')),
        simulator,
        Node(package='robot_state_publisher', executable='robot_state_publisher', parameters=[{'robot_description': robot_description, 'use_sim_time': True}], output='screen'),
        Node(package='ros_gz_bridge', executable='parameter_bridge', arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'], output='screen'),
        # The plugin creates /controller_manager inside Gazebo. Spawn in series so
        # both service calls do not contend for controller_manager's lifecycle lock.
        TimerAction(period=6.0, actions=[jsb]),
        RegisterEventHandler(OnProcessExit(target_action=jsb, on_exit=[drive])),
    ])
