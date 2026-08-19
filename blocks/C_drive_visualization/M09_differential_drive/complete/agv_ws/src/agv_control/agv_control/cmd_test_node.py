import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CmdTestNode(Node):
    def __init__(self):
        super().__init__('cmd_test_node')
        self.declare_parameter('linear_speed', 0.15)
        self.declare_parameter('angular_speed', 0.0)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.remaining = 30
        self.create_timer(0.1, self.publish_once)

    def publish_once(self):
        command = Twist()
        if self.remaining > 0:
            command.linear.x = self.get_parameter('linear_speed').value
            command.angular.z = self.get_parameter('angular_speed').value
            self.remaining -= 1
        self.publisher.publish(command)
        if self.remaining == 0:
            self.get_logger().info('test command finished; publishing zero Twist')
            self.remaining = -1


def main():
    rclpy.init(); node = CmdTestNode()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()
