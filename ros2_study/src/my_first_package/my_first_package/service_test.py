import rclpy
from rclpy.node import Node
from my_first_package_msgs.srv import AllocateTask

class TaskAllocatorClient(Node):
    def __init__(self):
        super().__init__('task_allocator_client')
        self.cli = self.create_client(AllocateTask, 'allocate_task')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.request = AllocateTask.Request()

    def send_task_request(self, task_type, location, item, quantity):
        self.request.task_type = task_type
        self.request.location = location
        self.request.item = item
        self.request.quantity = quantity
        self.future = self.cli.call_async(self.request)
        self.future.add_done_callback(self.callback)

    def callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info('Task successfully allocated')
            else:
                self.get_logger().warning('Failed to allocate task:')
        except Exception as e:
            self.get_logger().error('Service call failed %r' % (e,))

def main(args=None):
    rclpy.init(args=args)
    client = TaskAllocatorClient()

    # Example task requests
    client.send_task_request(task_type="IB", location="I1", item="ramen", quantity=1)

    rclpy.spin_once(client)
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
