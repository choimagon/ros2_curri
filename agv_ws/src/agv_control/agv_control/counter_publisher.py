import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class CounterPublisher(Node):
    def __init__(self):
        super().__init__('counter_publisher')
        self.publisher = self.create_publisher(Int32, '/counter', 10)
        self.value = 0
        self.create_timer(1.0, self.publish_counter)

    def publish_counter(self):
        message = Int32(data=self.value)
        self.publisher.publish(message)
        self.get_logger().info(f'/counter: {message.data}')
        self.value += 1


def main():
    rclpy.init(); node = CounterPublisher()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()
