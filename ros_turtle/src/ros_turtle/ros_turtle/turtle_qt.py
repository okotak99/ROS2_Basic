import sys
import signal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import rclpy as rp
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
import math
from threading import Thread
from PyQt5.QtCore import pyqtSignal
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg

from_class = uic.loadUiType("/home/addinedu/dev_ws/ros_turtle/src/ros_turtle/UI/controll.ui")[0]

class TurtleSpawner(Node):
    def __init__(self, ui):
        super().__init__('turtle_spawner')
        self.ui = ui
        self.spawn_service = self.create_client(Spawn, 'spawn')
        self.count = 1
        self.spawn_turtle()


    def spawn_turtle(self):
        request1 = Spawn.Request()
        request1.name = 'turtle2'
        request1.x = 2.0
        request1.y = 2.0
        request1.theta = 0.0
        future1 = self.spawn_service.call_async(request1)


        request2 = Spawn.Request()
        request2.name = 'turtle3'
        request2.x = 8.0
        request2.y = 8.0
        request2.theta = 0.0
        future2 = self.spawn_service.call_async(request2)

        rp.spin_until_future_complete(self, future1)
        rp.spin_until_future_complete(self, future2)

        if future1.result() is not None:
            self.get_logger().info('Turtle2 spawned successfully')
        if future2.result() is not None:
            self.get_logger().info('Turtle3 spawned successfully')

class TurtleDrawCircle(Node):
    def __init__(self, ui):
        super().__init__('draw_circle_node')
        self.ui = ui
        self.pub_1 = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pub_2 = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.pub_3 = self.create_publisher(Twist, '/turtle3/cmd_vel', 10)
        self.timer = self.create_timer(1, self.timer_callback)
        self.ui.circleClicked.connect(self.handle_turtle)
        self.ui.starClicked.connect(self.handle_turtle_star)
        self.is_circle_clicked = False
        self.is_star_clicked = False
        self.star_toggle = True

    def handle_turtle(self):
        if self.ui.circleCombo.currentText() == 'turtle2':
           self.toggle = 2
        elif self.ui.circleCombo.currentText() == 'turtle3':
            self.toggle = 3
        else: 
            self.toggle = 1

        self.is_circle_clicked = True
        self.is_star_clicked = False

    def handle_turtle_star(self):
        if self.ui.circleCombo.currentText() == 'turtle2':
           self.toggle = 2
        elif self.ui.circleCombo.currentText() == 'turtle3':
            self.toggle = 3
        else: 
            self.toggle = 1

        self.is_circle_clicked = False
        self.is_star_clicked = True


    def timer_callback(self):
        if self.is_circle_clicked:
            msg = Twist() 
            linear_vel = float(self.ui.velLineEdit.text())
            radius = float(self.ui.radLineEdit.text())

            msg.linear.x = linear_vel
            msg.linear.y = 0.0
            msg.angular.z = linear_vel / radius
            
            self.is_star_clicked = False

            if self.toggle == 1:
                self.pub_1.publish(msg)
            elif self.toggle == 2:
                self.pub_2.publish(msg)
            else: 
                self.pub_3.publish(msg)

        if self.is_star_clicked:
            msg = Twist()
            linear_vel = float(self.ui.velLineEdit.text())

            self.is_circle_clicked = False

            if self.star_toggle:
                msg.linear.x = linear_vel
                msg.linear.y = 0.0
                msg.angular.z = 0.0
                self.star_toggle = False
            else:
                msg.linear.x = 0.0
                msg.linear.y = 0.0
                msg.angular.z = 2.51328
                self.star_toggle = True
            
            if self.toggle == 1:
                self.pub_1.publish(msg)
            elif self.toggle == 2:
                self.pub_2.publish(msg)
            else: 
                self.pub_3.publish(msg)


        
