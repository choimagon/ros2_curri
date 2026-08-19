import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class SafetyController(Node):
    """Pass a desired command through unless an obstacle is within stop_distance."""
    def __init__(self):
        super().__init__('safety_controller')
        self.declare_parameter('stop_distance', 0.50)
        self.declare_parameter('front_half_angle_deg', 15.0)
        self.obstacle_distance = math.inf
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.create_subscription(Twist, '/cmd_vel_raw', self.command_callback, 10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def scan_callback(self, scan):
        limit = math.radians(self.get_parameter('front_half_angle_deg').value)
        readings = [value for index, value in enumerate(scan.ranges)
                    if abs(scan.angle_min + index * scan.angle_increment) <= limit and math.isfinite(value)]
        self.obstacle_distance = min(readings) if readings else math.inf

    def command_callback(self, command):
        safe = Twist()
        if self.obstacle_distance >= self.get_parameter('stop_distance').value or command.linear.x <= 0.0:
            safe = command
        else:
            self.get_logger().warn('obstacle at %.2f m: stopping forward command' % self.obstacle_distance)
        self.publisher.publish(safe)


def main():
    rclpy.init(); node = SafetyController()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()
