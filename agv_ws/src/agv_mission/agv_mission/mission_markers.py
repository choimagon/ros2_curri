"""RViz markers that make the safety sector and mission FSM visible."""
import math

import rclpy
from geometry_msgs.msg import Point
from rclpy.node import Node
from std_msgs.msg import Float32, String
from visualization_msgs.msg import Marker, MarkerArray


class MissionMarkers(Node):
    def __init__(self):
        super().__init__('mission_markers')
        self.declare_parameter('stop_distance', 0.50)
        self.declare_parameter('front_half_angle_deg', 15.0)
        self.distance = math.inf
        self.state = 'IDLE'
        self.publisher = self.create_publisher(MarkerArray, '/agv_markers', 10)
        self.create_subscription(Float32, '/obstacle_distance', self.distance_callback, 10)
        self.create_subscription(String, '/mission_state', self.state_callback, 10)
        self.create_timer(0.2, self.publish_markers)

    def distance_callback(self, message):
        self.distance = message.data

    def state_callback(self, message):
        self.state = message.data

    def publish_markers(self):
        stamp = self.get_clock().now().to_msg()
        stop_distance = float(self.get_parameter('stop_distance').value)
        half_angle = math.radians(float(self.get_parameter('front_half_angle_deg').value))
        unsafe = self.distance < stop_distance
        sector = Marker()
        sector.header.frame_id, sector.header.stamp = 'base_link', stamp
        sector.ns, sector.id, sector.type, sector.action = 'safety_sector', 0, Marker.LINE_STRIP, Marker.ADD
        sector.scale.x = 0.025
        sector.color.r, sector.color.g, sector.color.b, sector.color.a = (1.0, 0.15, 0.05, 0.95) if unsafe else (0.05, 0.9, 0.25, 0.95)
        sector.points = [Point(x=0.0, y=0.0, z=0.04)]
        for index in range(25):
            angle = -half_angle + (2.0 * half_angle * index / 24.0)
            sector.points.append(Point(x=stop_distance * math.cos(angle), y=stop_distance * math.sin(angle), z=0.04))
        sector.points.append(Point(x=0.0, y=0.0, z=0.04))

        text = Marker()
        text.header.frame_id, text.header.stamp = 'base_link', stamp
        text.ns, text.id, text.type, text.action = 'mission_state', 1, Marker.TEXT_VIEW_FACING, Marker.ADD
        text.pose.position.z = 0.48
        text.scale.z = 0.16
        text.color.r, text.color.g, text.color.b, text.color.a = 1.0, 1.0, 1.0, 1.0
        distance = 'inf' if not math.isfinite(self.distance) else f'{self.distance:.2f} m'
        text.text = f'{self.state} | obstacle {distance}'
        self.publisher.publish(MarkerArray(markers=[sector, text]))


def main():
    rclpy.init()
    node = MissionMarkers()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
