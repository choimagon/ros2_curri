import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class CounterMonitor(Node):
    def __init__(self):
        super().__init__('counter_monitor')
        self.create_subscription(Int32, '/counter', self.callback, 10)

    def callback(self, message):
        self.get_logger().info(f'received /counter: {message.data}')


def main():
    rclpy.init(); node = CounterMonitor()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()
