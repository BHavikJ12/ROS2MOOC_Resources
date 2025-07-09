import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, SetPen, TeleportAbsolute
from geometry_msgs.msg import Twist
from my_robot_interfaces.srv import GetCoordinates  
import math

class MySpawner(Node):
    def __init__(self, node_name):
        super().__init__(node_name)

    ######################################################## HINT #######################################################

        self.spawn_client = self.create_client(Spawn, '/spawn')


        # Create the service client for getting spawn coordinates

        # Spawn the first turtle and start movement
        self.spawn_turtle(self.next_turtle_index)
        self.get_logger().info(f'Starting movement towards turtle{self.next_turtle_index}')


    
    
    def calculate_movement(self, target_pose, current_pose):
        # Calculate the Euclidean distance between the current pose and target pose
        
        # Calculate the angle between the current position and the target position
        
        # Normalize the angle to be between -π and π

        return distance, angle

        
    
    def move_turtles(self):
   
        # Determine the next target turtle (based on next_turtle_index)
        target_turtle = f'turtle{self.next_turtle_index}'
        target_pose = self.turtle_poses.get(target_turtle)

        # If target turtle pose is not available, try to spawn it
        if not target_pose:
            self.get_logger().info(f'Target pose for {target_turtle} not available. Attempting to spawn it.')
            self.spawn_turtle(self.next_turtle_index)
            return
        
        # Calculate the distance and angle needed to move towards the target turtle's pose
        distance, angle = self.calculate_movement(target_pose, self.turtle1_pose)
        twist_msg1 = Twist()

        # If the distance to the target turtle is less than 0.8 units, stop moving turtle1
        if distance < 0.8:

            # Increment the next turtle index, and add the target turtle to the following list
 
            if self.next_turtle_index <= 10:
                self.get_logger().info(f'Spawning next turtle: {self.next_turtle_index}')
                self.spawn_turtle(self.next_turtle_index)
            else:
                self.get_logger().info('Maximum number of turtles (10) reached.')
        else:
            twist_msg1.linear.x = 
            twist_msg1.angular.z = 
            self.pub1.publish(twist_msg1)
            self.follow_turtle_sequence()

    def follow_turtle_sequence(self):
       
        # Define a gap distance for following turtles to maintain from turtle1
        gap_distance = 0.6
        leader_pose = self.turtle1_pose


        # Loop through each turtle that is following turtle1
        for follower in self.following_turtles:
            # Skip the follower if its pose is not yet available
            if not self.turtle_poses[follower]:
                continue
            
            # Calculate the new position for the follower to maintain the gap distance from the leader
            new_x = leader_pose.x - gap_distance * math.cos(leader_pose.theta)
            new_y = leader_pose.y - gap_distance * math.sin(leader_pose.theta)

            # Create a client for teleporting the follower to its new position
            teleport_client = self.create_client(TeleportAbsolute, f'/{follower}/teleport_absolute')
            teleport_request = TeleportAbsolute.Request(x=new_x, y=new_y, theta=leader_pose.theta)
            
            # Call the teleportation service to move the follower to the new position
            teleport_client.call_async(teleport_request)
           
            # Update the leader's position to the follower's position for the next iteration
            leader_pose = self.turtle_poses[follower]

    def stop_all_pens(self):
        # Loop through all the turtles in the following sequence and turn off their pens
        for turtle in self.following_turtles:
            pen_client = self.create_client(SetPen, f'/{turtle}/set_pen')
            pen_request = SetPen.Request(off=True)
            pen_client.call_async(pen_request)


    
    ##################################################################################################################################

def main(args=None):
    rclpy.init(args=args)
    node = MySpawner('pose_listener')

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
