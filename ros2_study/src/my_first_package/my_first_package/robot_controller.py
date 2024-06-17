import rclpy as rp
from rclpy.node import Node
from my_first_package_msgs.srv import AllocateTask


class RobotStatusServer(Node):
    def __init__(self):
        super().__init__('robot_status_server')
        self.srv = self.create_service(AllocateTask, 'allocate_task', self.allocate_task_callback)
        self.get_logger().info('Service server ready')

    def allocate_task_callback(self, request, response):
        # Extracting request data
        task_type = request.task_type
        location = request.location
        item = request.item
        quantity = request.quantity

        # Perform different actions based on task_type
        if task_type == "IB":
            response.success = self.inbound_process(location)

        # elif task_type == "OB":
        #     # response.success = self.outbound_preocess(location)
        #     pass

        # elif task_type == "RE":
        #     pass

        # elif task_type == "CG":
        #     pass

        else:
            response.success = False
        
        return response
    

    def inbound_process(self, location):
        print("입고")

        if location == "I1":
            print("I1 이동 (goal)")
            print("UP")
            return True
            
        elif location == "I2":
            print("I2 이동 (goal)")
            print("UP")
            return True

        elif location == "I3":
            print("I3 이동 (goal)")
            print("UP")
            return True

        elif location == "A1-1":
            print("A1 이동 (goal)")
            floor = location.split("-")[1]
            print(f"{floor} Down")
            return True

        # Add other cases if needed
        else:
            return False
    

def main(args=None):
    rp.init(args=args)
    robot_controller = RobotStatusServer()
    rp.spin(robot_controller)

    robot_controller.destroy_node()
    rp.shutdown()


if __name__=='__main__':
    main()