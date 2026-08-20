"""Publish a bounded Path trail from the bridged Gazebo odometry topic."""
from collections import deque

import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path
from rclpy.node import Node


class OdomPath(Node):
    def __init__(self):
        super().__init__('odom_path')
        self.declare_parameter('max_poses', 500)
        self.poses = deque(maxlen=int(self.get_parameter('max_poses').value))
        self.publisher = self.create_publisher(Path, '/path', 10)
        self.create_subscription(Odometry, '/odom', self.callback, 10)

    def callback(self, message):
        pose = PoseStamped()
        pose.header = message.header
        pose.pose = message.pose.pose
        self.poses.append(pose)
        path = Path()
        path.header = message.header
        path.poses = list(self.poses)
        self.publisher.publish(path)


def main():
    rclpy.init()
    node = OdomPath()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
