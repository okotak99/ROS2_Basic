import rclpy as rp
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist


class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.spawn_turtle_service = self.create_client(Spawn, 'spawn')
        self.cmd_vel_publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)


    def spawn_turtle(self, name, x, y, theta):
        request = Spawn.Request()
        request.name = name
        request.x = x
        request.y = y
        request.theta = theta
        future = self.spawn_turtle_service.call_async(request)
        rp.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info('Turtle spawned successfully: %r' % future.result().name)
        else:
            self.get_logger().error('Failed to spawn turtle')


    def set_turtle_velocity(self, linear, angular):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.cmd_vel_publisher.publish(msg)

