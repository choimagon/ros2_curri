import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32


class LidarProcessor(Node):
    def __init__(self):
        super().__init__('lidar_processor')
        self.declare_parameter('front_half_angle_deg', 15.0)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.callback, qos_profile_sensor_data)
        self.publisher = self.create_publisher(Float32, '/obstacle_distance', 10)

    def callback(self, scan):
        half_angle = math.radians(self.get_parameter('front_half_angle_deg').value)
        front_ranges = [distance for index, distance in enumerate(scan.ranges)
                        if abs(scan.angle_min + index * scan.angle_increment) <= half_angle and math.isfinite(distance)]
        result = Float32(data=min(front_ranges) if front_ranges else float('inf'))
        self.publisher.publish(result)


def main():
    rclpy.init(); node = LidarProcessor()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()
