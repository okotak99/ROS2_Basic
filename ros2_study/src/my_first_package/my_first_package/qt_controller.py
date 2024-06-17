from turtle_qt_controller import TurtleController
import sys
import signal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import rclpy as rp
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist


from_class = uic.loadUiType("my_first_package/UI/QtController.ui")[0]

class QtController(QDialog, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Qt turtle Controller")

        
        self.turtle_controller = TurtleController()
        self.spawnBtn.clicked.connect(self.spawnTurtle)
        # self.moveBtn.clicked.connect(self.moveTurtle)

        self.count = 1


    def spawnTurtle(self):
        self.count += 1
        name = f'turtle{self.count}'
        x = float(self.xLineEdit.text())
        y = float(self.yLineEdit.text())
        theta = float(self.thetaLineEdit.text())
        self.turtle_controller.spawn_turtle(name, x, y, theta)


    def moveTurtle(self):
        linear = float(self.linearVelLineEdit.text())
        angular = float(self.angularVelLineEdit.text())
        self.turtle_controller.set_turtle_velocity(linear, angular)


def shutdown_rp(turtle_controller):
    if turtle_controller is not None:
        turtle_controller.destroy_node()
        rp.shutdown()


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    rp.init()   
    myWindows = QtController() 
    myWindows.turtle_controller = TurtleController()
    myWindows.show()    
    signal.signal(signal.SIGINT, lambda sig, frame: shutdown_rp(myWindows.turtle_controller))  
    app.aboutToQuit.connect(lambda: shutdown_rp(myWindows.turtle_controller))         
    sys.exit(app.exec_())
       

