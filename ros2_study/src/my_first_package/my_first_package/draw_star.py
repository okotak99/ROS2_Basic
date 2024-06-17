import rclpy as rp
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math


class DrawStar(Node):
    def __init__(self):
        super().__init__('draw_star')
        self.timer_period = 1.0
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        star_points = [(0, 2), (1, 1), (2, 0), (1, -1), (0, -2), (-1, -1), (-2, 0), (-1, 1), (0, 2)]
        current_point = star_points.pop(0)
        next_point = star_points[0]

        # Calculate linear and angular velocity to move to the next point
        linear_vel = math.sqrt((next_point[0] - current_point[0])**2 + (next_point[1] - current_point[1])**2)
        angular_vel = math.atan2(next_point[1] - current_point[1], next_point[0] - current_point[0])

        self.move_robot(linear_vel, angular_vel)

    def move_robot(self, linear_vel, angular_vel):
        msg = Twist()
        msg.linear.x = linear_vel
        msg.angular.z = angular_vel
        self.publisher.publish(msg)


def main(args=None):
    rp.init(args=args)
    draw_star_node = DrawStar()
    rp.spin_once(draw_star_node)
    draw_star_node.destroy_node()
    rp.shutdown()


if __name__ == '__main__':
    main()
