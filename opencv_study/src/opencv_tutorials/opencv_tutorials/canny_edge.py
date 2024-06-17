import rclpy as rp
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CannyNode(Node):
    def __init__(self):
        super().__init__('canny_edge')
        self.subscriber = self.create_subscription(Image, '/camera', self.callback, 10)
        self.publisher = self.create_publisher(Image, 'canny', 10)
        self.cv_bridge = CvBridge()


    def callback(self, msg):
        cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Canny 엣지 검출
        edges = cv2.Canny(gray_image, 100, 200)

        # Canny 엣지를 ROS 메시지로 변환하여 퍼블리시
        canny_img_msg = self.cv_bridge.cv2_to_imgmsg(edges, encoding="mono8")
        self.publisher.publish(canny_img_msg)


def main(args=None):
    rp.init(args=args)
    canny_edge = CannyNode()
    rp.spin(canny_edge)
    canny_edge.destroy_node()
    rp.shutdown()



if __name__=='__main__':
    main()


