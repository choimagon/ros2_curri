import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from agv_interfaces.msg import Detection, DetectionArray


class YoloNode(Node):
    def __init__(self):
        super().__init__('yolo_node')
        self.declare_parameter('model_path', 'yolo11n.pt')
        self.declare_parameter('confidence_threshold', 0.50)
        self.declare_parameter('enable_yolo', False)
        self.bridge = CvBridge()
        self.publisher = self.create_publisher(DetectionArray, '/detections', 10)
        self.create_subscription(Image, '/camera/image_raw', self.callback, qos_profile_sensor_data)
        self.model = None
        if self.get_parameter('enable_yolo').value:
            try:
                from ultralytics import YOLO
                self.model = YOLO(self.get_parameter('model_path').value)
                self.get_logger().info('YOLO model loaded')
            except ImportError:
                self.get_logger().error('ultralytics is not installed: follow M17 before enable_yolo:=true')

    def callback(self, image_message):
        output = DetectionArray(header=image_message.header)
        if self.model is not None:
            image = self.bridge.imgmsg_to_cv2(image_message, desired_encoding='bgr8')
            result = self.model(image, verbose=False)[0]
            threshold = self.get_parameter('confidence_threshold').value
            for box in result.boxes:
                confidence = float(box.conf[0])
                if confidence < threshold: continue
                x1, y1, x2, y2 = [int(value) for value in box.xyxy[0].tolist()]
                detection = Detection(header=image_message.header, class_name=result.names[int(box.cls[0])], confidence=confidence, center_x=(x1+x2)//2, center_y=(y1+y2)//2, width=x2-x1, height=y2-y1, estimated_distance=0.0)
                output.detections.append(detection)
        self.publisher.publish(output)


def main():
    rclpy.init(); node = YoloNode()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()
