import rclpy as rp
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
import math
import sys


class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_qt_controller')
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.goal_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.go_to_goal)
        self.pose = Pose()
        # self.spawn_turtle_service = self.create_client(Spawn, 'spawn')

        self.is_goal_clicked = False
        self.x = None
        self.y = None
        self.theta = None


    def click_button(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.is_goal_clicked = True


    def pose_callback(self, data):
        self.pose = data
        


    def go_to_goal(self):
        if self.is_goal_clicked:
        
            goal = Pose()
            goal.x = self.x
            goal.y = self.y
            goal.theta = self.theta

            new_vel = Twist()

            # Ecludian Distance
            distance_to_goal = math.sqrt( (goal.x - self.pose.x)**2  + (goal.y - self.pose.y)**2 )
            # Angle to Goal
            angle_to_goal =math.atan2(goal.y - self.pose.y , goal.x - self.pose.x)

            distance_tolerance = 0.1
            angle_tolerance = 0.01

            angle_error = angle_to_goal - self.pose.theta
            kp = 5

            if abs(angle_error) > angle_tolerance:
                new_vel.angular.z = kp * angle_error
                print('ads')
            else :
                if( distance_to_goal ) >= distance_tolerance:
                    new_vel.linear.x = kp * distance_to_goal
                else :
                    new_vel.linear.x= 0.0
                    self.get_logger().info("Goal Reached ")
                    self.is_goal_clicked = False

            self.goal_pub.publish(new_vel)


    # def timer_callback(self):
    #     msg = Twist()
    #     # linear_vel
    #     # radius

    #     # msg.linear.x = linear_vel
    #     msg.linear.y = 0.0
    #     # msg.angular.z = linear.vel/radius
    #     self.cmd_vel_publisher.publish(msg)

    

    # def spawn_turtle(self, name, x, y, theta):
    #     request = Spawn.Request()
    #     request.name = name
    #     request.x = x
    #     request.y = y
    #     request.theta = theta
    #     future = self.spawn_turtle_service.call_async(request)
    #     rp.spin_until_future_complete(self, future)
    #     if future.result() is not None:
    #         self.get_logger().info('Turtle spawned successfully: %r' % future.result().name)
    #     else:
    #         self.get_logger().error('Failed to spawn turtle')


    # def set_turtle_velocity(self, linear, angular):
    #     msg = Twist()
    #     msg.linear.x = linear
    #     msg.angular.z = angular
    #     self.cmd_vel_publisher.publish(msg)
