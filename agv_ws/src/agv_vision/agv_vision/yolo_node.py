import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from agv_interfaces.msg import Detection, DetectionArray
import cv2


class YoloNode(Node):
    def __init__(self):
        super().__init__('yolo_node')
        self.declare_parameter('model_path', 'yolo11n.pt')
        self.declare_parameter('confidence_threshold', 0.50)
        self.declare_parameter('enable_yolo', False)
        self.declare_parameter('enable_red_target_fallback', True)
        self.declare_parameter('target_width_m', 0.25)
        self.bridge = CvBridge()
        self.publisher = self.create_publisher(DetectionArray, '/detections', 10)
        self.debug_publisher = self.create_publisher(Image, '/vision/debug_image', qos_profile_sensor_data)
        self.create_subscription(Image, '/camera/image_raw', self.callback, qos_profile_sensor_data)
        self.model = None
        if self.get_parameter('enable_yolo').value:
            try:
                from ultralytics import YOLO
                self.model = YOLO(self.get_parameter('model_path').value)
                self.get_logger().info('YOLO model loaded')
            except ImportError:
                self.get_logger().error('ultralytics is not installed: follow M17 before enable_yolo:=true')

    def make_detection(self, header, class_name, confidence, x1, y1, x2, y2, image_width):
        """Estimate distance with a pinhole model for the fixed 60-degree course camera."""
        width = max(1, x2 - x1)
        focal_px = image_width / (2.0 * 0.57735)
        distance = float(self.get_parameter('target_width_m').value) * focal_px / width
        return Detection(
            header=header, class_name=class_name, confidence=float(confidence),
            center_x=(x1 + x2) // 2, center_y=(y1 + y2) // 2,
            width=width, height=max(1, y2 - y1), estimated_distance=distance)

    def red_target_detection(self, image, header):
        """Dependency-free fallback for the red target placed in warehouse.sdf.

        This is deliberately labelled as a fallback in the debug image.  It keeps
        M17--M22 runnable before a learner downloads a YOLO model, while the same
        Detection message and mission interface are used by real YOLO inference.
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_red = cv2.inRange(hsv, (0, 90, 70), (12, 255, 255))
        upper_red = cv2.inRange(hsv, (165, 90, 70), (179, 255, 255))
        mask = cv2.bitwise_or(lower_red, upper_red)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(contour) < 80:
            return None
        x, y, width, height = cv2.boundingRect(contour)
        return self.make_detection(header, 'red_target_fallback', 0.90, x, y, x + width, y + height, image.shape[1])

    def callback(self, image_message):
        image = self.bridge.imgmsg_to_cv2(image_message, desired_encoding='bgr8')
        debug = image.copy()
        output = DetectionArray(header=image_message.header)
        label = 'no detection'
        if self.model is not None:
            result = self.model(image, verbose=False)[0]
            threshold = self.get_parameter('confidence_threshold').value
            for box in result.boxes:
                confidence = float(box.conf[0])
                if confidence < threshold:
                    continue
                x1, y1, x2, y2 = [int(value) for value in box.xyxy[0].tolist()]
                detection = self.make_detection(image_message.header, result.names[int(box.cls[0])], confidence, x1, y1, x2, y2, image.shape[1])
                output.detections.append(detection)
                cv2.rectangle(debug, (x1, y1), (x2, y2), (30, 220, 30), 2)
                label = f'YOLO {detection.class_name} {confidence:.2f}'
        elif self.get_parameter('enable_red_target_fallback').value:
            detection = self.red_target_detection(image, image_message.header)
            if detection is not None:
                output.detections.append(detection)
                x1 = detection.center_x - detection.width // 2
                y1 = detection.center_y - detection.height // 2
                x2, y2 = x1 + detection.width, y1 + detection.height
                cv2.rectangle(debug, (x1, y1), (x2, y2), (0, 215, 255), 2)
                label = f'course fallback target {detection.estimated_distance:.2f} m'
            else:
                label = 'course fallback: red target not visible'
        cv2.putText(debug, label, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        self.publisher.publish(output)
        self.debug_publisher.publish(self.bridge.cv2_to_imgmsg(debug, encoding='bgr8'))


def main():
    rclpy.init(); node = YoloNode()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()
