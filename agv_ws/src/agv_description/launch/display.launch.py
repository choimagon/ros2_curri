from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    share = get_package_share_directory('agv_description')
    xacro_file = os.path.join(share, 'urdf', 'agv.urdf.xacro')
    rviz_file = os.path.join(share, 'rviz', 'agv.rviz')
    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)
    return LaunchDescription([
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui'),
        Node(package='robot_state_publisher', executable='robot_state_publisher', parameters=[{'robot_description': robot_description}]),
        Node(package='rviz2', executable='rviz2', arguments=['-d', rviz_file]),
    ])
