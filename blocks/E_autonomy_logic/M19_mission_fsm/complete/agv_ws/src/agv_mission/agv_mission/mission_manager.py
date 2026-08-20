import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32, String
from agv_interfaces.msg import DetectionArray


class MissionManager(Node):
    def __init__(self):
        super().__init__('mission_manager')
        self.declare_parameter('stop_distance', 0.50)
        self.declare_parameter('search_speed', 0.25)
        self.declare_parameter('approach_speed', 0.15)
        self.declare_parameter('image_center_x', 320)
        self.declare_parameter('target_timeout_sec', 0.70)
        self.state = 'IDLE'
        self.obstacle_distance = math.inf
        self.target = None
        self.last_target_time = None
        self.create_subscription(Float32, '/obstacle_distance', self.obstacle_callback, 10)
        self.create_subscription(DetectionArray, '/detections', self.detections_callback, 10)
        self.command_publisher = self.create_publisher(Twist, '/cmd_vel_raw', 10)
        self.state_publisher = self.create_publisher(String, '/mission_state', 10)
        self.create_timer(0.1, self.tick)

    def obstacle_callback(self, message):
        self.obstacle_distance = message.data

    def detections_callback(self, message):
        if message.detections:
            self.target = message.detections[0]
            self.last_target_time = self.get_clock().now()

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.get_logger().info('mission state -> ' + state)
        self.state_publisher.publish(String(data=self.state))

    def tick(self):
        command = Twist()
        if self.last_target_time is not None:
            age = (self.get_clock().now() - self.last_target_time).nanoseconds / 1e9
            if age > self.get_parameter('target_timeout_sec').value:
                self.target = None
        if self.obstacle_distance < self.get_parameter('stop_distance').value:
            self.set_state('AVOID')
            command.angular.z = self.get_parameter('search_speed').value
        elif self.target is None:
            self.set_state('SEARCH')
            command.angular.z = self.get_parameter('search_speed').value
        elif self.target.estimated_distance > 0.0 and self.target.estimated_distance < self.get_parameter('stop_distance').value:
            self.set_state('GOAL')
        else:
            self.set_state('APPROACH')
            command.linear.x = self.get_parameter('approach_speed').value
            error = self.target.center_x - self.get_parameter('image_center_x').value
            command.angular.z = max(min(-0.004 * error, 0.6), -0.6)
        self.command_publisher.publish(command)


def main():
    rclpy.init(); node = MissionManager()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()
