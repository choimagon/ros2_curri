from setuptools import find_packages, setup
package_name = 'agv_mission'
setup(name=package_name, version='0.1.0', packages=find_packages(exclude=['test']), data_files=[('share/ament_index/resource_index/packages', ['resource/' + package_name]), ('share/' + package_name, ['package.xml'])], install_requires=['setuptools'], zip_safe=True, maintainer='AGV student', maintainer_email='student@example.com', license='Apache-2.0', entry_points={'console_scripts': ['mission_manager = agv_mission.mission_manager:main', 'mission_markers = agv_mission.mission_markers:main']})
