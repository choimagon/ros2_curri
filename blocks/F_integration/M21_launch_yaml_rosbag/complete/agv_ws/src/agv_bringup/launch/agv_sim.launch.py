import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    bringup = get_package_share_directory('agv_bringup')
    description = get_package_share_directory('agv_description')
    gazebo = get_package_share_directory('agv_gazebo')
    xacro_file = os.path.join(description, 'urdf', 'agv.urdf.xacro')
    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)
    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true', description='Start RViz2'),
        DeclareLaunchArgument('autonomy', default_value='true', description='Start mission and safety nodes'),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(os.path.join(gazebo, 'launch', 'gazebo.launch.py'))),
        Node(package='robot_state_publisher', executable='robot_state_publisher', parameters=[os.path.join(bringup, 'config', 'robot.yaml'), {'robot_description': robot_description}]),
        Node(package='agv_sensors', executable='lidar_processor', parameters=[os.path.join(bringup, 'config', 'sensors.yaml')]),
        Node(package='agv_sensors', executable='imu_monitor', parameters=[os.path.join(bringup, 'config', 'sensors.yaml')]),
        Node(package='agv_sensors', executable='odom_path', parameters=[{'use_sim_time': True}]),
        Node(package='agv_vision', executable='yolo_node', parameters=[os.path.join(bringup, 'config', 'vision.yaml')]),
        Node(package='agv_mission', executable='mission_manager', parameters=[os.path.join(bringup, 'config', 'mission.yaml')], condition=IfCondition(LaunchConfiguration('autonomy'))),
        Node(package='agv_mission', executable='mission_markers', parameters=[os.path.join(bringup, 'config', 'mission.yaml')], condition=IfCondition(LaunchConfiguration('autonomy'))),
        Node(package='agv_control', executable='safety_controller', parameters=[os.path.join(bringup, 'config', 'mission.yaml')], condition=IfCondition(LaunchConfiguration('autonomy'))),
        Node(package='rviz2', executable='rviz2', arguments=['-d', os.path.join(description, 'rviz', 'agv.rviz')], condition=IfCondition(LaunchConfiguration('rviz'))),
    ])