class TurtlePosition(Node):
    def __init__(self, ui):
        super().__init__('postion_subscriber')
        self.ui = ui
        self.pose_sub1 = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback1, 10)
        self.pose_sub2 = self.create_subscription(Pose, '/turtle2/pose', self.pose_callback2, 10)
        self.pose_sub3 = self.create_subscription(Pose, '/turtle3/pose', self.pose_callback3, 10)
        self.pose1 = Pose()
        self.pose2 = Pose()
        self.pose3 = Pose()

        self.turtle_x = []
        self.turtle_y = []
        self.turtle_plot = self.ui.map.plot(pen='r')
        self.ui.map.setRange(xRange=[0, 11], yRange=[0, 11])
        self.ui.map.setLabel('left', 'Y')
        self.ui.map.setLabel('bottom', 'X')
        self.ui.map.setBackground('w')


    def pose_callback1(self, data):
        self.ui.turtle1xLabel.setText(str(round(data.x, 2)))
        self.ui.turtle1yLabel.setText(str(round(data.y, 2)))
        self.ui.turtle1thetaLabel.setText(str(round(data.theta, 2)))
        self.turtle_x.append(round(data.x, 2))
        self.turtle_y.append(round(data.y, 2))
        self.turtle_plot.setData(self.turtle_x, self.turtle_y)

    def pose_callback2(self, data):
        self.ui.turtle2xLabel.setText(str(round(data.x, 2)))
        self.ui.turtle2yLabel.setText(str(round(data.y, 2)))
        self.ui.turtle2thetaLabel.setText(str(round(data.theta, 2)))

    def pose_callback3(self, data):
        self.ui.turtle3xLabel.setText(str(round(data.x, 2)))
        self.ui.turtle3yLabel.setText(str(round(data.y, 2)))
        self.ui.turtle3thetaLabel.setText(str(round(data.theta, 2)))


class TurtleGTG(Node):
    def __init__(self, ui):
        super().__init__('gtg_controller')
        self.ui = ui
        self.pose_sub1 = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback1, 10)
        self.pose_sub2 = self.create_subscription(Pose, '/turtle2/pose', self.pose_callback2, 10)
        self.pose_sub3 = self.create_subscription(Pose, '/turtle3/pose', self.pose_callback3, 10)
        self.goal_pub1 = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.goal_pub2 = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.goal_pub3 = self.create_publisher(Twist, '/turtle3/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.go_to_goal)
        
        self.ui.goalClicked.connect(self.handle_goal_click)  
        self.pose = Pose()
        self.is_goal_clicked = False
        self.toggle = 1 

    def handle_goal_click(self):
        if self.ui.goalCombo.currentText() == 'turtle2':
           self.toggle = 2
        elif self.ui.goalCombo.currentText() == 'turtle3':
            self.toggle = 3
        else: 
            self.toggle = 1
        self.is_goal_clicked = True

    def pose_callback1(self, data):
        if self.toggle == 1:
            self.pose = data

    def pose_callback2(self, data):
        if self.toggle == 2:
            self.pose = data

    def pose_callback3(self, data):
        if self.toggle == 3:
            self.pose = data


    def go_to_goal(self):
        if self.is_goal_clicked:
            goal = Pose()
            goal.x = float(self.ui.destXLineEdit.text())
            goal.y = float(self.ui.destYLineEdit.text())
            goal.theta = float(self.ui.destThetaLineEdit.text())
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

            else :
                if ( distance_to_goal ) >= distance_tolerance:
                    new_vel.linear.x = kp * distance_to_goal

                else :
                    new_vel.linear.x= 0.0
                    new_vel.angular.z = 0.0
                    # self.get_logger().info("Goal Reached")
                    self.is_goal_clicked = False


            if self.toggle == 1:
                self.goal_pub1.publish(new_vel)
            elif self.toggle == 2:
                self.goal_pub2.publish(new_vel)
            else:
                self.goal_pub3.publish(new_vel)
        
        else:
            pass


class QtController(QDialog, from_class):
    goalClicked = pyqtSignal(bool)
    circleClicked = pyqtSignal(bool)
    starClicked = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Qt turtle Controller")

        self.destXLineEdit.setText('5.54')
        self.destYLineEdit.setText('5.54')
        self.destThetaLineEdit.setText('0')

        self.goalBtn.clicked.connect(self.gtg_turtle)
        self.circleBtn.clicked.connect(self.draw_circle)
        self.starBtn.clicked.connect(self.draw_star)

    def gtg_turtle(self):
        self.goalClicked.emit(True)

    def draw_circle(self):
        self.circleClicked.emit(True)

    def draw_star(self):
        self.starClicked.emit(True)

    
    def closeEvent(self, event):
        rp.shutdown()
        super().closeEvent(event)



if __name__ == "__main__":
    rp.init()   
    executor = MultiThreadedExecutor()

    app = QApplication(sys.argv) 
    myWindows = QtController() 
    myWindows.show()   

    spawn_node = TurtleSpawner(myWindows)
    executor.add_node(spawn_node)

    position_node = TurtlePosition(myWindows)
    executor.add_node(position_node)

    draw_circle_node = TurtleDrawCircle(myWindows)
    executor.add_node(draw_circle_node)

    gtg_node = TurtleGTG(myWindows)
    executor.add_node(gtg_node)

    thread = Thread(target=executor.spin)
    thread.start()

    sys.exit(app.exec_())
       