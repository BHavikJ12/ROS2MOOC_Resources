import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import PS4Service  
from std_msgs.msg import String

class PS4Client(Node):
    def __init__(self):
        super().__init__('ps4_client')
        self.client = self.create_client(PS4Service, 'ps4_service')
        #######################Complete This Section ###########################
        
        # Create a publisher to publish the response on topic "ps4_result"
        
        ########################################################################

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available, waiting...")

        self.request_ps4_service()

    ############## Complete This Section ############## 
    def request_ps4_service(self):
        
    
    def handle_response(self, future):
        
        response = future.result()
        if response:
                        
            # Combine the message and unique_id into one string
            combined_message = f"{response.message} unique ID: {response.unique_id}"
            # Create a String message to publish
            
            # Publish the combined message

        else:
            self.get_logger().info("Failed to receive a valid response.")
    ###################################################

def main(args=None):
    rclpy.init(args=args)
    client = PS4Client()
    rclpy.spin(client)
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
