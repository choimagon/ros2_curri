from setuptools import find_packages, setup

package_name = 'agv_control'
setup(name=package_name, version='0.1.0', packages=find_packages(exclude=['test']),
      data_files=[('share/ament_index/resource_index/packages', ['resource/' + package_name]), ('share/' + package_name, ['package.xml']), ('share/' + package_name + '/config', ['config/controllers.yaml'])],
      install_requires=['setuptools'], zip_safe=True, maintainer='AGV student', maintainer_email='student@example.com', license='Apache-2.0',
      entry_points={'console_scripts': [
          'counter_publisher = agv_control.counter_publisher:main', 'counter_monitor = agv_control.counter_monitor:main',
          'cmd_test_node = agv_control.cmd_test_node:main', 'velocity_monitor = agv_control.velocity_monitor:main',
          'safety_controller = agv_control.safety_controller:main', 'pid_controller = agv_control.pid_controller:main']})
