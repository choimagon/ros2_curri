import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class PidController(Node):
    """A small P-only starting point: replace with PI/PID after observing overshoot."""
    def __init__(self):
        super().__init__('pid_controller')
        self.declare_parameter('kp_angular', 0.004)
        self.declare_parameter('max_linear_speed', 0.25)
        self.declare_parameter('max_angular_speed', 0.8)
        self.publisher = self.create_publisher(Twist, '/cmd_vel_raw', 10)
        self.create_subscription(Twist, '/target_error', self.error_callback, 10)

    def error_callback(self, error):
        command = Twist()
        command.linear.x = min(max(error.linear.x, 0.0), self.get_parameter('max_linear_speed').value)
        command.angular.z = max(min(error.angular.z * self.get_parameter('kp_angular').value, self.get_parameter('max_angular_speed').value), -self.get_parameter('max_angular_speed').value)
        self.publisher.publish(command)


def main():
    rclpy.init(); node = PidController()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()
