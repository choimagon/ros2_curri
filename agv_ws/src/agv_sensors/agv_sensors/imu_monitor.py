import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Imu


class ImuMonitor(Node):
    def __init__(self):
        super().__init__('imu_monitor')
        self.create_subscription(Imu, '/imu/data', self.callback, qos_profile_sensor_data)

    def callback(self, message):
        self.get_logger().info('gyro z=%.3f rad/s, acceleration z=%.3f m/s², frame=%s' % (message.angular_velocity.z, message.linear_acceleration.z, message.header.frame_id), throttle_duration_sec=1.0)


def main():
    rclpy.init(); node = ImuMonitor()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()
