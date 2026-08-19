from setuptools import find_packages, setup
package_name = 'agv_vision'
setup(name=package_name, version='0.1.0', packages=find_packages(exclude=['test']), data_files=[('share/ament_index/resource_index/packages', ['resource/' + package_name]), ('share/' + package_name, ['package.xml'])], install_requires=['setuptools'], zip_safe=True, maintainer='AGV student', maintainer_email='student@example.com', license='Apache-2.0', entry_points={'console_scripts': ['yolo_node = agv_vision.yolo_node:main']})
