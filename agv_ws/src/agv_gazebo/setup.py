from glob import glob
from setuptools import find_packages, setup

package_name = 'agv_gazebo'
setup(name=package_name, version='0.1.0', packages=find_packages(exclude=['test']),
      data_files=[('share/ament_index/resource_index/packages', ['resource/' + package_name]), ('share/' + package_name, ['package.xml']),
                  ('share/' + package_name + '/launch', glob('launch/*.launch.py')), ('share/' + package_name + '/worlds', glob('worlds/*.sdf')),
                  ('share/' + package_name + '/config', glob('config/*.yaml')), ('share/' + package_name + '/models/agv', glob('models/agv/*'))],
      install_requires=['setuptools'], zip_safe=True, maintainer='AGV student', maintainer_email='student@example.com', license='Apache-2.0')
