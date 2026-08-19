import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory('agv_gazebo')
    world = os.path.join(share, 'worlds', 'warehouse.sdf')
    models = os.path.join(share, 'models')
    previous = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    gz_launch = os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
    return LaunchDescription([
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', models + (':' + previous if previous else '')),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(gz_launch), launch_arguments={'gz_args': '-r ' + world}.items()),
        Node(package='ros_gz_bridge', executable='parameter_bridge', parameters=[{'config_file': os.path.join(share, 'config', 'bridge.yaml')}], output='screen'),
    ])
