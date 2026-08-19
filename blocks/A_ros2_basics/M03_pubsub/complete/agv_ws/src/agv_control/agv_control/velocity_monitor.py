import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityMonitor(Node):
    def __init__(self):
        super().__init__('velocity_monitor')
        self.create_subscription(Twist, '/cmd_vel', self.callback, 10)

    def callback(self, message):
        self.get_logger().info('cmd_vel linear.x=%.3f angular.z=%.3f' % (message.linear.x, message.angular.z))


def main():
    rclpy.init(); node = VelocityMonitor()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()
