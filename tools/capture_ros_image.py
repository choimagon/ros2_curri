#!/usr/bin/env python3
"""Save one ROS Image message as a PNG for versioned course evidence."""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image


class OneImage(Node):
    def __init__(self, topic: str, output: Path):
        super().__init__('course_image_capture')
        self.output = output
        self.bridge = CvBridge()
        self.create_subscription(Image, topic, self.callback, qos_profile_sensor_data)

    def callback(self, message: Image) -> None:
        image = self.bridge.imgmsg_to_cv2(message, desired_encoding='bgr8')
        self.output.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(self.output), image):
            raise RuntimeError(f'could not write {self.output}')
        self.get_logger().info(f'saved {self.output} ({image.shape[1]}x{image.shape[0]})')
        rclpy.shutdown()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('topic')
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    rclpy.init()
    node = OneImage(args.topic, args.output)
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
